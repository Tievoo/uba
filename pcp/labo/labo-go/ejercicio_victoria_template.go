package main

import (
	"fmt"
	"math/rand"
	"time"
)
// En este caso usamos el mismo struct para representar pedidos de faros y carrocerias porque no hace
// falta diferenciarlos a fines de este ejercicio.
type Pedido struct {
	colaboradorID int // Se utiliza para el print en el método Victoria
	terminado     chan struct{}
}

type Taller struct {
	faros       chan Pedido
	carrocerias chan Pedido
}

func NuevoTaller() *Taller {

}

func (t *Taller) TraerFaro(colaboradorID int) {


}

func (t *Taller) TraerCarroceria(colaboradorID int) {

	// TODO
}

func armarUnidad() {
	time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond)
}

func (t *Taller) Victoria(cantidadAutos int) {
	
}
