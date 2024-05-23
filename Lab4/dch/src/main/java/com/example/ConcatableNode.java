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
		System.out.println(hull.toString());
	}

	public void print(String tab){
		if(isLeaf){
			System.out.println(tab + "LEAF (ex=" + ex + ")");
			return;
		}
		String toPrint = tab + "NODE (leftMax=" + leftBranchMax.ex.toString();
		if(hull != null){
			toPrint += " hull : " + hull.toString();
		}
		toPrint += ") : ";
		System.out.println(toPrint);	
		if(left != null){
			System.out.println(tab + "left -> ");
			left.print(tab + "\t");
		}
		if(right != null){
			System.out.println(tab + "right -> ");
			right.print(tab + "\t");
		}
	}

	public Point getEx(){
		return this.ex;
	}
}