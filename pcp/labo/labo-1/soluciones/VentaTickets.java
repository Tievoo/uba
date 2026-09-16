// Lollapallozers.

import java.util.concurrent.Semaphore;
import java.util.concurrent.ThreadLocalRandom;

public class VentaTickets {
    static int TYPES = 3;
    static int[] LIMIT = { 50, 30, 10 };
    static int BUYERS = 20;
    static int ATTEMPTS_PER_BUYER = 500;

    private int[] available = LIMIT.clone();
    private int version = 0;

    private int readers = 0;
    private Semaphore readersMutex = new Semaphore(1);
    private Semaphore turn = new Semaphore(1, true);

    static class Lectura {
        int quantity;
        int version;
        Lectura(int quantity, int version) {
            this.quantity = quantity;
            this.version = version;
        }
    }

    // Muchos compradores pueden ver a la vez, salvo que alguien este comprando.
    public Lectura ver(int type) throws InterruptedException {
        readersMutex.acquire();
        readers++;
        if (readers == 1) turn.acquire(); // el primer lector le saca el turno a los compradores
        readersMutex.release();

        Lectura reading = new Lectura(available[type], version);

        readersMutex.acquire();
        readers--;
        if (readers == 0) turn.release(); // el ultimo lector devuelve el turno
        readersMutex.release();

        return reading;
    }

    // Exclusivo de punta a punta: mientras un comprador esta aca, ningun
    // lector nuevo puede entrar a ver(). Devuelve false si la version ya
    // no es la actual (hay que releer) o si no quedan tickets.
    public boolean comprar(int type, int readVersion) throws InterruptedException {
        turn.acquire();
        try {
            if (version != readVersion) return false;
            if (available[type] == 0) return false;
            available[type]--;
            version++;
            return true;
        } finally {
            turn.release();
        }
    }

    public boolean intentarComprar(int type) throws InterruptedException {
        while (true) {
            Lectura reading = ver(type);
            if (reading.quantity == 0) return false;
            if (comprar(type, reading.version)) return true;
            // alguien compro entre el ver() y el comprar(): releer y reintentar.
        }
    }

    public static void main(String[] args) throws InterruptedException {
        VentaTickets sale = new VentaTickets();
        int[] soldPerThread = new int[BUYERS];

        Thread[] buyers = new Thread[BUYERS];
        for (int i = 0; i < BUYERS; i++) {
            int id = i;
            buyers[i] = new Thread(() -> {
                int sold = 0;
                try {
                    for (int j = 0; j < ATTEMPTS_PER_BUYER; j++) {
                        int type = ThreadLocalRandom.current().nextInt(TYPES);
                        if (sale.intentarComprar(type)) sold++;
                        Thread.sleep(ThreadLocalRandom.current().nextInt(5)); // simula tiempo entre compras
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                soldPerThread[id] = sold;
            });
        }

        for (Thread t : buyers) t.start();
        for (Thread t : buyers) t.join();

        int totalSold = 0;
        for (int v : soldPerThread) totalSold += v;

        int totalRemaining = 0;
        boolean oversold = false;
        for (int type = 0; type < TYPES; type++) {
            int remaining = sale.available[type];
            totalRemaining += remaining;
            if (remaining < 0) oversold = true;
        }

        int totalLimit = 0;
        for (int l : LIMIT) totalLimit += l;

        System.out.println("Vendidos: " + totalSold + ", restante: " + totalRemaining + ", total: " + totalLimit);
        boolean ok = !oversold && (totalSold + totalRemaining == totalLimit);
        System.out.println(ok ? "OK" : "MAL");
    }
}
