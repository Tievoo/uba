## Ejercicio 5

Copio esto aca para mi propia conveniencia

1, 2, 3, 4, 2, 1, 5, 6, 2, 1, 2, 3, 7, 6, 3, 2, 1, 2, 3, 6

Esta consigna es absolutamente delirante porque implica escribir casos para 1 a 7 frames para 3 algoritmos distintos, cuestión que tendría que armar 21 tablitas, y a mi no me rompan las pelotas. asumo que tenemos 5 frames y procedo.

### a) LRU
| It  | Pedido  | PF/H   | F1  | F2  | F3  | F4  | F5  | LRU |
|---- |-------- |------  |---- |---- |---- |---- |---- |---- |
|  1  |   1     |   PF   |  1  | -   |  -  |  -  |  -  | 1   |
|  2  |   2     |   PF   |  1  |  2  |  -  |  -  |  -  | 1   |
|  3  |   3     |   PF   |  1  |  2  |  3  |  -  |  -  | 1   |
|  4  |   4     |   PF   |  1  |  2  |  3  |  4  |  -  | 1   |
|  5  |   2     |   H    |  1  |  2  |  3  |  4  |  -  | 1   |
|  6  |   1     |   H    |  1  |  2  |  3  |  4  |  -  | 3   |
|  7  |   5     |  PF    |  1  |  2  |  3  |  4  |  5  | 3   |
|  8  |   6     |  PF    |  1  |  2  |  6  |  4  |  5  | 4   |
|  9  |   2     |  H     |  1  |  2  |  6  |  4  |  5  | 4   |
| 10  |   1     |  H     |  1  |  2  |  6  |  4  |  5  | 4   |
| 11  |   2     |  H     |  1  |  2  |  6  |  4  |  5  | 4   |
| 12  |   3     |  PF    |  1  |  2  |  6  |  3  |  5  | 5   |
| 13  |   7     |  PF    |  1  |  2  |  6  |  3  |  7  | 6   |
| 14  |   6     |  H     |  1  |  2  |  6  |  3  |  7  | 1   |
| 15  |   3     |  H     |  1  |  2  |  6  |  3  |  7  | 1   |
| 16  |   2     |  H     |  1  |  2  |  6  |  3  |  7  | 1   |
| 17  |   1     |  H     |  1  |  2  |  6  |  3  |  7  | 7   |
| 18  |   2     |  H     |  1  |  2  |  6  |  3  |  7  | 7   |
| 19  |   3     |  H     |  1  |  2  |  6  |  3  |  7  | 7   |
| 20  |   6     |  H     |  1  |  2  |  6  |  3  |  7  | 7   |

8 pf's
me voy a batar

### b) FIFO
| It  | Pedido  | PF/H   | F1  | F2  | F3  | F4  | F5  |FIFO |
|---- |-------- |------  |---- |---- |---- |---- |---- |---- |
|  1  |   1     |   PF   |  1  | -   |  -  |  -  |  -  | 1   |
|  2  |   2     |   PF   |  1  |  2  |  -  |  -  |  -  | 1   |
|  3  |   3     |   PF   |  1  |  2  |  3  |  -  |  -  | 1   |
|  4  |   4     |   PF   |  1  |  2  |  3  |  4  |  -  | 1   |
|  5  |   2     |   H    |  1  |  2  |  3  |  4  |  -  | 1   |
|  6  |   1     |   H    |  1  |  2  |  3  |  4  |  -  | 1   |
|  7  |   5     |  PF    |  1  |  2  |  3  |  4  |  5  | 1   |
|  8  |   6     |  PF    |  6  |  2  |  3  |  4  |  5  | 2   |
|  9  |   2     |  H     |  6  |  2  |  3  |  4  |  5  | 2   |
| 10  |   1     |  PF    |  6  |  1  |  3  |  4  |  5  | 3   |
| 11  |   2     |  PF    |  6  |  1  |  2  |  4  |  5  | 4   |
| 12  |   3     |  PF    |  6  |  1  |  2  |  3  |  5  | 5   |
| 13  |   7     |  PF    |  6  |  1  |  2  |  3  |  7  | 6   |
| 14  |   6     |  H     |  6  |  1  |  2  |  3  |  7  | 6   |
| 15  |   3     |  H     |  6  |  1  |  2  |  3  |  7  | 6   |
| 16  |   2     |  H     |  6  |  1  |  2  |  3  |  7  | 6   |
| 17  |   1     |  H     |  6  |  1  |  2  |  3  |  7  | 6   |
| 18  |   2     |  H     |  6  |  1  |  2  |  3  |  7  | 6   |
| 19  |   3     |  H     |  6  |  1  |  2  |  3  |  7  | 6   |
| 19  |   6     |  H     |  6  |  1  |  2  |  3  |  7  | 6   |

10 pf's
seguiremos informando

1, 2, 3, 4, 2, 1, 5, 6, 2, 1, 2, 3, 7, 6, 3, 2, 1, 2, 3, 6


### c) Second chance
| It  | Pedido  | PF/H   | F1  | F2  | F3  | F4  | F5  |R-Queue   |
|---- |-------- |------  |---- |---- |---- |---- |---- |----      |
|  1  |   1     | PF     | 1   | -   | -   |    -|    -|1         |
|  2  |   2     | PF     | 1   | 2   |  -  | -   |-    |1,2       |
|  3  |   3     | PF     | 1   | 2   |  3  |    -|-    |1,2,3     |
|  4  |   4     | PF     | 1   | 2   |  3  |    4|-    |1,2,3,4   |
|  5  |   2     | H      | 1   | 2   | 3   | 4   | -   |1,(2),3,4 |
|  6  |   1     | H      | 1   | 2   | 3   | 4   | -   |(1),(2),3,4 |
| 7   |   5     | PF     | 1   | 2   | 3   | 4   | 5   |(1),(2),3,4,5 |
| 8   |   6     | PF     | 1   | 2   | 6   | 4   | 5   | 4,5,1,2,6 |
| 9   |   2     | H      | 1   | 2   | 6   | 4   | 5   | 4,5,1,(2),6 |
| 10  |   1     | H      | 1   | 2   | 6   | 4   | 5   | 4,5,(1),(2),6 |
| 11  |   2     | H      | 1   | 2   | 6   | 4   | 5   | 4,5,(1),(2),6 |
| 12  |   3     | PF     | 1   | 2   | 6   | 3   | 5   | 5,(1),(2),6, 3 |
| 13  |   7     | PF     | 1   | 2   | 6   | 3   | 7   | (1),(2),6, 3, 7 |
| 14  |   6     | H      | 1   | 2   | 6   | 3   | 7   | (1),(2),(6), 3, 7 |
| 15  |   3     | H      | 1   | 2   | 6   | 3   | 7   | (1),(2),(6), (3), 7 |
| 16  |   2     | H      | 1   | 2   | 6   | 3   | 7   | (1),(2),(6), (3), 7 |
| 17  |   1     | H      | 1   | 2   | 6   | 3   | 7   | (1),(2),(6), (3), 7 |
| 18  |   2     | H      | 1   | 2   | 6   | 3   | 7   | (1),(2),(6), (3), 7 |
| 19  |   3     | H      | 1   | 2   | 6   | 3   | 7   | (1),(2),(6), (3), 7 |
| 20  |   6     | H      | 1   | 2   | 6   | 3   | 7   | (1),(2),(6), (3), 7 |

8 pfs

































