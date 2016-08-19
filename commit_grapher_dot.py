from git import Repo
import graphviz

from grapher import Grapher

class DotGrapher(Grapher):
	"""Uses dot to create graph of labelled commits."""
	def __init__(self, labels):
		super(DotGrapher, self).__init__(labels)

	def make_graph(self):
		self.graph = graphviz.Digraph('G', filename='test.gv')

		print sorted(set(l for ls in self.labels.values() for l in ls))
		subgraphs = {}
		for label in set(l for ls in self.labels.values() for l in ls):
			lsub = graphviz.Digraph("cluster_"+label)
			lsub.body.append('style=filled')
			lsub.body.append('color={color}'.format(color=self.get_color(label)))
			lsub.body.append('label="{0}"'.format(label))
			lsub.node_attr.update(style='filled', color='white')
			# lsub.body.append('rank = same')
			subgraphs[label] = lsub

		for commit in self.commits:
			subgraphs[max(self.labels[commit])].node(self.display_name(commit))
		for commit in self.commits:
			for parent in commit.parents:
				if parent in self.labels:
					self.graph.edge(self.display_name(parent), self.display_name(commit))
		for subgraph in subgraphs.values():
			self.graph.subgraph(subgraph)

	def render_graph(self, fname, view=False):
		self.graph.render(fname, view=view)

if __name__ == '__main__':
	import commit_labeler
	import sys
	labeler = commit_labeler.Labeler()
	repo = Repo(sys.argv[1])
	labeler.label_commits(repo)
	grapher = DotGrapher(labeler.labels)
	grapher.make_graph()
	print grapher.graph.source
	grapher.render_graph('test.gv', True)
