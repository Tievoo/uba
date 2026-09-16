package org.pcp.exactas.set;

import java.util.concurrent.locks.ReentrantLock;

public class CoarseListSet implements ConcurrentIntSet {
    private final ReentrantLock lock = new ReentrantLock();
    private final Node head = new Node(Long.MIN_VALUE);
    private final Node tail = new Node(Long.MAX_VALUE);

    public CoarseListSet() { head.next = tail; }

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
        Node(long key) { this(key, null); }
        Node(long key, Node next) { this.key=key; this.next=next; } }
}
