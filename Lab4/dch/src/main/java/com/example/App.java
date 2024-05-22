package com.example;

import java.util.Random;

/**
 * Hello world!
 */
public final class App {
    private App() {
    }
    public static void main(String[] args) throws InterruptedException {
        int winX = 900;
        int winY = 350;
        int pointN = 20;
        int range = 50;
        int time = 1000;

        Point[] points = new Point[pointN];
        Random r = new Random();
        for (int i = 0; i < points.length; i++) {
            points[i] = new Point(range * r.nextDouble(), range * r.nextDouble());
        }

        Hull con = new Hull();
        for (Point point : points) {
            con.insert(point);
            con.showPlot(winX, winY);
            Thread.sleep(time);
        }

        for (Point point : points) {
            con.delete(point);
            con.showPlot(winX, winY);
            Thread.sleep(time);
        }

        System.out.println("Completed.");
    }
}
