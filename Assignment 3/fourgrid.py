class FourGrid(object):
	"""A random (solvable) four-connected grid. If you're so inclined, you can implement A* for this class as well.
	The distance between any two cells (if they are connected) is one. We recommend using euclidean distance (or
	something similar) for your heuristic.
	You _do not_ need to implement this for this homework; it's just here if you're gung-ho."""
	def __init__(self, rows, cols, seed=0):
		super(FourGrid, self).__init__()
		self.rows, self.cols = rows, cols
		self.seed = seed
	
	def __repr__(self):
		return ""

	def __str__(self):
		return ""

	def __getitem__(self, key):
	"""Pass in a (row, col) tuple to get a particular cell in this map."""
		return None

class _GridNode(object):
	"""docstring for _GridNode"""
	def __init__(self):
		super(_GridNode, self).__init__()