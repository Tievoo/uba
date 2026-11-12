# Guía 5 — STM

Enunciado: `guia5.pdf`. Resumen: `../../knowledge/resumenes/05-stm.md` (secciones 10 y 11 = receta + mapa de ejercicios).

## Ejercicio 1 — Buffer de capacidad 1
### a) No bloqueante

```haskell
get :: TVar (Maybe t) -> STM (Maybe t)
get buf = do
  m <- readTVar buf
  case m of
    Nothing -> return Nothing        -- vacío: no hay nada para tomar
    Just x  -> do
      writeTVar buf Nothing          -- lo tomo: el buffer queda vacío
      return (Just x)

put :: TVar (Maybe t) -> t -> STM Bool
put buf v = do
  m <- readTVar buf
  case m of
    Nothing -> do
      writeTVar buf (Just v)         -- vacío: lo lleno
      return True
    Just _  -> return False          -- lleno: no piso lo que hay
```

### b) Programa: put 1 y get concurrentes

```haskell
import Control.Concurrent.STM
import Control.Concurrent.Async

main :: IO ()
main = do
  buf <- newTVarIO (Just 0)                         -- buffer con valor inicial 0
  escritor <- async (atomically (put buf 1))        -- thread que escribe 1
  lector   <- async (atomically (get buf))          -- thread que lee
  _ <- wait escritor
  resultado <- wait lector
  print resultado
```

### c) Bloqueante

```haskell
import Data.Maybe (isJust, isNothing, fromJust)

get :: TVar (Maybe b) -> STM b
get buf = do
  m <- readTVar buf
  check (isJust m)              -- espero a que esté lleno
  writeTVar buf Nothing         -- lo tomo
  return (fromJust m)           -- saco el valor del Just

put :: TVar (Maybe t) -> t -> STM ()
put buf v = do
  m <- readTVar buf
  check (isNothing m)           -- espero a que esté vacío
  writeTVar buf (Just v)        -- ya es STM (): no hace falta return
```

### d) read sin tomar

```haskell
-- se llama read en el enunciado, pero choca con read del Prelude
leer :: TVar (Maybe b) -> STM b
leer buf = do
  m <- readTVar buf
  check (isJust m)              -- espero a que esté lleno
  return (fromJust m)           -- no escribo: el valor queda en el buffer
```

## Ejercicio 2 — Semáforo con STM

```haskell
type Semaforo = TVar Int

nuevoSemaforo :: Int -> IO Semaforo
nuevoSemaforo n = newTVarIO n          -- en main: sem <- nuevoSemaforo 3

acquire :: Semaforo -> STM ()
acquire sem = do
  x <- readTVar sem
  check (x > 0)                        -- espero a que haya permisos
  writeTVar sem (x - 1)

release :: Semaforo -> STM ()
release sem = modifyTVar' sem (+1)

-- cliente que toma dos permisos atómicamente
cliente :: Semaforo -> IO ()
cliente sem = do
  atomically (do                       -- un solo atomically: o toma los dos, o ninguno
    acquire sem
    acquire sem)
  usarRecurso
  atomically (do
    release sem
    release sem)
```

## Ejercicio 3 — Juego de las bolitas

```haskell
data Juego = Juego { bolsa :: TVar Int, generadores :: TVar Int }
-- invariante: bolsa <= generadores

nuevoJuego :: IO Juego
nuevoJuego = do
  b <- newTVarIO 0
  g <- newTVarIO 0
  return (Juego b g)

entrarGenerador :: Juego -> STM ()
entrarGenerador j = modifyTVar' (generadores j) (+1)

salirGenerador :: Juego -> STM ()
salirGenerador j = do
  b <- readTVar (bolsa j)
  g <- readTVar (generadores j)
  check (b < g)                        -- al irme quedan g-1: necesito b <= g-1
  writeTVar (generadores j) (g - 1)

generar :: Juego -> STM ()
generar j = do
  b <- readTVar (bolsa j)
  g <- readTVar (generadores j)
  check (b < g)                        -- con una bolita más sigue b <= g
  writeTVar (bolsa j) (b + 1)

consumir :: Juego -> STM ()
consumir j = do
  b <- readTVar (bolsa j)
  check (b >= 2)
  writeTVar (bolsa j) (b - 2)
```

## Ejercicio 4 — Fumadores

