#%%

import sys
sys.setrecursionlimit(10**7)

# Example matrix as a list of strings
lines = [
    "RRRRIICCFF",
    "RRRRIICCCF",
    "VVRRRCCFFF",
    "VVRCCCJFFF",
    "VVVVCJJCFE",
    "VVIVCCJJEE",
    "VVIIICJJEE",
    "MIIIIIJJEE",
    "MIIISIJEEE",
    "MMMISSJEEE",
]
with open('input.txt') as f:
    data = f.readlines()

lines = [line[:-1] for line in data]


# Convert to a 2D list (matrix[y][x])
matrix = [list(row) for row in lines]
nrows = len(matrix)
ncols = len(matrix[0])

# We'll keep track of visited cells using a separate 2D list of booleans.
visited = [[False]*ncols for _ in range(nrows)]

def in_bounds(y, x):
    return 0 <= y < nrows and 0 <= x < ncols

def find_region(iy, ix, symbol, region_coords):
    """
    Recursive DFS that collects all coordinates belonging to the region
    of `symbol` that includes (iy, ix).
    """
    # Mark visited
    visited[iy][ix] = True
    region_coords.append((iy, ix))

    # Explore neighbors (up, down, left, right)
    for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
        ny, nx = iy + dy, ix + dx
        if in_bounds(ny, nx):
            if not visited[ny][nx] and matrix[ny][nx] == symbol:
                find_region(ny, nx, symbol, region_coords)

