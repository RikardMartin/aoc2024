#%%
import numpy as np
from collections import defaultdict


#%%
with open('testinput.txt') as f:
    data = f.readlines()

data = [line[:-1] for line in data]
data

len_x = len(data[0])+2
max_x = len_x - 1
len_y = len(data)+2
max_y = len_y - 1
matrix = np.empty( (len_y, len_x), dtype='str')
# plants = set()

for idy in range(1,len_y-1):
    for idx in range(1,len_x-1):
        # print(idx,idy)
        matrix[idy, idx] = data[idy-1][idx-1]
        # plants.add(data[idy-1][idx-1])
# matrix[1:-1,1:-1] = data

print(matrix)
print(matrix.shape)
# print(plants)
#%%
def find_region(iy, ix, symbol, pruned_garden, direction=None):
    global area, perimeter
    """
    """
    # print("checking node", (iy, ix), "for symbol", symbol, "with area as", area)
    if pruned_garden[iy, ix]==symbol:
        area += 1
        pruned_garden[iy, ix] = ''
        coords.add((iy, ix))
        
        # print("found plant", symbol, "at", (iy, ix), "with area", area, "and perimeter", perimeter)

        find_region(iy, ix+1, symbol, pruned_garden, direction='right')
        find_region(iy+1, ix, symbol, pruned_garden, direction='down')
        find_region(iy, ix-1, symbol, pruned_garden, direction='left')
        find_region(iy-1, ix, symbol, pruned_garden, direction='up')


def direction(vA, vB):
    """ Return (dy, dx) from vA to vB. """
    (yA, xA) = vA
    (yB, xB) = vB
    return (yB - yA, xB - xA)

def find_perimeter():
    """
    walk through region matrix. row by row from left to right
        if current node is not symbol, continue.
        at current point, for each direction that doesnt have symbol in it.
            if right or left:
                if up is symbol, mark direction as perimeter
            if up or down:
                if left is symbol, mark that direction as perimeter.
        else continue.
        TODO: handle edges and corners (outside loop)
    """
    pass


