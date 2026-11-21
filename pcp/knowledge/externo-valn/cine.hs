import Control.Concurrent.STM
import Control.Monad

type Butaca = TVar Bool -- False = libre, True = ocupada

type Fila = [Butaca]

type Sala = [Fila]

-- crearSala {cantidad de filas} {butacas por fila}
crearSala :: Int -> Int -> IO Sala
crearSala cantFilas butacasPorFila =
  replicateM cantFilas (replicateM butacasPorFila (newTVarIO False))

-- reservar {cantidad de integrantes del grupo} {sala}
reservar :: Int -> Sala -> IO ()
reservar k sala = do
  atomically (orElse (reservarContiguas k sala) (reservarSeparadas k sala))

-- reservar {cantidad de integrantes del grupo} {sala}
reservarContiguas :: Int -> Sala -> STM ()
reservarContiguas _ [] = retry
reservarContiguas k (fila : filas) =
  orElse (reservarContiguasEnFila k fila) (reservarContiguas k filas)

-- reservar {cantidad de integrantes del grupo} {fila}
reservarContiguasEnFila :: Int -> Fila -> STM ()
reservarContiguasEnFila _ [] = retry
reservarContiguasEnFila k fila
  | k > length fila = retry
  | otherwise = orElse (reservarButacasContiguas (take k fila)) (reservarContiguasEnFila k (drop 1 fila))

-- reservar {cantidad de integrantes del grupo} {subfila}
reservarButacasContiguas :: [Butaca] -> STM ()
reservarButacasContiguas [] = return ()
reservarButacasContiguas (butacaTVar : butacas) = do
  butaca <- readTVar butacaTVar
  check (estáLibre butaca)
  writeTVar butacaTVar True
  reservarButacasContiguas butacas
  where
    estáLibre :: Bool -> Bool
    estáLibre butaca = not butaca

-- reservar {cantidad de integrantes del grupo} {sala}
reservarSeparadas :: Int -> Sala -> STM ()
reservarSeparadas 0 _ = return ()
reservarSeparadas _ [] = retry
reservarSeparadas k (fila : filas) = do
  butacasReservadas <- reservarButacasSeparadas k fila
  reservarSeparadas (k - butacasReservadas) filas

-- reservar {cantidad de integrantes del grupo} {fila}
-- devuelve la cantidad de butacas que asignó exitosamente
reservarButacasSeparadas :: Int -> Fila -> STM Int
reservarButacasSeparadas 0 _ = return 0
reservarButacasSeparadas _ [] = return 0
reservarButacasSeparadas k (butacaTVar : butacas) = do
  butaca <- readTVar butacaTVar
  if (estáLibre butaca)
    then do
      writeTVar butacaTVar True
      cantButacasAsignadas <- reservarButacasSeparadas (k - 1) butacas
      return (cantButacasAsignadas + 1)
    else
      reservarButacasSeparadas k butacas
  where
    estáLibre :: Bool -> Bool
    estáLibre butaca = not butaca
