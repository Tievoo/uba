import java.util.concurrent.Semaphore;
import java.util.concurrent.ThreadLocalRandom;

public class CaminoUnaViaFIFO {
    static int A = 0, B = 1;
    static int NUM_CARS = 12;
    static int BRIDGE_CAPACITY = 4;

    // Cada auto es un thread de esta clase, que tiene su propio campo para
    // guardar su posicion en exitQueue entre entrar() y salir().
    static class Auto extends Thread {
        private int miSlot;

        Auto(Runnable r) {
            super(r);
        }

        static Auto actual() {
            return (Auto) Thread.currentThread();
        }
    }

    private Semaphore turnstile = new Semaphore(1);
    private Semaphore resource = new Semaphore(1);
    private Semaphore[] countMutex = { new Semaphore(1), new Semaphore(1) };
    private int[] count = new int[2];

    private Semaphore spots = new Semaphore(BRIDGE_CAPACITY);
    private Semaphore queueMutex = new Semaphore(1);
    private Semaphore[] exitQueue = new Semaphore[BRIDGE_CAPACITY];
    private int head = 0;
    private int nextSpot = 0;
    private int queued = 0;

    {
        for (int i = 0; i < BRIDGE_CAPACITY; i++) {
            exitQueue[i] = new Semaphore(0);
        }
    }

    public void entrar(int direction) throws InterruptedException {
        turnstile.acquire();
        countMutex[direction].acquire();
        count[direction]++;
        if (count[direction] == 1) {
            resource.acquire();
        }
        countMutex[direction].release();
        turnstile.release();

        spots.acquire();

        queueMutex.acquire();
        int slot = nextSpot;
        nextSpot = (nextSpot + 1) % BRIDGE_CAPACITY;
        boolean esElPrimero = queued == 0;
        queued++;
        queueMutex.release();

        if (esElPrimero) {
            exitQueue[slot].release();
        }
        Auto.actual().miSlot = slot;
    }

    public void salir(int direction) throws InterruptedException {
        exitQueue[Auto.actual().miSlot].acquire();

        countMutex[direction].acquire();
        count[direction]--;
        if (count[direction] == 0) {
            resource.release();
        }
        countMutex[direction].release();

        queueMutex.acquire();
        head = (head + 1) % BRIDGE_CAPACITY;
        queued--;
        boolean alguienQueda = queued > 0;
        int nuevoHead = head;
        queueMutex.release();

        if (alguienQueda) {
            exitQueue[nuevoHead].release();
        }

        spots.release();
    }

    // Simula el tiempo que tarda un auto en cruzar el desvio.
    private void cruzarPuente() throws InterruptedException {
        Thread.sleep(ThreadLocalRandom.current().nextInt(2));
    }

    public static void main(String[] args) throws InterruptedException {
        CaminoUnaViaFIFO route = new CaminoUnaViaFIFO();

        Auto[] cars = new Auto[NUM_CARS];
        for (int i = 0; i < NUM_CARS; i++) {
            int car = i;
            cars[i] = new Auto(() -> {
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
