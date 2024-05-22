package com.example;

import java.util.Objects;


public class Point implements Comparable<Point> {
	protected final double x;
	protected final double y;
	
	public Point(double x, double y) {
		this.x = x;
		this.y = y;
	}

	@Override
	public int compareTo(Point o) {
		return Double.compare(this.x, o.x);
	}

	@Override
	public boolean equals(Object o) {
		if (this == o) return true;
		if (!(o instanceof Point)) return false;
		return Double.compare(this.x, ((Point)o).x) == 0 && Double.compare(this.y, ((Point)o).y) == 0;
	}

	@Override
	public int hashCode() {
		return Objects.hash(x, y);
	}
}