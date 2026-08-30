// Lollapallozers.

public class VentaTickets {
    static int TYPES = 3;
    static int[] LIMIT = { 50, 30, 10 };
    static int BUYERS = 20;
    static int ATTEMPTS_PER_BUYER = 500;

    private int[] available = LIMIT.clone();

    // TODO: variables de sincronizacion.

    // Devuelve true si logro comprar un ticket del tipo dado, false si no quedan.
    public boolean comprar(int type) throws InterruptedException {
        // TODO
        return false;
    }

    public static void main(String[] args) throws InterruptedException {
        VentaTickets sale = new VentaTickets();
        int[] soldPerBuyer = new int[BUYERS];

        int totalSold = 0;
        for (int v : soldPerBuyer) totalSold += v;

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