def compute_region_perimeter(coords_set):
    """
    Compute the 'merged' outer boundary perimeter for a set of grid cells
    that form a single connected region.

    Strategy (outline):
      1) Gather all 'boundary edges' in an (undirected) set. Each edge
         is between grid vertices. We represent an edge by two endpoints
         in a sorted tuple so we don’t double-count.

      2) Pick one boundary edge, then 'walk' clockwise (or counter-clockwise)
         around the shape until we return to the start. Keep track of
         direction changes to count segments.

      3) The final perimeter is the number of line segments in that boundary walk.

    For your puzzle examples, this yields:
      - 2x2 block => perimeter = 4
      - 'FFF / FF / F' L-shape => perimeter = 8
    """
    # Step 1: Build a set of boundary edges (vertical and horizontal).
    # An 'edge' here is between two adjacent grid "vertex" points in the 2D plane.
    # We'll store edges as a pair of coordinate pairs, e.g. ((y1,x1), (y2,x2)),
    # always sorted so that edge (A,B) = edge (B,A).

    edges = set()
    for (y, x) in coords_set:
        # For each of the 4 possible edges around cell (y,x),
        # check if that edge goes out-of-region:
        #
        # The "square" cell (y, x) can be thought of as having 4 edges:
        #   top edge between (y,x) in "vertex" space and (y,x+1)
        #   bottom edge between (y+1,x) and (y+1,x+1)
        #   left edge between (y,x) and (y+1,x)
        #   right edge between (y,x+1) and (y+1,x+1)
        #
        # But we only add an edge to the boundary if the adjacent cell
        # is not in coords_set (or is out of bounds).
        #
        # We'll check "up" vs "down" in cell terms, which corresponds to
        # "top edge" vs "bottom edge" in vertex terms, etc.

        # 1) Top edge check: is the neighbor cell above out-of-region?
        if not ((y-1, x) in coords_set):
            # The top edge in 'vertex' coordinates:
            v1 = (y, x)
            v2 = (y, x+1)
            edge = tuple(sorted([v1, v2]))
            edges.add(edge)

        # 2) Bottom edge: neighbor below out-of-region?
        if not ((y+1, x) in coords_set):
            v1 = (y+1, x)
            v2 = (y+1, x+1)
            edge = tuple(sorted([v1, v2]))
            edges.add(edge)

        # 3) Left edge: neighbor to the left out-of-region?
        if not ((y, x-1) in coords_set):
            v1 = (y, x)
            v2 = (y+1, x)
            edge = tuple(sorted([v1, v2]))
            edges.add(edge)

        # 4) Right edge: neighbor to the right out-of-region?
        if not ((y, x+1) in coords_set):
            v1 = (y, x+1)
            v2 = (y+1, x+1)
            edge = tuple(sorted([v1, v2]))
            edges.add(edge)

    # Step 2: We want to walk the boundary edges in a loop, counting
    # how many 'straight' segments there are.  We'll do a standard
    # polygon-walk: pick one edge, find which edge is connected to it,
    # etc., until we return.

    # Convert edges to adjacency of 'vertices' in the plane.
    # For each vertex, keep track of which other vertices it's connected to.
    from collections import defaultdict
    adj = defaultdict(list)
    for (v1, v2) in edges:
        adj[v1].append(v2)
        adj[v2].append(v1)

    # To do a boundary trace, we need to find an actual loop in terms of edges.
    # - First, we pick a "start vertex" with a small (y, x) to keep it consistent.
    start_vertex = min(adj.keys())

    # - Then, among the neighbors of start_vertex, pick the next vertex in a consistent ordering
    #   so that we traverse around the polygon consistently. We'll do a simple "sort" by coordinates
    #   or something that heads 'clockwise/counter-clockwise'.
    #   Because we are on a grid, we can just pick the neighbor that is "most to the left" or so.
    #   A robust approach is: pick the neighbor that is, say, the minimum by (dx,dy) direction.
    #
    # We'll do a quick helper that tries to step clockwise around the boundary from one edge to the next.
    # Then we'll track direction changes.

    def direction(vA, vB):
        """ Return (dy, dx) from vA to vB. """
        (yA, xA) = vA
        (yB, xB) = vB
        return (yB - yA, xB - xA)

    # We’ll define a small function to get the "next boundary vertex" given
    # we arrived at vertex current from prev, and want to pick the next among adj[current].
    #
    # Because this is a grid, each vertex should have 2 boundary-adjacent edges (the region boundary is a loop),
    # except for corners that might have more if the region is not a simple rectangle. However, a single connected
    # boundary loop in a grid typically has exactly 2 edges per vertex in this representation. If you get a vertex
    # with more than 2 neighbors, there's a ‘T-junction’ in the boundary (which can happen with holes, etc.).
    #
    # For a single simply connected region (no holes), each boundary vertex should have 2 neighbors. We'll pick the
    # neighbor that is *not* `prev`.

    def next_vertex(prev, current):
        neighbors = adj[current]
        if len(neighbors) == 1:
            # A 'dead end' - theoretically shouldn't happen on a closed boundary,
            # unless there's an odd shape. We'll just return the same neighbor to break.
            return neighbors[0]
        elif len(neighbors) == 2:
            # Typical for a well-formed boundary loop. Return the one that's not `prev`.
            return neighbors[0] if neighbors[1] == prev else neighbors[1]
        else:
            # If there's more, pick any that isn't `prev`. In a well-formed loop,
            # you might have a 'corner' with multiple edges. We'll pick the next *clockwise*
            # by sorting direction or something. For simplicity, just pick anything != prev.
            for nb in neighbors:
                if nb != prev:
                    return nb

    # Start walking
    # We'll pick the next vertex by sorting the adjacency to ensure consistent direction.
    possible_starts = adj[start_vertex]
    if not possible_starts:
        # Means region has 0 boundary edges for some weird reason...
        return 0

    next_v = min(possible_starts)  # pick the smallest coordinate as next
    visited_path = [(start_vertex, next_v)]  # store edges in order
    seg_count = 1  # We'll start with 1 segment.

    prev = start_vertex
    curr = next_v
    old_dir = direction(prev, curr)

    # We'll continue walking edges until we come back to (start_vertex, next_v).
    while True:
        nv = next_vertex(prev, curr)
        new_dir = direction(curr, nv)
        if new_dir != old_dir:
            seg_count += 1
            old_dir = new_dir

        visited_path.append((curr, nv))
        prev, curr = curr, nv

        # If we've looped back to the first edge, we are done.
        if (prev, curr) == (start_vertex, next_v):
            break

    return seg_count

# ---------------------------------------------------------

total_price = 0

for y in range(nrows):
    for x in range(ncols):
        if not visited[y][x]:
            symbol = matrix[y][x]
            current_region_coords = []
            find_region(y, x, symbol, current_region_coords)
            
            # area = number of cells in region
            area = len(current_region_coords)

            # perimeter = boundary trace count
            coords_set = set(current_region_coords)
            perimeter = compute_region_perimeter(coords_set) - 1

            total_price += area * perimeter
            print(f"Found region '{symbol}', area={area}, perimeter={perimeter}")

print(f"\nTotal price = {total_price}")
