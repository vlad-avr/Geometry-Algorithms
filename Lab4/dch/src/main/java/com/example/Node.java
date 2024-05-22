package com.example;

public class Node<E extends Comparable<E>> {
	final protected static boolean RED = false;
	final protected static boolean BLACK = true;
	protected E ex;
	protected Node<E> left, right, leftBranchMax;
	protected boolean color;
	protected boolean isLeaf;

	public Node() {}
	
	public Node(E e) {
		this.isLeaf = true;
		this.color = BLACK;
		this.ex = e;
		this.leftBranchMax = this;
	}

	public Node(Node<E> lMax, Node<E> left, Node<E> right) {
		this.isLeaf = false;
		this.color = RED;
		this.leftBranchMax = lMax;
		this.left = left;
		this.right = right;
	}
}