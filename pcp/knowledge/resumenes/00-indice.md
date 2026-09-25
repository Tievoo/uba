# Resúmenes PCP — Índice

La materia tiene **4 temas**. Cada uno tiene una teórica, una práctica, una guía y (a veces) un labo, y cada uno corresponde a **un ejercicio del parcial**.

| # | Tema | Teórica | Práctica | Guía | Labo | Ej. del parcial |
|---|------|---------|----------|------|------|-----------------|
| 1 | Modelo de cómputo, exclusión mutua, modelo de memoria | 01-Mutex | clase-01 | Guía 1 | — | Ej 1 |
| 2 | Semáforos | 02-Semaforos | practica-clase-02 | Guía 2 | Labo 1 | Ej 2 |
| 3 | Monitores | 03-Monitores | clase-3-apunte | Guía 3 | — | Ej 3 |
| 4 | Estructuras concurrentes y lock-free | 04-Listas, 05-colas | clase-04 | Guía 4 | Labo 3 | Ej 4 |

## Orden de lectura sugerido
1. `01-exclusion-mutua.md` → después, la práctica 1 completa.
2. `02-semaforos.md` → práctica 2 + labo 1 (**prioridad alta**).
3. `03-monitores.md` → apunte de la práctica 3 (**prioridad alta**; está escrito como una clase y se lee muy bien).
4. `04-estructuras.md` → práctica 4 + teóricas 4 y 5.
5. `../patrones-parcial.md` → el "machete" para ejercitar con el simulacro.

## Idea general de la materia, en un párrafo
Hay varios **threads** (hilos) que corren "a la vez" y comparten memoria. El problema: si dos tocan la misma variable al mismo tiempo, pasan cosas raras (se pierden sumas, dos entran a donde debía entrar uno solo, alguien espera para siempre). La materia es una escalera de herramientas para evitarlo:

1. **Solo con leer y escribir variables** (algoritmos tipo Peterson): se puede, pero es difícil y gasta CPU esperando (*busy-waiting*).
2. **Semáforos**: un contador de permisos que el sistema operativo maneja. Si no hay permiso, te duerme.
3. **Monitores**: un objeto que garantiza solo, sin que lo escribas, que un único thread a la vez ejecuta sus métodos, y además te deja esperar hasta que se cumpla una condición.
4. **Estructuras de datos concurrentes**: listas y colas que muchos threads pueden usar a la vez, con locks más finos o **sin locks** (usando la instrucción atómica CAS).

Lo que siempre se evalúa:
- **Safety** ("nunca pasa algo malo"): exclusión mutua, no hay race conditions, la estructura es correcta (linealizable).
- **Liveness** ("algo bueno termina pasando"): no hay deadlock y nadie espera para siempre (no hay inanición).
