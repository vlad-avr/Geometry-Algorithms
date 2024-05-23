package com.example;

import java.util.ArrayList;


public class HalfHull extends Tree<Point> {
	protected ConcatableNode root;
	public HalfHull() {
		super();
	}
	
	protected static void DOWN (ConcatableNode n) {
		n.left.hull = new HullPart(ConcatableQueue.concatenate(n.hull.split(n.leftBranchMax.ex, LEFT, true), n.left.hull));
		n.right.hull = new HullPart(ConcatableQueue.concatenate(n.right.hull, n.hull));
	}
	
	protected static void UP (ConcatableNode n) {
		n.hull = HullPart.bridge(n.left.hull, n.right.hull);
	}
	
	protected static ConcatableNode rotateLeft (ConcatableNode n) {
		DOWN(n);
		ConcatableNode tempCNode = n.right;
		boolean tempColor = n.color;
		DOWN(tempCNode);
		n.right = tempCNode.left;
		n.color = tempCNode.color;
		UP(n);
		tempCNode.left = n;
		tempCNode.color = tempColor;
		UP(tempCNode);
		return tempCNode;
	}
	
	protected static ConcatableNode rotateRight (ConcatableNode n) {
		DOWN(n);
		ConcatableNode tempCNode = n.left;
		boolean tempColor = n.color;
		DOWN(tempCNode);
		n.left = tempCNode.right;
		n.color = tempCNode.color;
		UP(n);
		tempCNode.right = n;
		tempCNode.color = tempColor;
		UP(tempCNode);
		return tempCNode;
	}

	public void print(){
		// String hull = "";
		// ArrayList<Point> hullList = getHull();
		// for(Point point : hullList){
		// 	hull += point.toString();
		// }
		// System.out.println("HULL " + hull);
		root.print("");
	}

	protected ConcatableNode addLeaf (Point c) {
		size ++;
		return new ConcatableNode(c);
	}

	protected static void flipColor (ConcatableNode n) {
		n.color = !n.color;
		n.left.color = !n.left.color;
		n.right.color = !n.right.color;
	}
	
	protected static ConcatableNode fixUpdate (ConcatableNode n) {
		if (n.isLeaf) {
			return n;
		}
		
		if (n.left.color == BLACK && n.right.color == RED) {
			n = rotateLeft(n);
		}
		else {
			if (n.left.color == RED && n.left.left.color == RED) {
				n = rotateRight(n);
			}
			if (n.left.color == RED && n.right.color == RED) {
				flipColor(n);
			}
		}
		return n;
	}
	
	protected ConcatableNode insertAt (ConcatableNode n, Point e) {
		if (e.compareTo(n.leftBranchMax.ex) <= 0) {
			if (n.isLeaf) {
				if (e.compareTo(n.ex) == 0) {
					n.ex = e;
				}
				else {
					ConcatableNode nNew = addLeaf(e);
					n = new ConcatableNode(nNew, nNew, n);
				}
			}
			else {
				DOWN(n);
				n.left = insertAt(n.left, e);
				UP(n);
			}
		}
		else {
			if (n.isLeaf) {
				ConcatableNode nNew = addLeaf(e);
				n = new ConcatableNode(n, n, nNew);
			}
			else {
				DOWN(n);
				n.right = insertAt(n.right, e);
				UP(n);
			}
		}
	
		n = fixUpdate(n);
		return n;
	}
	
	protected ConcatableNode deleteAt (ConcatableNode n, Point e) {
		if (e.compareTo(n.leftBranchMax.ex) <= 0) {
			if (n.left.isLeaf) {
				if (e.compareTo(n.left.ex) != 0) {
					return n;
				}
				else {
					DOWN(n);
					removeLeaf(n.left);
					return n.right;
				}
			}
		
			DOWN(n);
			
			if (e.compareTo(n.leftBranchMax.ex) == 0) {
				ConcatableNode tempCNode = n.left;
				while (!tempCNode.right.isLeaf) {
					tempCNode = tempCNode.right;
				}
				n.leftBranchMax = tempCNode.leftBranchMax;
			}
			
			if (n.left.color == RED || n.left.left.color == RED) {
				n.left = deleteAt(n.left,e);
				UP(n);
			}
			else {
				flipColor(n);
				n.left = deleteAt(n.left,e);
				if (n.left.color == RED) {
					UP(n);
					flipColor(n);
				}
				else if (n.right.left.color == BLACK) {
					UP(n);
					n = rotateLeft(n);
				}
				else {
					n.right = rotateRight(n.right);
					UP(n);
					n = rotateLeft(n);
					flipColor(n);
				}
			}
		}
		else {
			if (n.right.isLeaf) {
				if (e.compareTo(n.right.ex) != 0) {
					return n;
				}
				else {
					DOWN(n);
					removeLeaf(n.right);
					n.left.color = BLACK;
					return n.left;
				}
			}
			else if (n.right.left.color == RED) {
				DOWN(n);
				n.right = deleteAt(n.right,e);
				UP(n);
			}
			else if (n.color == RED) {
				
				flipColor(n);
				DOWN(n);
				n.right = deleteAt(n.right,e);
				UP(n);
				if (n.right.color == RED) {
					flipColor(n);
				}
				else if (n.left.left.color == RED) {
					n = rotateRight(n);
					flipColor(n);
				}
			}
			else {
				n = rotateRight(n);
				DOWN(n);
				n.right = deleteAt(n.right,e);
				UP(n);
				if (n.right.color == RED) {
					n = rotateLeft(n);
				}
			}
		}
		return n;
	}

	public void insert (Point e) {
		if (root == null) {
			root = new ConcatableNode(e);
			size = 1;
		}
		else {
			root = insertAt(root, e);
			if (root.color == RED) {
				root.color = BLACK;
			}
		}
	}

	public void delete (Point e) {
		if (root == null) {
			return;
		}
		if (root.isLeaf) {
			if (e.compareTo(root.ex) == 0) {
				root = null;
				size = 0;
			}
		}
		else {
			if (root.left.color == BLACK && root.right.color == BLACK) {
				root.color = RED;
			}
			root = deleteAt(root, e);
			if (root.color == RED) {
				root.color = BLACK;
			}
		}
	}

	public ArrayList<Point> getHull() {
		return root != null ? root.hull.getHull() : new ArrayList<>();
	}
}