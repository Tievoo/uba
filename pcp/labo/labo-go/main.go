package main

import (
	"fmt"
	"math/rand"
	"time"
)

const (
	CANT_COLABORADORES_FAROS       = 6
	CANT_COLABORADORES_CARROCERIAS = 7
	CANT_AUTOS                     = 15
)

func main() {
	fmt.Printf("Colaboradores de faros: %d\n", CANT_COLABORADORES_FAROS)
	fmt.Printf("Colaboradores de carrocerias: %d\n", CANT_COLABORADORES_CARROCERIAS)
	fmt.Printf("Autos a construir: %d\n\n", CANT_AUTOS)

	taller := NuevoTaller()

	for id := 1; id <= CANT_COLABORADORES_FAROS; id++ {
		go colaboradorFaro(taller, id)
	}

	for id := 1; id <= CANT_COLABORADORES_CARROCERIAS; id++ {
		go colaboradorCarroceria(taller, id)
	}

	taller.Victoria(CANT_AUTOS)
}

func colaboradorFaro(taller *Taller, id int) {
	for {
		taller.TraerFaro(id)
		time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond)
	}
}

func colaboradorCarroceria(taller *Taller, id int) {
	for {
		taller.TraerCarroceria(id)
		time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond)
	}
}
