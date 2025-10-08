import math
import random
import time
import argparse
import matplotlib.pyplot as plt


# --------------------------
# Data helpers
# --------------------------
def generate_points(n, xmin=0, xmax=100, ymin=0, ymax=100):
    return [(random.uniform(xmin, xmax), random.uniform(ymin, ymax)) for _ in range(n)]

def load_points_from_file(path):
    with open(path) as f:
        lines = f.read().strip().splitlines()
    n = int(lines[0])
    pts = [tuple(map(float, line.split(','))) for line in lines[1:n+1]]
    return pts


# --------------------------
# Geometry helpers
# --------------------------
def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def distance2(a, b):
    dx, dy = a[0]-b[0], a[1]-b[1]
    return dx*dx + dy*dy


# --------------------------
# Graham Scan  (O(n log n))
# --------------------------
def graham_scan(points):
    pts = sorted(set(points))  # remove duplicates + sort
    if len(pts) <= 1:
        return pts

    # lower hull
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # upper hull
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]


# --------------------------
# Gift Wrapping / Jarvis March (O(n*h))
# --------------------------
def gift_wrapping(points):
    pts = list(set(points))
    if len(pts) <= 1:
        return pts

    # start from leftmost point
    start = min(pts, key=lambda p: (p[0], p[1]))
    hull = []
    p = start
    while True:
        hull.append(p)
        q = pts[0] if pts[0] != p else pts[1]
        for r in pts:
            if q == p or cross(p, q, r) < 0 or (cross(p, q, r) == 0 and distance2(p, r) > distance2(p, q)):
                q = r
        p = q
        if p == start:
            break
    return hull


# --------------------------
# Modes
# --------------------------
def performance_mode(points):
    for name, algo in [("Graham Scan", graham_scan), ("Gift Wrapping", gift_wrapping)]:
        t0 = time.perf_counter()
        hull = algo(points)
        t1 = time.perf_counter()
        print(f"{name:15s}: hull size={len(hull):3d}, time={(t1 - t0)*1000:.2f} ms")

def visual_mode(points):
    plt.scatter(*zip(*points), s=10, label='points')
    for name, algo in [("Graham Scan", graham_scan), ("Gift Wrapping", gift_wrapping)]:
        hull = algo(points)
        hx, hy = zip(*hull + [hull[0]])
        plt.plot(hx, hy, '-o', label=name)
    plt.legend()
    plt.title("Convex Hull")
    plt.savefig("hull.png")
    print("Saved plot to hull.png")
    #plt.show()


# --------------------------
# Main
# --------------------------
def main():
    parser = argparse.ArgumentParser(description="Convex Hull comparison: Graham Scan vs Gift Wrapping")
    parser.add_argument("--mode", choices=["performance", "visual"], required=True,
                        help="Run in performance mode or visual mode")
    parser.add_argument("--input", choices=["random", "file"], default="random",
                        help="Use random points or read from file")
    parser.add_argument("--n", type=int, default=100,
                        help="Number of points if using random")
    parser.add_argument("--path", type=str,
                        help="Path to file if using file input")
    args = parser.parse_args()

    if args.input == "random":
        pts = generate_points(args.n)
    else:
        if not args.path:
            parser.error("--path is required when input=file")
        pts = load_points_from_file(args.path)

    if args.mode == "performance":
        performance_mode(pts)
    else:
        visual_mode(pts)


if __name__ == "__main__":
    main()
