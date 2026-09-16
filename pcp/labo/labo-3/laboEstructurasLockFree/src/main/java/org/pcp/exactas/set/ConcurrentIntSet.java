package org.pcp.exactas.set;

public interface ConcurrentIntSet {

    boolean add(int value) {
        // IMPLEMENT IT
        
    }

    boolean remove(int value);

    boolean contains(int value);

    default boolean isImplemented() {
        return false;
    }
}
