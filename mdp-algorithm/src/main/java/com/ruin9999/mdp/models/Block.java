package com.ruin9999.mdp.models;

import java.awt.*;
import java.util.UUID;

/***
 * A class that models a single square on the grid
 */
public class Block {
    public enum States {
        UNEXPLORED,
        EXPLORED,
        BLOCKED,
        PATH,
    }

    public enum Direction {
        NORTH,
        SOUTH,
        EAST,
        WEST,
    }

    public enum Type {
        OBSTACLE,
        GRID,
    }

    public static class Colors {
        public static final Color UNEXPLORED = Color.WHITE;
        public static final Color EXPLORED = Color.GRAY;
        public static final Color BLOCKED = Color.RED;
        public static final Color PATH = Color.YELLOW;
    }

    public UUID id = null;
    public Vector2<Integer> coords = null;
    public States state = null;
    public Direction direction = null;
    public Type type = null;
    public Color color = null;

    /***
     * Constructor for a typical {@code block}.
     *
     * @param coords The coordinates for this block.
     */
    public Block(Vector2<Integer> coords) {
        this.id = UUID.randomUUID();
        this.coords = coords;
        this.state = States.UNEXPLORED;
        this.type = Type.GRID;
        this.color = Colors.UNEXPLORED;
    }

    /**
     * Constructor for a typical {@code block}.
     *
     * @param coords The coordinates for this block.
     * @param state  The state of this block (UNEXPLORED, EXPLORED, BLOCKED, PATH).
     */
    public Block(Vector2<Integer> coords, States state) {
        this.id = UUID.randomUUID();
        this.coords = coords;
        this.state = state;
        this.type = Type.GRID;
        this.color = Colors.UNEXPLORED;
    }

    /**
     * Constructor for an {@code obstacle}.
     *
     * @param coords    The coordinates for this block.
     * @param state     The state of this block (UNEXPLORED, EXPLORED, BLOCKED, PATH).
     * @param direction The facing direction of this block (NORTH, SOUTH, EAST, WEST).
     */
    public Block(Vector2<Integer> coords, States state, Direction direction) {
        this.id = UUID.randomUUID();
        this.coords = coords;
        this.state = state;
        this.type = Type.OBSTACLE;
        this.direction = direction;
        this.color = Colors.BLOCKED;
    }


}
