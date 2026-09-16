import java.util.concurrent.Semaphore;

public class ExcursionPareja {
    static int STAGES = 5;

    private Semaphore andreaArrived = new Semaphore(0);
    private Semaphore bernardoArrived = new Semaphore(0);

    public void caminarAndrea() throws InterruptedException {
        System.out.println("Andrea llega a la pirca");
        andreaArrived.release();
        bernardoArrived.acquire();
        System.out.println("Andrea arranca el siguiente tramo");
    }

    public void caminarBernardo() throws InterruptedException {
        System.out.println("Bernardo llega a la pirca");
        bernardoArrived.release();
        andreaArrived.acquire();
        System.out.println("Bernardo arranca el siguiente tramo");
    }

    public static void main(String[] args) throws InterruptedException {
        ExcursionPareja excursion = new ExcursionPareja();

        for (int stage = 1; stage <= STAGES; stage++) {
            System.out.println("--- tramo " + stage + " ---");

            Thread andrea = new Thread(() -> {
                try { excursion.caminarAndrea(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
            });
            Thread bernardo = new Thread(() -> {
                try { excursion.caminarBernardo(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
            });

            andrea.start();
            bernardo.start();
            andrea.join();
            bernardo.join();
        }
    }
}
