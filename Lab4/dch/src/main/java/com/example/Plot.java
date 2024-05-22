package com.example;

import javax.swing.*;
import java.awt.*;
import java.awt.geom.Ellipse2D;
import java.awt.geom.Line2D;
import java.util.ArrayList;


public class Plot extends JPanel {
    private final ArrayList<Point> points;
    private final ArrayList<Point> hull;
    private final double shiftX;
    private final double shiftY;
    private static final float size = 10;

    public Plot(ArrayList<Point> points, ArrayList<Point> hull, double shiftX, double shiftY) {
        this.points = points;
        this.hull = hull;
        this.shiftX = shiftX;
        this.shiftY = shiftY;
    }

    public static float sizeFactor() {
        return size;
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        Graphics2D graph = (Graphics2D) g;
        graph.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        graph.setStroke(new BasicStroke(size / 2));


        graph.setPaint(Color.BLUE);
        for (int i = 0; i < hull.size()-1; i++) {
            graph.draw(new Line2D.Double((hull.get(i).x - shiftX) * size + size, (hull.get(i).y - shiftY) * size + size,
                    (hull.get(i + 1).x - shiftX) * size + size, (hull.get(i + 1).y - shiftY) * size + size));
        }

        graph.setPaint(Color.RED);
        for (Point point : points) {
            graph.fill(new Ellipse2D.Double((point.x - shiftX)*size + size/2, (point.y - shiftY)*size + size/2, size, size));
        }

        graph.setPaint(Color.BLUE);
        for (Point point : hull) {
            graph.fill(new Ellipse2D.Double((point.x - shiftX)*size + size/2, (point.y - shiftY)*size + size/2, size, size));
        }
    }
}