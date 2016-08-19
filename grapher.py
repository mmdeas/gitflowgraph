class Grapher(object):
	"""Uses dot to create graph of labelled commits."""
	def __init__(self, labels):
		super(Grapher, self).__init__()
		self.commits = labels.keys()
		self.labels = labels
		self.graph = None

	def make_graph(self):
		pass

	def render_graph(self, fname, view=False):
		pass

	def get_color(self, label):
		if label == 'development':
			return 'green'
		if label.startswith('fg-'):
			return 'orange'
		if label.startswith('f-'):
			return 'red'
		return 'lightgrey'

	def display_name(self, commit):
		return "{hash}\n{name}".format(hash=commit.hexsha[:8], name=commit.message)#commit.name_rev.split()[-1])
