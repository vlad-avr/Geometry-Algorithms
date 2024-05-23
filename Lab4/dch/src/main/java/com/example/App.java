package com.example;

import java.util.Random;
import java.util.Scanner;

/**
 * Hello world!
 */
public final class App {
    private App() {
    }

    private static double getRoundedDouble(int scale, Random r){
        double randomValue = r.nextDouble();
        double roundedValue = Math.round(randomValue * scale) / scale;
        return roundedValue;
    }
    public static void main(String[] args) throws InterruptedException {
        int winX = 900;
        int winY = 350;
        int pointN = 20;
        int range = 20;
        int bound = 100;
        Scanner scan = new Scanner(System.in);

        Point[] points = new Point[pointN];
        Random r = new Random();
        for (int i = 0; i < points.length; i++) {
            points[i] = new Point(r.nextInt(bound) + getRoundedDouble(bound, r), r.nextInt(range) + getRoundedDouble(bound, r));
        }

        Hull con = new Hull();
        for (Point point : points) {
            System.out.println("Inserting : " + point.toString());
            con.insert(point);
            con.print();
            con.showPlot(winX, winY);
            scan.nextLine();
        }

        for (Point point : points) {
            System.out.println("Deleting : " + point.toString());
            con.delete(point);
            con.print();
            con.showPlot(winX, winY);
            scan.nextLine();
        }
        scan.close();
        System.out.println("Completed.");
    }
}
