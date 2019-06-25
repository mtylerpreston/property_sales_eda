import numpy as np
import pandas as pd


class Node:

    def __init__(self, node_value, root=node_value, left_child=None, right_child=None):
        self.node_value = node_value
        self.left_child = left_child
        self.right_child = right_child
        self.root = root
