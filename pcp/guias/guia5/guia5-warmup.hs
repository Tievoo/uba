-- Guía 5 warm-up: Haskell, IO y mónadas
-- Abrir con:   ghci pcp/guias/guia5/guia5-warmup.hs
-- Recargar:    :r        Ver un tipo:  :t algo        Salir:  :q
-- Correr main: runghc pcp/guias/guia5/guia5-warmup.hs

-- Ejercicio 1 -----------------------------------------------------------

longitud :: [a] -> Int
longitud [] = 0
longitud (_:xs) = 1 + longitud xs

sumatoria :: [Int] -> Int
sumatoria [] = 0
sumatoria (x:xs) = x + sumatoria xs

-- (fix: todas las ecuaciones tienen que tener la misma cantidad de argumentos)
pertenece :: Eq a => a -> [a] -> Bool
pertenece _ [] = False
pertenece x (y:ys) = x == y || pertenece x ys

-- quita solo la primera aparición
quitar :: Eq a => a -> [a] -> [a]
quitar _ [] = []
quitar x (y:ys) = if x == y then ys else y : quitar x ys

-- Ejercicio 2 -----------------------------------------------------------

cuadrados :: [Int] -> [Int]
cuadrados = map (^2)

positivos :: [Int] -> [Int]
positivos = filter (> 0)

-- (fix: hay que aplicar el predicado p al elemento, x no es un Bool)
cantidad :: (a -> Bool) -> [a] -> Int
cantidad p = foldr (\x acc -> if p x then acc + 1 else acc) 0

-- Ejercicio 3 -----------------------------------------------------------

data Arbol a = Hoja | Nodo (Arbol a) a (Arbol a)
  deriving Show

-- (fix: la firma dice elemento primero, árbol después)
insertar :: Ord a => a -> Arbol a -> Arbol a
insertar x Hoja = Nodo Hoja x Hoja
insertar x (Nodo izq val der)
  | x < val   = Nodo (insertar x izq) val der
  | x > val   = Nodo izq val (insertar x der)
  | otherwise = Nodo izq val der  -- no insertamos duplicados

estaEn :: Ord a => a -> Arbol a -> Bool
estaEn _ Hoja = False
estaEn x (Nodo izq val der)
  | x < val   = estaEn x izq
  | x > val   = estaEn x der
  | otherwise = True

enOrden :: Arbol a -> [a]
enOrden Hoja = []
enOrden (Nodo izq val der) = enOrden izq ++ [val] ++ enOrden der

-- foldr :: (a -> b -> b) -> b -> [a] -> b, con b = Arbol a: insertar encaja justo
desdeLista :: Ord a => [a] -> Arbol a
desdeLista = foldr insertar Hoja

-- Ejercicio 4 -----------------------------------------------------------

safeHead :: [a] -> Maybe a
safeHead [] = Nothing
safeHead (x:_) = Just x

buscar :: Eq k => k -> [(k, v)] -> Maybe v
buscar _ [] = Nothing
buscar x ((k,v):xs) = if x == k then Just v else buscar x xs

dividir :: Int -> Int -> Maybe Int
dividir _ 0 = Nothing
dividir x y = Just (x `div` y)

data Cuenta = Cuenta { titular :: String, saldo :: Int }
  deriving Show

depositar :: Int -> Cuenta -> Cuenta
depositar cantidad cuenta = cuenta { saldo = saldo cuenta + cantidad }

extraer :: Int -> Cuenta -> Maybe Cuenta
extraer x c
  | x <= saldo c = Just (c { saldo = saldo c - x })
  | otherwise    = Nothing

-- Ejercicio 5 -----------------------------------------------------------

-- a) (a / b) / c + 1, tres versiones

-- con do
calcular :: Int -> Int -> Int -> Maybe Int
calcular a b c = do
  x <- dividir a b
  y <- dividir x c
  return (y + 1)

-- con >>=
calcular2 :: Int -> Int -> Int -> Maybe Int
calcular2 a b c = dividir a b >>= \x -> dividir x c >>= \y -> return (y + 1)

-- con case
calcular3 :: Int -> Int -> Int -> Maybe Int
calcular3 a b c = case dividir a b of
  Nothing -> Nothing
  Just x  -> case dividir x c of
    Nothing -> Nothing
    Just y  -> Just (y + 1)

-- b) si extraer falla, todo el do da Nothing. depositar no puede fallar,
--    así que va directo en el return (no lleva <-).
transferir :: Int -> Cuenta -> Cuenta -> Maybe (Cuenta, Cuenta)
transferir monto origen destino = do
  origen' <- extraer monto origen
  return (origen', depositar monto destino)

-- c) Either String: Left "error" en lugar de Nothing, Right v en lugar de Just v
dividirE :: Int -> Int -> Either String Int
dividirE _ 0 = Left "división por cero"
dividirE x y = Right (x `div` y)

