# Cine York — solución (resuelto por Claude)

Enunciado: `ejercicio-stm-cine-york.pdf`. Sin compilar (no hay GHC instalado en esta máquina).

Interpretación de "reservar, que de la cantidad de grupos y una sala, realiza la reserva": `reservar` recibe
la lista de tamaños de los grupos (un thread por grupo) y la sala. La operación STM de un grupo se llama
`tomarButacas`.

## Ideas

```
R1 (nunca dos veces / nunca menos de k): buscar y ocupar las k butacas en UN solo atomically.
   Si dos grupos eligen la misma butaca, los dos leyeron y escribieron esa TVar: uno aborta y reintenta.

R2 (el que esperó no queda atado al pasado): la espera es un retry. Al despertarse, el atomically se
   re-ejecuta ENTERO desde el principio, leyendo la sala como está ahora -> aplica la misma política que
   a un recién llegado. No guardo nada de "lo que vi cuando empecé a esperar".

R3 (no despertarse por cambios que no pueden afectarlo): retry despierta cuando cambia CUALQUIER TVar
   leída. Si el grupo leyera todas las butacas antes de decidir esperar, lo despertaría cualquier
   butaca que se ocupe o se libere. Entonces:
   - antes de leer butacas, el grupo lee UNA sola TVar: alcanza !! (k-1) = "hay al menos k libres".
     Si es False -> retry habiendo leído solo esa TVar.
   - esa TVar se escribe solo cuando su valor CAMBIA (escribir el mismo valor también despierta).
   - mientras el grupo espera vale False; solo pasa a True cuando las libres suben de < k a >= k,
     que es exactamente el único cambio que puede permitirle sentarse.
   (Con un único contador TVar Int libres, una ocupación de otro grupo o una liberación que no
    alcanza también lo despertarían: no cumple R3 estricto.)

Si alcanza k es True, hay >= k libres, así que la búsqueda siempre encuentra lugar (contiguas o
sueltas): después de pasar el check, la transacción no vuelve a hacer retry.
```

## Código

