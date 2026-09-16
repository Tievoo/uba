package org.pcp.exactas.set;

import java.util.concurrent.locks.ReentrantLock;

public class LazyListSet implements ConcurrentIntSet {
    private final Node head = new Node(Long.MIN_VALUE);
    private final Node tail = new Node(Long.MAX_VALUE);

    public LazyListSet() { head.next = tail; }

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
        // TODO
        return false;
    }

    private static boolean edgeExists(Node pred, Node curr) {
        // TODO
        return false;
    }

    @Override public boolean isImplemented() {
        return false;
    }

    private static final class Node {
        final long key;
        volatile Node next;
        volatile boolean marked;
        final ReentrantLock lock = new ReentrantLock();
        Node(long key) { this(key, null); } Node(long key, Node next) { this.key=key; this.next=next; }
    }
}
