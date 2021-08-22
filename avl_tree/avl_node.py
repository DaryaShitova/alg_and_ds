class AVLNode:
    def __init__(self, key=0, elem=None):
        self.key = key
        self.elem = elem
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0

    def to_string(self):
        return "key:" + str(self.key) + ", element: " + str(self.elem)
