package com.example;

import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.stream.Collectors;
import java.util.stream.Stream;


public class Hull extends HalfHull {
    protected final HalfHull topHullHalf;
    protected final HalfHull bottomHullHalf;
    protected final ArrayList<Point> points;
    protected final JFrame plotFrame;

    public Hull() {
        topHullHalf = new HalfHull();
        bottomHullHalf = new HalfHull();
        points = new ArrayList<>();
        plotFrame = new JFrame();
        plotFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    @Override
    public void insert(Point e) {
        points.add(e);
        topHullHalf.insert(e);
        bottomHullHalf.insert(new Point(e.x, -e.y));
    }

    @Override
    public void delete(Point e) {
        points.remove(e);
        topHullHalf.delete(e);
        bottomHullHalf.delete(new Point(e.x, -e.y));
    }

    @Override
    public ArrayList<Point> getHull() {
        ArrayList<Point> topHull = topHullHalf.getHull();
        ArrayList<Point> bottomHull = bottomHullHalf.getHull();
        bottomHull.replaceAll(coord -> new Point(coord.x, -coord.y));
        Collections.reverse(bottomHull);
        if (!bottomHull.isEmpty()) {
            bottomHull.remove(0);
        }
        ArrayList<Point> hull = new ArrayList<>(Stream.concat(topHull.stream(), bottomHull.stream()).collect(Collectors.toCollection(ArrayList::new)));
        if (hull.isEmpty()) {
            return new ArrayList<>(points);
        }
        return hull;
    }

    public void showPlot(int xPos, int yPos) {
        double minX = Double.POSITIVE_INFINITY;
        double maxX = Double.NEGATIVE_INFINITY;
        double minY = Double.POSITIVE_INFINITY;
        double maxY = Double.NEGATIVE_INFINITY;
        for (Point point : points) {
            if (point.x > maxX) {
                maxX = point.x;
            }
            if (point.y > maxY) {
                maxY = point.y;
            }
            if (point.x < minX) {
                minX = point.x;
            }
            if (point.y < minY) {
                minY = point.y;
            }
        }
        int sizeX = (int) ((maxX - minX) * Plot.sizeFactor() + 2 * Plot.sizeFactor());
        int sizeY = (int) ((maxY - minY) * Plot.sizeFactor() + 2 * Plot.sizeFactor());
        plotFrame.getContentPane().removeAll();
        plotFrame.getContentPane().repaint();
        plotFrame.getContentPane().setPreferredSize(new Dimension(sizeX, sizeY));
        if (!points.isEmpty()) {
            plotFrame.setLocation(xPos + ((int) (minX*Plot.sizeFactor())), yPos + ((int) (minY*Plot.sizeFactor())));
        } else {
            plotFrame.setLocation(xPos, yPos);
        }
        ArrayList<Point> currentHull = getHull();
        plotFrame.add(new Plot(points, currentHull, minX, minY));
        plotFrame.getContentPane().validate();
        plotFrame.getContentPane().repaint();
        plotFrame.pack();
        plotFrame.setVisible(true);
    }
}