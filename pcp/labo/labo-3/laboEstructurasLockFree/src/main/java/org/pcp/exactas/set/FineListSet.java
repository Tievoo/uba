package org.pcp.exactas.set;

import java.util.concurrent.locks.ReentrantLock;

public class FineListSet implements ConcurrentIntSet {
    private final Node head = new Node(Long.MIN_VALUE);
    private final Node tail = new Node(Long.MAX_VALUE);

    public FineListSet() { head.next = tail; }

    @Override public boolean add(int value) {
        return false;
    }

    @Override public boolean remove(int value) {
        return false;
    }

    @Override public boolean contains(int value) {
        return false;
    }

    @Override public boolean isImplemented() {
        return false;
    }

    private static final class Node {
        final long key;
        Node next;
        final ReentrantLock lock = new ReentrantLock();
        Node(long key) { this(key, null); } Node(long key, Node next) { this.key=key; this.next=next; }
    }
}
