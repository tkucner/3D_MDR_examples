import helpers as he


class OctTree:
    class OctNode:
        def __init__(self):
            self.corners = []
            self.children = []
            self.points = []
            self.oct_id = -1
            self.parent = []
            self.leaf = False

    def __init__(self, points, point_threshold):

        self.point_threshold = point_threshold

        self.corners = he.compute_max_cube(points)
        self.tree = []
        self.points = points
        new_root = self.OctNode()
        new_root.corners = self.corners
        new_root.points = points
        new_root.oct_id = 0
        new_root.parent = -1
        self.tree.append(new_root)

    def build_tree(self):
        explore = True
        while explore:
            explore = False
            for node in self.tree:
                if not node.leaf and len(node.children) == 0:
                    explore = True
                    self.attempt_split(node)

    def attempt_split(self, node):
        sub_cubes = he.divide_cube(node.corners)
        attempted_nodes = []
        children_ids = []
        for sc_id, sc_corners in sub_cubes.items():
            att_node = self.OctNode()
            att_node.corners = sc_corners
            att_node.parent = node.oct_id
            att_node.oct_id = self.tree[-1].oct_id + 1 + sc_id
            children_ids.append(self.tree[-1].oct_id + 1 + sc_id)
            points_in, points_count = he.in_cube(node.points, sc_corners)
            if points_count < self.point_threshold:
                att_node.leaf = True
            att_node.points = points_in
            attempted_nodes.append(att_node)
        self.tree.extend(attempted_nodes)
        node.children = children_ids
