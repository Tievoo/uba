// Volcan Lanin, parte 1.
import java.util.concurrent.Semaphore;

public class ExcursionPareja {
    static int STAGES = 5;

    public Semaphore s1 = new Semaphore(0);
    public Semaphore s2 = new Semaphore(0);

    public void caminarAndrea() throws InterruptedException {
        System.out.println("Andrea llega a la pirca");
        s1.release();
        s2.acquire();
        System.out.println("Andrea arranca el siguiente tramo");
    }

    public void caminarBernardo() throws InterruptedException {
        System.out.println("Bernardo llega a la pirca");
        s2.release();
        s1.acquire();
        System.out.println("Bernardo arranca el siguiente tramo");
    }

    public static void main(String[] args) throws InterruptedException {
        ExcursionPareja excursion = new ExcursionPareja();

        for (int stage = 1; stage <= STAGES; stage++) {
            System.out.println("--- tramo " + stage + " ---");
            Thread andrea = new Thread(() -> {
                try {
                    excursion.caminarAndrea();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            });
            Thread bernardo = new Thread(() -> {
                try {
                    excursion.caminarBernardo();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            });

            andrea.start();
            bernardo.start();
            andrea.join();
            bernardo.join();
        }
    }
}
