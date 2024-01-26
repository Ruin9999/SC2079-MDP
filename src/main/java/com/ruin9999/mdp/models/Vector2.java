package com.ruin9999.mdp.models;

/**
 * A simple generic class representing a 2D vector with coordinates of type T.
 *
 * @param <T> The type of the coordinates.
 */
public class Vector2<T> {
    private T x;
    private T y;

    public Vector2(T x, T y) {
        this.x = x;
        this.y = y;
    }

    public T getX() {
        return this.x;
    }

    public T getY() {
        return this.y;
    }

    public void setX(T x) {
        this.x = x;
    }

    public void setY(T y) {
        this.y = y;
    }
}
