package org.pcp.exactas.set;

import java.util.concurrent.atomic.AtomicMarkableReference;

public class LockFreeListSet implements ConcurrentIntSet {
    private final Node head = new Node(Long.MIN_VALUE, null);
    private final Node tail = new Node(Long.MAX_VALUE, null);

    public LockFreeListSet() { head.next.set(tail, false); }

    @Override public boolean add(int value) {
        while (true) {
            Window window = find(value);
            Node pred = window.pred;
            Node curr = window.curr;
            // TODO
            return false;
        }
    }

    @Override public boolean remove(int value) {
        while (true) {
            Window window = find(value);
            Node pred = window.pred;
            Node curr = window.curr;
            // TODO
            return false;
        }
    }

    @Override public boolean contains(int value) {
        // TODO
        return false;
    }

    @Override public boolean isImplemented() { return false; }

    private Window find(int value) {
        boolean[] marked = {false};
        retry:
        while (true) {
            Node pred = head;
            Node curr = pred.next.getReference();
            while (true) {
                Node succ = curr.next.get(marked);
                // Si curr->next está marcado, significa que debo eliminar curr de la lista
                while (marked[0]) {
                    if (!pred.next.compareAndSet(curr, succ, false, false))
                        continue retry;
                    curr = succ;
                    succ = curr.next.get(marked);
                }
                if (curr.key >= value) return new Window(pred, curr);
                pred = curr;
                curr = succ;
            }
        }
    }

    static final class Window {
        final Node pred;
        final Node curr;
        Window(Node pred, Node curr) { this.pred = pred; this.curr = curr; }
    }

    static final class Node {
        final long key;
        final AtomicMarkableReference<Node> next;
        Node(long key, Node next) { this.key = key; this.next = new AtomicMarkableReference<>(next, false); }
    }
}