def compute_region_perimeter(coords_set):
    """
    Build a boundary graph, then trace out all loops (outer boundary plus holes).
    For each loop, we count how many *straight segments* it has, and then sum
    all loops to get the final perimeter.

    Return the total perimeter for this region.
    """

    # ----------------------------------------------------------------------
    # 1) BUILD A SET OF 'BOUNDARY' EDGES (undirected)
    # ----------------------------------------------------------------------
    # For each cell in coords_set, check if that cell's top/bottom/left/right
    # is out of region. If yes, that side is part of the boundary.
    # We represent an edge by a pair of "grid vertices" in (y,x) space.
    # e.g. top edge of cell (y, x) goes from (y, x) to (y, x+1).
    #
    # We'll store them as *undirected* edges in a set, each edge is a frozenset
    # of the 2 endpoints: frozenset({v1, v2}).
    # ----------------------------------------------------------------------
    edges_undirected = set()

    for (cy, cx) in coords_set:
        # top edge
        if (cy-1, cx) not in coords_set:
            v1 = (cy, cx)
            v2 = (cy, cx+1)
            edges_undirected.add(frozenset([v1, v2]))

        # bottom edge
        if (cy+1, cx) not in coords_set:
            v1 = (cy+1, cx)
            v2 = (cy+1, cx+1)
            edges_undirected.add(frozenset([v1, v2]))

        # left edge
        if (cy, cx-1) not in coords_set:
            v1 = (cy, cx)
            v2 = (cy+1, cx)
            edges_undirected.add(frozenset([v1, v2]))

        # right edge
        if (cy, cx+1) not in coords_set:
            v1 = (cy, cx+1)
            v2 = (cy+1, cx+1)
            edges_undirected.add(frozenset([v1, v2]))

    # ----------------------------------------------------------------------
    # 2) CONVERT TO DIRECTED EDGES AND BUILD ADJACENCY
    #
    # For each undirected edge {v1,v2}, we create 2 directed edges:
    # v1->v2 and v2->v1. We'll store them in adjacency[v1].append(v2).
    # ----------------------------------------------------------------------
    from collections import defaultdict
    adjacency = defaultdict(list)

    for undirected_edge in edges_undirected:
        (v1, v2) = tuple(undirected_edge)
        adjacency[v1].append(v2)
        adjacency[v2].append(v1)

    # ----------------------------------------------------------------------
    # 3) FIND ALL LOOPS in this boundary graph by picking unvisited *directed*
    #    edges and doing a *clockwise* walk around the boundary.
    #
    #    We'll keep a separate 'visited_edges' set of directed edges (vA->vB).
    #    Each time we find a loop, we do a boundary walk. Then we count direction
    #    changes => number of segments.
    # ----------------------------------------------------------------------
    visited_edges = set()

    def edge_key(vA, vB):
        # store a directed edge as a tuple
        return (vA, vB)

    # We'll define 4 possible direction vectors for the grid:
    # up, right, down, left, in clockwise order.
    directions_cw = [(-1,0), (0,1), (1,0), (0,-1)]

    def direction_of(vA, vB):
        # Return one of the direction vectors from vA to vB
        yA, xA = vA
        yB, xB = vB
        return (yB - yA, xB - xA)  # should be in {(-1,0),(0,1),(1,0),(0,-1)} if perfect grid

    # A small helper to find the index of a direction in directions_cw
    def dir_index(d):
        return directions_cw.index(d)

    # A function that picks the next vertex in a consistent clockwise boundary walk.
    # We'll do a "turn right if we can, else go straight, else turn left, else turn around" approach.
    # Because we are on a grid, we always can find a direction in directions_cw.
    def pick_next_vertex(curr_vertex, old_dir):
        """
        Among adjacency[curr_vertex], pick the neighbor that is
        the 'most right' turn from old_dir in clockwise sense.
        This ensures we follow the boundary in a consistent loop.
        """
        # We'll build an ordering of directions in preference order:
        # 'right turn' is 1 step forward in the directions_cw list.
        # For example, if old_dir is directions_cw[i], then:
        #    "right" is directions_cw[(i+1) % 4]
        #    "straight" is directions_cw[i]
        #    "left" is directions_cw[(i-1) % 4]
        #    "back" is directions_cw[(i+2) % 4]
        i = dir_index(old_dir)
        candidates = [
            directions_cw[(i+1) % 4],  # right
            directions_cw[i],          # straight
            directions_cw[(i-1) % 4],  # left
            directions_cw[(i+2) % 4],  # back
        ]

        # Among adjacency[curr_vertex], we pick the first neighbor that matches
        # one of these directions in that order of preference.
        neighbors = adjacency[curr_vertex]
        for d in candidates:
            next_vertex = (curr_vertex[0] + d[0], curr_vertex[1] + d[1])
            if next_vertex in neighbors:
                return (next_vertex, d)

        # Should not happen if the boundary is consistent, but just in case:
        return (curr_vertex, (0,0))

    def walk_one_loop(start_vA, start_vB):
        """
        Given a directed edge (start_vA -> start_vB),
        walk the boundary *clockwise* until we come back to (start_vA->start_vB).
        Return the count of direction changes (segments) for this loop.

        We'll mark each traversed directed edge as visited in visited_edges.
        """
        loop_dir = direction_of(start_vA, start_vB)
        old_dir = loop_dir
        seg_count = 1  # Starting out, we have one segment.

        curr_vA = start_vA
        curr_vB = start_vB
        visited_edges.add(edge_key(curr_vA, curr_vB))

        while True:
            # Move forward: current edge is (curr_vA -> curr_vB).
            # Next step: from curr_vB, pick the neighbor that forms
            # the 'most right' direction from old_dir.
            next_v, new_dir = pick_next_vertex(curr_vB, old_dir)

            if new_dir != old_dir:
                seg_count += 1
                old_dir = new_dir

            visited_edges.add(edge_key(curr_vB, next_v))

            curr_vA, curr_vB = curr_vB, next_v

            # Check if we've come back to the start edge
            if (curr_vA == start_vA) and (curr_vB == start_vB):
                break

        return seg_count
     
    total_segments = 0

    # We'll find all loops by scanning through adjacency. For each vertex vA,
    # for each neighbor vB, that's a possible directed edge (vA->vB). If it's not visited,
    # we do walk_one_loop(...) to follow it around a boundary loop. Then we add
    # that loop's segment count to total_segments.
    for vA in adjacency:
        for vB in adjacency[vA]:
            ekey = edge_key(vA, vB)
            if ekey not in visited_edges:
                # We'll walk that loop
                loop_segments = walk_one_loop(vA, vB)
                total_segments += loop_segments

    return total_segments



pruned_garden = matrix.copy()
total_price = 0

for idy in range(1,len_y-1):
    for idx in range(1,len_x-1):

        area = 0
        coords = set()
        symbol = pruned_garden[idy, idx]
        if symbol!='':
            find_region(idy, idx, symbol, pruned_garden)
            perimeter = compute_region_perimeter(coords) - 1

            total_price += area*perimeter
            print("plant:", symbol, ", area:", area, ", perimeter:", perimeter)


print("total price:", total_price)
# %%
