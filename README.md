# Convex Hull Algorithms – Graham Scan & Gift Wrapping

This project implements and compares two classic algorithms for computing the **convex hull** of a set of 2D points:

- **Graham Scan** – time complexity **O(n log n)**
- **Gift Wrapping (Jarvis March)** – time complexity **O(n h)** (worst case O(n²), where *h* is the number of hull points)

It supports two execution modes:

- **Performance mode** – runs both algorithms on a given point set and prints execution time and hull size.
- **Visual mode** – plots the points and the convex hulls produced by both algorithms.

---
## Usage

**performance:
	.venv/bin/python convex_hull.py --mode performance --input random --n 10000

**visual:
	.venv/bin/python convex_hull.py --mode visual --input random --n 100