```haskell
data Ingrediente = Tabaco | Papel | Fosforos
  deriving Eq

-- la mesa guarda qué ingrediente FALTA (= los otros dos están puestos)
-- Nothing = mesa vacía
type Mesa = TVar (Maybe Ingrediente)

tomar :: Ingrediente -> Mesa -> STM ()
tomar mio mesa = do
  m <- readTVar mesa
  check (m == Just mio)                -- falta justo el mío: están los dos que necesito
  writeTVar mesa Nothing               -- los saco en la misma transacción

poner :: Ingrediente -> Mesa -> STM ()
poner falta mesa = do
  m <- readTVar mesa
  check (m == Nothing)                 -- espero a que la mesa esté vacía
  writeTVar mesa (Just falta)          -- pongo los otros dos

fumador :: Ingrediente -> Mesa -> IO ()
fumador mio mesa = do
  atomically (tomar mio mesa)
  -- fumar (afuera de la transacción)
  fumador mio mesa

proveedor :: Mesa -> [Ingrediente] -> IO ()
proveedor mesa []     = proveedor mesa [Tabaco, Papel, Fosforos]   -- vuelvo a empezar
proveedor mesa (i:is) = do
  atomically (poner i mesa)
  proveedor mesa is

main :: IO ()
main = do
  mesa <- newTVarIO Nothing
  _ <- async (fumador Tabaco mesa)
  _ <- async (fumador Papel mesa)
  _ <- async (fumador Fosforos mesa)
  p <- async (proveedor mesa [])
  wait p                               -- el proveedor no termina nunca
```

## Ejercicio 5 — Pizzería

```haskell
data Barra = Barra { grandes :: TVar Int, chicas :: TVar Int }
-- Barra ya tiene TVars adentro: se pasa Barra, no TVar Barra

data Tamanio = Grande | Chica

hacerPizza :: Tamanio -> Barra -> STM ()
hacerPizza Grande barra = modifyTVar' (grandes barra) (+1)
hacerPizza Chica  barra = modifyTVar' (chicas barra) (+1)

tomarGrande :: Barra -> STM ()
tomarGrande barra = do
  g <- readTVar (grandes barra)
  check (g >= 1)                       -- si no hay grande: retry → el orElse prueba la otra
  writeTVar (grandes barra) (g - 1)

tomarDosChicas :: Barra -> STM ()
tomarDosChicas barra = do
  c <- readTVar (chicas barra)
  check (c >= 2)                       -- si tampoco: retry de todo, el cliente duerme
  writeTVar (chicas barra) (c - 2)

cliente :: Barra -> STM ()
cliente barra = tomarGrande barra `orElse` tomarDosChicas barra
```

## Ejercicio 6 — Pila concurrente

```haskell
type Pila a = TVar [a]                 -- la cabeza de la lista es el tope

nuevaPila :: IO (Pila a)
nuevaPila = newTVarIO []

push :: Pila a -> a -> STM ()
push pila x = modifyTVar' pila (x :)   -- (x :) = "agregá x adelante"

pop :: Pila a -> STM a
pop pila = do
  xs <- readTVar pila
  check (not (null xs))                -- espero a que haya tope
  writeTVar pila (tail xs)             -- saco el tope
  return (head xs)
```

## Ejercicio 7 — Cola
### a) encolar / desencolar / desencolarSi

```haskell
data Cola a = Cola (TVar [a])          -- sin llaves: la TVar se saca con pattern matching

encolar :: Cola a -> a -> STM ()
encolar (Cola t) x = modifyTVar' t (++ [x])   -- al fondo

desencolar :: Cola a -> STM a
desencolar (Cola t) = do
  xs <- readTVar t
  check (not (null xs))                -- espero a que haya algo
  writeTVar t (tail xs)
  return (head xs)

desencolarSi :: Cola a -> STM (Maybe a)
desencolarSi (Cola t) = do
  xs <- readTVar t
  case xs of
    []     -> return Nothing           -- vacía: no espero, aviso
    (y:ys) -> do
      writeTVar t ys
      return (Just y)
```

### b) encolarDesencolar

```haskell
encolarDesencolar :: Cola a -> Cola a -> IO ()
encolarDesencolar c1 c2 = atomically (do
  x <- desencolar c1                   -- si c1 está vacía: retry, no queda nada a medias
  encolar c2 x)
```
### c) Cola con prioridad

