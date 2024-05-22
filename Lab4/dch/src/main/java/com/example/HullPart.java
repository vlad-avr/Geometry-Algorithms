package com.example;

import java.util.ArrayList;


public class HullPart extends ConcatableQueue<Point> {
	public HullPart(Point c) {
		super(c);
	}
	
	public HullPart(ConcatableQueue<Point> q) {
		super(q.root, q.height, q.minNode, q.maxNode);
	}
	
	public static HullPart bridge (HullPart lHull, HullPart rHull) {
		Node<Point> lItr = lHull.root;
		Node<Point> rItr = rHull.root;
		
		boolean done = false;
		double middleX = (lHull.maxNode.ex.x + rHull.minNode.ex.x)/2.0;
		
		while ( !done ) {
			double t = computeSlope(lItr.leftBranchMax, rItr.leftBranchMax);
			int iL = determineCase(lItr.leftBranchMax, t);
			int iR = determineCase(rItr.leftBranchMax, t);
		
			switch (iL) {
			case -1:
				switch (iR) {
					case -1 : rItr = rItr.right; break;
					case 0 : {
						lItr = lItr.right;
						if (!rItr.isLeaf && rItr.right != null) {
							rItr = rItr.right;
						}
						break;
					}
					case +1 : {
						double lHeight = lItr.leftBranchMax.ex.y +
								computeSlope(lItr.leftBranchMax, lItr.leftBranchMax.right) * (middleX - lItr.leftBranchMax.ex.x);
						double rHeight = rItr.leftBranchMax.ex.y +
								computeSlope(rItr.leftBranchMax.left, rItr.leftBranchMax) * (middleX - rItr.leftBranchMax.ex.x);
						if (lHeight <= rHeight) {
							rItr = rItr.left;
						} else {
							lItr = lItr.right;
						}
					}
					break;
				}
				break;
			case 0:
				switch (iR) {
					case -1 : {
						if (!lItr.isLeaf && lItr.left != null) {
							lItr = lItr.left;
						}
						rItr = rItr.right;
					}
					break;
					case 0 : {
						lItr = lItr.leftBranchMax;
						rItr = rItr.leftBranchMax;
						done = true;
					}
					break;
					case +1 : {
						if (!lItr.isLeaf && lItr.left != null) {
							lItr = lItr.left;
						}
						rItr = rItr.left;
					}
					break;
				}
				break;
			case +1:
				switch (iR) {
					case -1 : {
						lItr = lItr.left;
						rItr = rItr.right;
					}
					break;
					case 0 : {
						lItr = lItr.left;
						if (!rItr.isLeaf && rItr.right != null) {
							rItr = rItr.right;
						}
					}
					break;
					case +1 : lItr = lItr.left; break;
				}
				break;
			}
		}
		return new HullPart(concatenate(lHull.split(lItr.ex, LEFT, true), rHull.split(rItr.ex, RIGHT, false)));
	}
	
	public ArrayList<Point> getHull() {
		if (root == null) {
			return new ArrayList<>();
		}

		ArrayList<Point> res = new ArrayList<>();
		Node<Point> n = minNode;
		while (n != null) {
			res.add(n.ex);
			n = n.right;
		}
		return res;
	}
	
	protected static double computeSlope (Node<Point> leftN, Node<Point> rightN) {
		return (rightN.ex.y - leftN.ex.y)/(rightN.ex.x - leftN.ex.x);
	}
	
	protected static int determineCase (Node<Point> n, double t) {
		boolean leftAbove = true;
		boolean rightAbove = false;
		
		if ( (n.left != null) && computeSlope(n.left, n) < t  ) {
			leftAbove = false;
		}
		
		if ( (n.right != null) && computeSlope(n, n.right) > t  ) {
			rightAbove = true;
		}
		
		if (leftAbove && rightAbove) {
			return -1;
		}
		else if (!leftAbove && !rightAbove) {
			return +1;
		}
		else {
			return 0;
		}
	}
}