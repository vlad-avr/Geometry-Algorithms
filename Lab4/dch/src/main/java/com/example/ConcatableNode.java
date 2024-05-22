package com.example;

public class ConcatableNode extends Node<Point> {
	protected ConcatableNode left, right, leftBranchMax;
	protected HullPart hull;
	
	public ConcatableNode (Point c) {
		this.isLeaf = true;
		this.color = BLACK;
		this.ex = c;
		this.leftBranchMax = this;

		hull = new HullPart(c);
	}

	public ConcatableNode (ConcatableNode lMax, ConcatableNode left, ConcatableNode right) {
		this.isLeaf = false;
		this.color = RED;
		this.leftBranchMax = lMax;
		this.left = left;
		this.right = right;
		
		hull = HullPart.bridge(left.hull, right.hull);
	}
}