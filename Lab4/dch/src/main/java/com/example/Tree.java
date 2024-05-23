package com.example;

public class Tree<E extends Comparable<E>>{
	final protected static boolean RED = false;
	final protected static boolean BLACK = true;
	final protected static boolean LEFT = false;
	final protected static boolean RIGHT = true;

	protected Node<E> root;
	protected int size;
	
	public Tree () {
		this.root = null;
		this.size = 0;
	}
	
	protected static <E extends Comparable<E>>  Node<E> rotateLeft (Node<E> n) {
		Node<E> tempNode = n.right;
		boolean tempColor = n.color;
		n.right = tempNode.left;
		n.color = tempNode.color;
		tempNode.left = n;
		tempNode.color = tempColor;
		return tempNode;
	}
	
	protected static <E extends Comparable<E>> Node<E> rotateRight (Node<E> n) {
		Node<E> tempNode = n.left;
		boolean tempColor = n.color;
		n.left = tempNode.right;
		n.color = tempNode.color;
		tempNode.right = n;
		tempNode.color = tempColor;
		return tempNode;
	}

	protected static <E extends Comparable<E>> void flipColors (Node<E> n) {
		n.color = !n.color;
		n.left.color = !n.left.color;
		n.right.color = !n.right.color;
	}
	
	protected static <E extends Comparable<E>> Node<E> fixUpdate (Node<E> n) {
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
				flipColors(n);
			}
		}
		return n;
	}
	
	protected void removeLeaf (Node<E> n) {
		size--;
	}
}