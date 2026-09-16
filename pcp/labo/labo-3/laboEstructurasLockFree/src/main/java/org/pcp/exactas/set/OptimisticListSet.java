package org.pcp.exactas.set;

import java.util.concurrent.locks.ReentrantLock;

public class OptimisticListSet implements ConcurrentIntSet {
    private final Node head = new Node(Long.MIN_VALUE);
    private final Node tail = new Node(Long.MAX_VALUE);

    public OptimisticListSet() { head.next = tail; }

    @Override public boolean add(int value) {
        while (true) {
            Node pred = head, curr = head.next;
            // TODO
            return false;
        }
    }

    @Override public boolean remove(int value) {
        while (true) {
            Node pred = head, curr = head.next;
            // TODO
            return false;
        }
    }

    @Override public boolean contains(int value) {
        while (true) {
            Node pred = head, curr = head.next;
            // TODO
            return false;
        }
    }

    @Override public boolean isImplemented() {
        return false;
    }

    // Dadas referencias a dos nodos pred --> curr, retorna true si sigue existiendo la relación pred --> curr en la lista
    private boolean edgeExists(Node pred, Node curr) {
        Node node = head;
        while (node.key <= pred.key) {
            if (node == pred)
                return pred.next == curr;
            node = node.next;
        }
        return false;
    }

    private static final class Node {
        final long key;
        volatile Node next;
        final ReentrantLock lock = new ReentrantLock();
        Node(long key) { this(key, null); }
        Node(long key, Node next) { this.key=key; this.next=next; }
    }
}
