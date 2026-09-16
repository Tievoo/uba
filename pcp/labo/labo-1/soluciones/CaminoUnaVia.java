import java.util.concurrent.Semaphore;
import java.util.concurrent.ThreadLocalRandom;

public class CaminoUnaVia {
    static int A = 0, B = 1;
    static int NUM_CARS = 12;

    private Semaphore turnstile = new Semaphore(1);
    private Semaphore resource = new Semaphore(1);
    private Semaphore[] countMutex = { new Semaphore(1), new Semaphore(1) };
    private int[] count = new int[2];

    public void entrar(int direction) throws InterruptedException {
        turnstile.acquire();
        countMutex[direction].acquire();
        count[direction]++;
        if (count[direction] == 1) {
            resource.acquire();
        }
        countMutex[direction].release();
        turnstile.release();
    }

    public void salir(int direction) throws InterruptedException {
        countMutex[direction].acquire();
        count[direction]--;
        if (count[direction] == 0) {
            resource.release();
        }
        countMutex[direction].release();
    }

    // Simula el tiempo que tarda un auto en cruzar el desvio.
    private void cruzarPuente() throws InterruptedException {
        Thread.sleep(ThreadLocalRandom.current().nextInt(2));
    }

    public static void main(String[] args) throws InterruptedException {
        CaminoUnaVia route = new CaminoUnaVia();

        Thread[] cars = new Thread[NUM_CARS];
        for (int i = 0; i < NUM_CARS; i++) {
            int car = i;
            cars[i] = new Thread(() -> {
                try {
                    while (true) {
                        int direction = ThreadLocalRandom.current().nextInt(2);
                        route.entrar(direction);
                        System.out.println("Auto " + car + " cruzando en sentido " + direction);
                        route.cruzarPuente();
                        route.salir(direction);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }

        for (Thread t : cars) t.start();
        for (Thread t : cars) t.join();
    }
}
