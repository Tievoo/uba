// Reutilizada de ejercicios2/soluciones/Barrera.java (Ejercicio 1): ya
// resuelve el problema de la parte 2 de Volcan Lanin.
import java.util.concurrent.Semaphore;

public class Barrera {

    private int n;
    private int count = 0;
    private Semaphore mutex = new Semaphore(1);
    private Semaphore turnstile = new Semaphore(0);
    private Semaphore turnstile2 = new Semaphore(0);

    public Barrera(int n) {
        this.n = n;
    }

    public void esperar() throws InterruptedException {
        mutex.acquire();
        count++;
        if (count == n) {
            turnstile.release(n);
        }
        mutex.release();

        turnstile.acquire();

        mutex.acquire();
        count--;
        if (count == 0) {
            turnstile2.release(n);
        }
        mutex.release();

        turnstile2.acquire();
    }
}