```haskell
import Control.Concurrent
import Control.Concurrent.STM
import Control.Concurrent.Async

type Butaca = TVar Bool      -- True = ocupada
type Fila   = [Butaca]
type Sala   = [Fila]         -- de la fila más buscada a la menos buscada

data Cine = Cine Sala (TVar Int) [TVar Bool]
--               sala  libres     alcanza: el elemento k-1 dice "libres >= k"

-- ---------- creación ----------

nuevaFila :: Int -> IO Fila
nuevaFila 0 = return []
nuevaFila n = do
  b  <- newTVarIO False
  bs <- nuevaFila (n - 1)
  return (b : bs)

nuevaSala :: [Int] -> IO Sala          -- largo de cada fila, en orden de preferencia
nuevaSala []       = return []
nuevaSala (n : ns) = do
  f  <- nuevaFila n
  fs <- nuevaSala ns
  return (f : fs)

nuevasAlcanza :: Int -> IO [TVar Bool] -- al principio están todas libres: alcanza para todo k
nuevasAlcanza 0 = return []
nuevasAlcanza n = do
  t  <- newTVarIO True
  ts <- nuevasAlcanza (n - 1)
  return (t : ts)

nuevoCine :: Sala -> IO Cine
nuevoCine sala = do
  let total = sum (map length sala)
  libres  <- newTVarIO total
  alcanza <- nuevasAlcanza total
  return (Cine sala libres alcanza)

-- ---------- contador de libres (mantiene alcanza) ----------

cambiarLibres :: Cine -> Int -> STM ()
cambiarLibres (Cine _ libres alcanza) delta = do
  antes <- readTVar libres
  let despues = antes + delta
  writeTVar libres despues
  actualizar alcanza 1 antes despues

-- escribe alcanza k SOLO si cambia de valor (así no despierta a nadie de gusto)
actualizar :: [TVar Bool] -> Int -> Int -> Int -> STM ()
actualizar []       _ _     _       = return ()
actualizar (t : ts) k antes despues = do
  if (antes >= k) /= (despues >= k)
    then writeTVar t (despues >= k)
    else return ()
  actualizar ts (k + 1) antes despues

-- ---------- búsqueda (lee la sala y decide, sin escribir) ----------

leerFila :: Fila -> STM [(Butaca, Bool)]
leerFila []       = return []
leerFila (b : bs) = do
  ocupada <- readTVar b
  resto   <- leerFila bs
  return ((b, ocupada) : resto)

leerSala :: Sala -> STM [[(Butaca, Bool)]]
leerSala []       = return []
leerSala (f : fs) = do
  fila  <- leerFila f
  resto <- leerSala fs
  return (fila : resto)

-- primer bloque de k libres contiguas en una fila (de izquierda a derecha)
contiguasEnFila :: Int -> [(Butaca, Bool)] -> Maybe [Butaca]
contiguasEnFila k fila
  | length fila < k                  = Nothing
  | all (not . snd) (take k fila)    = Just (map fst (take k fila))
  | otherwise                        = contiguasEnFila k (tail fila)

-- primera fila (en orden de preferencia) que tenga un bloque
contiguas :: Int -> [[(Butaca, Bool)]] -> Maybe [Butaca]
contiguas _ []       = Nothing
contiguas k (f : fs) = case contiguasEnFila k f of
  Just bs -> Just bs
  Nothing -> contiguas k fs

-- las primeras k libres recorriendo la sala en orden de preferencia
sueltas :: Int -> [[(Butaca, Bool)]] -> [Butaca]
sueltas k filas = take k [b | (b, False) <- concat filas]

-- ---------- operaciones de un grupo ----------

ocupar :: [Butaca] -> STM ()
ocupar []       = return ()
ocupar (b : bs) = do
  writeTVar b True
  ocupar bs

desocupar :: [Butaca] -> STM ()
desocupar []       = return ()
desocupar (b : bs) = do
  writeTVar b False
  desocupar bs

tomarButacas :: Cine -> Int -> STM [Butaca]
tomarButacas cine@(Cine sala _ alcanza) k = do
  hay <- readTVar (alcanza !! (k - 1))
  check hay                              -- R3: si espero, solo leí esta TVar
  filas <- leerSala sala                 -- R2: leo la sala como está AHORA
  let elegidas = case contiguas k filas of
                   Just bs -> bs          -- 1ra opción: juntos, lo más adelante posible
                   Nothing -> sueltas k filas   -- 2da: k cualesquiera (hay >= k libres)
  ocupar elegidas                        -- R1: buscar y ocupar en la MISMA transacción
  cambiarLibres cine (-k)
  return elegidas

liberar :: Cine -> [Butaca] -> STM ()
liberar cine bs = do
  desocupar bs
  cambiarLibres cine (length bs)

-- ---------- threads ----------

grupo :: Cine -> Int -> IO ()
grupo cine k = do
  bs <- atomically (tomarButacas cine k)
  putStrLn ("grupo de " ++ show k ++ " sentado")
  threadDelay 1000000                    -- ve la película
  atomically (liberar cine bs)

lanzar :: Cine -> [Int] -> IO [Async ()]
lanzar _    []       = return []
lanzar cine (k : ks) = do
  a  <- async (grupo cine k)
  as <- lanzar cine ks
  return (a : as)

esperarTodos :: [Async ()] -> IO ()
esperarTodos []       = return ()
esperarTodos (a : as) = do
  wait a
  esperarTodos as

reservar :: [Int] -> Sala -> IO ()      -- tamaños de los grupos (1 <= k <= butacas totales)
reservar grupos sala = do
  cine <- nuevoCine sala
  hs   <- lanzar cine grupos
  esperarTodos hs

main :: IO ()
main = do
  sala <- nuevaSala [6, 6, 8, 8]
  reservar [4, 2, 3, 5, 4, 6, 1, 2, 7] sala
```

## Justificación

```
race conditions: toda lectura-decisión-escritura de butacas y del contador ocurre dentro de un mismo
   atomically (tomarButacas, liberar). STM las ejecuta aisladas: si dos chocan en una TVar, una aborta.
   Invariante: libres = cantidad de butacas en False, y alcanza !! (k-1) = (libres >= k); se
   mantienen porque se actualizan en la misma transacción que ocupa/libera.

deadlock: no hay locks. El único bloqueo es el retry de un grupo con alcanza k = False. Un grupo
   sentado siempre termina la película y libera (liberar no espera nada), así que las libres vuelven
   a subir y alcanza k pasa a True. Un grupo con k > butacas totales esperaría para siempre: se asume
   1 <= k <= total.

starvation: SÍ puede. Un grupo grande espera a que haya k libres; mientras tanto grupos chicos que
   llegan pueden ir ocupando cada lugar que se libera (cuando alcanza k pasa a True, se despiertan
   todos y gana cualquiera; retry no es FIFO). Traza: grupo de 6 esperando con 5 libres; se libera
   1 -> 6 libres, se despierta el de 6, pero antes commitea un grupo de 2 -> 4 libres, el de 6 vuelve
   a retry; y así para siempre.
```
