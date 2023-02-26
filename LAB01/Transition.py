class Transition(object):
	def __init__(self, nodeFrom,nodeTo,symbol):
		self.nodeFrom = nodeFrom
		self.nodeTo = nodeTo
		self.symbol = symbol
	def __str__(self):
		return "node"+str(self.nodeFrom) + " -> " + "node" + str(self.nodeTo) + " [label = \"" + self.symbol + "\"];"