```haskell
data Prioridad = Alta | Media | Baja
data ColaPrioridad a = ColaPrioridad (Cola a) (Cola a) (Cola a)   -- alta, media, baja

encolarP :: ColaPrioridad a -> a -> Prioridad -> STM ()
encolarP (ColaPrioridad alta _ _)  x Alta  = encolar alta x
encolarP (ColaPrioridad _ media _) x Media = encolar media x
encolarP (ColaPrioridad _ _ baja)  x Baja  = encolar baja x

desencolarP :: ColaPrioridad a -> STM a
desencolarP (ColaPrioridad alta media baja) =
  desencolar alta `orElse` desencolar media `orElse` desencolar baja
  -- si las tres están vacías: retry, duerme hasta que encolen en cualquiera
```

## Ejercicio 8 — RWLock (resuelto por Claude)
### a)

```haskell
data RWLock = RWLock (TVar Int) (TVar Bool)   -- cantidad de lectores, hay escritor

newRWLock :: IO RWLock
newRWLock = do
  varLectores <- newTVarIO 0
  flagEscritor <- newTVarIO False
  return (RWLock varLectores flagEscritor)

lockLectura :: RWLock -> STM ()
lockLectura (RWLock lectores escritor) = do
  e <- readTVar escritor
  check (not e)                        -- espero a que no haya escritor
  n <- readTVar lectores
  writeTVar lectores (n + 1)

unlockLectura :: RWLock -> STM ()
unlockLectura (RWLock lectores _) = do
  n <- readTVar lectores
  writeTVar lectores (n - 1)

lockEscritura :: RWLock -> STM ()
lockEscritura (RWLock lectores escritor) = do
  e <- readTVar escritor
  n <- readTVar lectores
  check (not e && n == 0)              -- espero a que no haya nadie
  writeTVar escritor True

unlockEscritura :: RWLock -> STM ()
unlockEscritura (RWLock _ escritor) = writeTVar escritor False

lector :: RWLock -> IO ()
lector rw = do
  atomically (lockLectura rw)
  -- leer (afuera de la transacción)
  atomically (unlockLectura rw)
-- ojo: si siempre hay lectores, un escritor puede esperar para siempre (inanición)
```

### b) Máximo de lectores

```haskell
data RWLock = RWLock (TVar Int) (TVar Bool) Int   -- + máximo de lectores (fijo)

newRWLock :: Int -> IO RWLock
newRWLock maximo = do
  varLectores <- newTVarIO 0
  flagEscritor <- newTVarIO False
  return (RWLock varLectores flagEscritor maximo)

lockLectura :: RWLock -> STM ()
lockLectura (RWLock lectores escritor maximo) = do
  e <- readTVar escritor
  n <- readTVar lectores
  check (not e && n < maximo)          -- además, espero a que haya lugar
  writeTVar lectores (n + 1)

-- unlockLectura, lockEscritura y unlockEscritura: iguales al a),
-- con un _ más en el pattern matching por el campo nuevo
```

## Ejercicio 9 — Filósofos (resuelto por Claude)

```haskell
-- tenedor = buffer del Ej 1c: Just () = libre (lleno), Nothing = lo tiene alguien
type Tenedor = TVar (Maybe ())

tomarTenedores :: Tenedor -> Tenedor -> STM ()
tomarTenedores izq der = do
  get izq                              -- get bloqueante del 1c
  get der                              -- si el segundo no está: retry, se suelta el primero

soltarTenedores :: Tenedor -> Tenedor -> STM ()
soltarTenedores izq der = do
  put izq ()                           -- put del 1c
  put der ()

filosofo :: Tenedor -> Tenedor -> IO ()
filosofo izq der = do
  -- pensar
  atomically (tomarTenedores izq der)  -- los dos juntos: no hay deadlock
  -- comer
  atomically (soltarTenedores izq der)
  filosofo izq der

main :: IO ()
main = do
  tenedores <- mapM (\_ -> newTVarIO (Just ())) [1..5]
  hilos <- mapM (\i -> async (filosofo (tenedores !! i) (tenedores !! ((i + 1) `mod` 5)))) [0..4]
  mapM_ wait hilos
-- sin deadlock (se toman atómicamente), pero puede haber inanición
```
