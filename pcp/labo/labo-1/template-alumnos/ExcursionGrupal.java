// Volcan Lanin, parte 2.
import java.util.concurrent.Semaphore;

public class ExcursionGrupal {
    static int PORTENIOS = 60;
    static int STAGES = 4;

    public Semaphore mutex = new Semaphore(1);
    public Semaphore molinete1 = new Semaphore(0);
    public Semaphore molinete2 = new Semaphore(0);
    public int waiting = 0;

    public void esperarPirca() throws InterruptedException {
        mutex.acquire();
        waiting++;
        if (waiting == PORTENIOS) {
            molinete1.release(PORTENIOS);
        }
        mutex.release();
        
        molinete1.acquire();

        mutex.acquire();
        waiting--;
        if (waiting == 0) {
            molinete2.release(PORTENIOS);
        }
        mutex.release();
        molinete2.acquire();
    }

    public static void main(String[] args) throws InterruptedException {
        ExcursionGrupal excursion = new ExcursionGrupal();

        Thread[] group = new Thread[PORTENIOS];
        for (int i = 0; i < PORTENIOS; i++) {
            int id = i;
            group[i] = new Thread(() -> {
                try {
                    for (int stage = 1; stage <= STAGES; stage++) {
                        Thread.sleep((long) (Math.random() * 300));
                        System.out.println("porteno " + id + " llega a la pirca del tramo " + stage);
                        excursion.esperarPirca();
                        System.out.println("porteno " + id + " arranca el tramo " + (stage + 1));
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }

        for (Thread t : group) t.start();
        for (Thread t : group) t.join();
    }
}
