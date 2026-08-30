// Zorros grises de Saldungaray, parte 2 .
import java.util.concurrent.ThreadLocalRandom;

public class CaminoUnaViaFIFO {
    static int NUM_CARS = 12;
    static int BRIDGE_CAPACITY = 4;

    // TODO: variables de sincronizacion.

    public void entrar(int direction) throws InterruptedException {
        // TODO
    }

    public void salir(int direction) throws InterruptedException {
        // TODO
    }

    // Simula el tiempo que tarda un auto en cruzar el desvio.
    private void cruzarPuente() throws InterruptedException {
        Thread.sleep(ThreadLocalRandom.current().nextInt(2));
    }

    public static void main(String[] args) throws InterruptedException {
        CaminoUnaViaFIFO route = new CaminoUnaViaFIFO();

        for (int i = 0; i < NUM_CARS; i++) {
            int car = i;
            int direction = ThreadLocalRandom.current().nextInt(2);
            System.out.println("Auto " + car + " cruzando en sentido " + direction);
        }
    }
}
