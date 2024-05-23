package com.example;

public class ConcatableQueue<E extends Comparable<E>> extends Tree<E>{
	protected int height;
	protected Node<E> minNode, maxNode;
	
	public ConcatableQueue () {
		this.root = null;
		this.height = -1;
		this.minNode = null;
		this.maxNode = null;
	}
	
	public ConcatableQueue (E e) {
		this.root = new Node<>(e);
		this.height = 0;
		this.minNode = root;
		this.maxNode = root;
	}
	
	public ConcatableQueue (Node<E> root, int height, Node<E> minNode, Node<E> maxNode) {
		this.root = root;
		this.height = height;
		this.minNode = minNode;
		this.maxNode = maxNode;
	}

	public void rootCopy (ConcatableQueue<E> other) {
		if (other == null) {
			return;
		}
		this.root = other.root;
		this.height = other.height;
		this.minNode = other.minNode;
		this.maxNode = other.maxNode;
	}
	
	protected void removeLeaf (Node<E> n) {
		if (n.left != null) {
			n.left.right = n.right;
		}
		else {
			minNode = n.right;
		}
		
		if (n.right != null) {
			n.right.left = n.left;
		}
		else {
			maxNode = n.left;
		}
	}

	protected static <E extends Comparable<E>> Node<E> concatTree (Node<E> leftNode, Node<E> rightNode, int leftHeight, int rightHeight, Node<E> leftMax) {
		if (leftNode == null) {
			return rightNode;
		}
		else if (rightNode == null) {
			return leftNode;
		}
		else if (leftHeight == rightHeight) {
			return new Node<>(leftMax, leftNode, rightNode);
		}
		else if (leftHeight > rightHeight) {
			leftNode.right = concatTree(leftNode.right, rightNode, leftHeight-1, rightHeight, leftMax);
			leftNode = fixUpdate(leftNode);
			return leftNode;
		}
		else {
			if (rightNode.left.color == RED) {
				rightNode.left = concatTree(leftNode, rightNode.left, leftHeight, rightHeight, leftMax);
				rightNode = fixUpdate(rightNode);
			}
			else {
				rightNode.left = concatTree(leftNode, rightNode.left, leftHeight, rightHeight-1, leftMax);
			}
			return rightNode;
		}
	}
	
	public static <E extends Comparable<E>> ConcatableQueue<E> concatenate (ConcatableQueue<E> qLeft, ConcatableQueue<E> qRight) {
		if (qLeft == null || qLeft.height == -1) {
			return qRight;
		}
		else if (qRight == null || qRight.height == -1) {
			return qLeft;
		}

		qLeft.maxNode.right = qRight.minNode;
		qRight.minNode.left = qLeft.maxNode;

		int newHeight = Math.max(qLeft.height, qRight.height);
		Node<E> newRoot = concatTree(qLeft.root, qRight.root, qLeft.height, qRight.height, qLeft.maxNode);
		if (newRoot.color == RED) {
			newRoot.color = BLACK;
			newHeight++;
		}

		return new ConcatableQueue<> (newRoot, newHeight, qLeft.minNode, qRight.maxNode);
	}

	protected static <E extends Comparable<E>> void cutAt (Node<E> n) {
		if (n != null && n.right != null) {
			n.right.left = null;
			n.right = null;
		}
	}
	
	protected static <E extends Comparable<E>> void splitAt(Node<E> n, int h, E e, ConcatableQueue<E> qLeft, ConcatableQueue<E> qRight) {
		if (n.isLeaf) {
			if (e.compareTo(n.ex) < 0) {
				qRight.root = n;
				qRight.minNode = n;
				qRight.height = 0;
				qLeft.maxNode = n.left;
				cutAt(n.left);
			}
			else {
				qLeft.root = n;
				qLeft.maxNode = n;
				qLeft.height = 0;
				qRight.minNode = n.right;
				cutAt(n);
			}
		}
		else {
			if (e.compareTo(n.leftBranchMax.ex) == 0) {
				qLeft.root = n.left;
				qLeft.height = h-1;
				qLeft.maxNode = n.leftBranchMax;
				if (qLeft.root.color == RED) {
					qLeft.root.color = BLACK;
					qLeft.height ++;
				}
				qRight.root = n.right;
				qRight.height = h-1;
				qRight.minNode = n.leftBranchMax.right;
				cutAt(n.leftBranchMax);
			}
			else if (e.compareTo(n.leftBranchMax.ex) < 0) {
				if (n.left.color == RED) {
					n.left.color = BLACK;
					splitAt(n.left, h, e, qLeft, qRight);
				}
				else {
					splitAt(n.left, h-1, e, qLeft, qRight);
				}
				int tempHeight = qRight.height;
				qRight.root = concatTree(qRight.root, n.right, qRight.height, h-1, n.leftBranchMax);
				qRight.height = Math.max(tempHeight, h-1);
				if (qRight.root.color == RED) {
					qRight.root.color = BLACK;
					qRight.height ++;
				}
			}
			else {
				splitAt(n.right, h-1, e, qLeft, qRight);
				if (n.left.color == RED) {
					n.left.color = BLACK;
					qLeft.root = concatTree(n.left, qLeft.root, h, qLeft.height, n.leftBranchMax);
					qLeft.height = h;
				}
				else {
					qLeft.root = concatTree(n.left, qLeft.root, h-1, qLeft.height, n.leftBranchMax);
					qLeft.height = h - 1;
				}
				
				if (qLeft.root.color == RED) {
					qLeft.root.color = BLACK;
					qLeft.height ++;
				}
			}
		}
	}
	
	public ConcatableQueue<E> split(E e, boolean returnLoR, boolean inclusive) {
		ConcatableQueue<E> qLeft = new ConcatableQueue<>();
		ConcatableQueue<E> qRight = new ConcatableQueue<>();

		if (root == null) {
			return qLeft;
		}
		else if (e.compareTo(minNode.ex) < 0 || (e.compareTo(minNode.ex) == 0 && !inclusive)) {
			if (returnLoR == RIGHT) {
				qRight.rootCopy(this);
				this.rootCopy(qLeft);
				return qRight;
			}
			else {
				return qLeft;
			}
		}
		else if (e.compareTo(maxNode.ex) > 0 || (e.compareTo(maxNode.ex) == 0 && inclusive)) {
			if (returnLoR == RIGHT) {
				return qRight;
			}
			else {
				qLeft.rootCopy(this);
				this.rootCopy(qRight);
				return qLeft;
			}
		}
		else {
			Node<E> itr = root;
			while (!itr.isLeaf) {
				if (e.compareTo(itr.leftBranchMax.ex) <= 0) {
					itr = itr.left;
				}
				else {
					itr = itr.right;
				}
			}
			if (e.compareTo(itr.ex) == 0) {
				if (inclusive) {
					e = itr.ex;
				}
				else {
					e = itr.left.ex;
				}
			}
			else if (e.compareTo(itr.ex) < 0) {
				e = itr.left.ex;
			}
			else {
				e = itr.ex;
			}
		}

		qLeft.minNode = this.minNode;
		qRight.maxNode = this.maxNode;
		splitAt(this.root, this.height, e, qLeft, qRight);

		if (returnLoR == RIGHT) {
			this.rootCopy(qLeft);
			return qRight;
		}
		else {
			this.rootCopy(qRight);
			return qLeft;
		}
	}
}