extraerE :: Int -> Cuenta -> Either String Cuenta
extraerE x c
  | x <= saldo c = Right (c { saldo = saldo c - x })
  | otherwise    = Left ("saldo insuficiente en la cuenta de " ++ titular c)

-- ¿Cuánto cambia transferir? Nada: solo el tipo y el nombre de extraer.
-- El do es idéntico porque Either String también es una mónada.
transferirE :: Int -> Cuenta -> Cuenta -> Either String (Cuenta, Cuenta)
transferirE monto origen destino = do
  origen' <- extraerE monto origen
  return (origen', depositar monto destino)

-- Ejercicio 6 -----------------------------------------------------------
-- En la mónada lista, x <- xs significa "para cada x de xs" (un for anidado),
-- y return v es [v]. Devolver [] descarta esa rama.

pares :: [a] -> [b] -> [(a, b)]
pares xs ys = do
  x <- xs
  y <- ys
  return (x, y)

pitagoricas :: Int -> [(Int, Int, Int)]
pitagoricas n = do
  a <- [1..n]
  b <- [a..n]
  c <- [b..n]
  if a*a + b*b == c*c then return (a, b, c) else []

-- Ejercicio 7 -----------------------------------------------------------
-- Los nombres llevan ' para no chocar con los de la biblioteca.
-- Solo podemos usar return, >>= / >> y do: tienen que andar para cualquier mónada.

when' :: Monad m => Bool -> m () -> m ()
when' c accion = if c then accion else return ()

replicateM_' :: Monad m => Int -> m a -> m ()
replicateM_' n accion
  | n <= 0    = return ()
  | otherwise = accion >> replicateM_' (n - 1) accion

mapM' :: Monad m => (a -> m b) -> [a] -> m [b]
mapM' _ [] = return []
mapM' f (x:xs) = do
  y  <- f x
  ys <- mapM' f xs
  return (y : ys)
-- mapM' (dividir 100) [1, 0, 5] == Nothing
-- (dividir 100 0 da Nothing y en Maybe un Nothing corta toda la cadena)

forM_' :: Monad m => [a] -> (a -> m b) -> m ()
forM_' [] _ = return ()
forM_' (x:xs) f = f x >> forM_' xs f

forever' :: Monad m => m a -> m b
forever' accion = accion >> forever' accion
-- forever' Nothing == Nothing: Nothing >> _ = Nothing, así que corta
-- en el primer paso y no se cuelga (por evaluación perezosa nunca mira el resto).
-- forever' (Just 1) sí se cuelga.

-- Ejercicio 8 -----------------------------------------------------------

saludar :: IO ()
saludar = do
  putStrLn "¿Cómo te llamás?"
  nombre <- getLine
  putStrLn ("Hola, " ++ nombre ++ "!")

-- readLn = getLine + read; el tipo (Int) lo infiere de la firma
sumarHastaCero :: IO Int
sumarHastaCero = do
  n <- readLn
  if n == 0
    then return 0
    else do
      resto <- sumarHastaCero
      return (n + resto)

mainSumar :: IO ()
mainSumar = do
  putStrLn "Ingresá números, uno por línea (0 para terminar):"
  total <- sumarHastaCero
  putStrLn ("Suma: " ++ show total)

-- Ejercicio 9 -----------------------------------------------------------

hola :: IO ()
hola = putStrLn "hola"

-- a) Clave: una IO es una *descripción* de un efecto; let solo le pone nombre,
--    no la ejecuta. Se ejecuta cuando aparece como paso del do.
--
-- programa1 imprime:  chau
--   let x = hola nombra la acción pero x nunca se usa como paso → no corre.
--
-- programa2 imprime:  hola / hola
--   x aparece dos veces como paso del do → la acción corre dos veces.
--
-- programa3 imprime:  5
--   return 10 no corta nada (no es el return de C/Java): crea una acción
--   que "devuelve" 10, y ese 10 se descarta. n sigue valiendo 5.
--
-- programa4 imprime:  c / a
--   La lista guarda 3 acciones sin ejecutar. as !! 2 es putStrLn "c" y
--   head as es putStrLn "a"; se ejecutan solo esas dos, en ese orden.

-- b)
repetir :: Int -> IO () -> IO ()
repetir n accion
  | n <= 0    = return ()
  | otherwise = do
      accion
      repetir (n - 1) accion

-- Ejercicio 10 ----------------------------------------------------------

adivinar :: Int -> IO ()
adivinar secreto = intentar 1
  where
    intentar :: Int -> IO ()
    intentar k = do
      putStrLn "Adiviná el número:"
      intento <- readLn
      case compare secreto intento of
        GT -> do
          putStrLn "El secreto es más alto"
          intentar (k + 1)
        LT -> do
          putStrLn "El secreto es más bajo"
          intentar (k + 1)
        EQ -> putStrLn ("¡Correcto! Te llevó " ++ show k ++ " intento(s)")

mainAdivinar :: IO ()
mainAdivinar = adivinar 42

main :: IO ()
main = do
  saludar
  mainSumar
  mainAdivinar
