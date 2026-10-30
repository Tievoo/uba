-- Guía 5 warm-up: Haskell, IO y mónadas
-- Abrir con:   ghci guias/guia5-warmup.hs
-- Recargar:    :r        Ver un tipo:  :t algo        Salir:  :q
--
-- Cada función arranca como `undefined`: compila, pero explota si la llamás.
-- Reemplazala por tu definición y probala en ghci.

-- Ejercicio 1 -----------------------------------------------------------

longitud :: [a] -> Int
longitud [] = 0
longitud (_:xs) = 1 + longitud xs

sumatoria :: [Int] -> Int
sumatoria [] = 0
sumatoria (x:xs) = x + sumatoria xs

pertenece :: Eq a => a -> [a] -> Bool
pertenece [] = False
pertenece x (y:ys) = x == y || pertenece x ys

-- quita solo la primera aparición
quitar :: Eq a => a -> [a] -> [a]
quitar x [] = []
quitar x (y:ys) = if x == y then ys else y : quitar x ys

-- Ejercicio 2 -----------------------------------------------------------

cuadrados :: [Int] -> [Int]
cuadrados = map (^2)

positivos :: [Int] -> [Int]
positivos = filter (> 0)

cantidad :: (a -> Bool) -> [a] -> Int
cantidad = foldr (\x acc -> if x then acc + 1 else acc) 0

-- Ejercicio 3 -----------------------------------------------------------

data Arbol a = Hoja | Nodo (Arbol a) a (Arbol a)
  deriving Show

insertar :: Ord a => a -> Arbol a -> Arbol a
insertar Hoja x = Nodo Hoja x Hoja
insertar (Nodo izq val der) x
  | x < val   = Nodo (insertar izq x) val der
  | x > val   = Nodo izq val (insertar der x)
  | otherwise = Nodo izq val der  -- no insertamos duplicados

estaEn :: Ord a => a -> Arbol a -> Bool
estaEn Hoja _ = False
estaEn (Nodo izq val der) x 
  | x < val   = estaEn izq x
  | x > val   = estaEn der x
  | otherwise = True

enOrden :: Arbol a -> [a]
enOrden Hoja = []
enOrden (Nodo izq val der) = enOrden izq ++ [val] ++ enOrden der

desdeLista :: Ord a => [a] -> Arbol a
desdeLista = foldr insertar Hoja

-- Ejercicio 4 -----------------------------------------------------------

safeHead :: [a] -> Maybe a
safeHead [] = Nothing
safeHead (x:_) = Just x

buscar :: Eq k => k -> [(k, v)] -> Maybe v
buscar x [] = Nothing
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

calcular :: Int -> Int -> Int -> Maybe Int
calcular a b c = do
  x <- dividir a b
  dividir x c

-- version 2
-- calcular a b c = dividir a b >>= \x -> dividir x c

-- version 3
-- calcular a b c = case dividir a b of
--   Nothing -> Nothing
--   Just x  -> dividir x c

transferir :: Int -> Cuenta -> Cuenta -> Maybe (Cuenta, Cuenta)
transferir = undefined

-- Ejercicio 7 -----------------------------------------------------------
-- Los nombres llevan ' para no chocar con los de la biblioteca.

when' :: Monad m => Bool -> m () -> m ()
when' = undefined

replicateM_' :: Monad m => Int -> m a -> m ()
replicateM_' = undefined

mapM' :: Monad m => (a -> m b) -> [a] -> m [b]
mapM' = undefined

forM_' :: Monad m => [a] -> (a -> m b) -> m ()
forM_' = undefined

forever' :: Monad m => m a -> m b
forever' = undefined

-- Ejercicio 8 -----------------------------------------------------------

saludar :: IO ()
saludar = undefined

sumarHastaCero :: IO Int
sumarHastaCero = undefined

-- Ejercicio 9 -----------------------------------------------------------

hola :: IO ()
hola = putStrLn "hola"

repetir :: Int -> IO () -> IO ()
repetir = undefined

-- Ejercicio 10 ----------------------------------------------------------

adivinar :: Int -> IO ()
adivinar = undefined

main :: IO ()
main = saludar
