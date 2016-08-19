import json
from itertools import count

from grapher import Grapher

class D3Grapher(Grapher):
	"""Generate an HTML page with a d3 graph."""
	def __init__(self, labels):
		super(D3Grapher, self).__init__(labels)
		
	def make_graph(self):
		self.graph = {'nodes':[], 'links':[]}
		indexes = {}
		for i, commit in enumerate(sorted(self.commits, key=lambda c: c.authored_date, reverse=True)):
			self.graph['nodes'].append(self._make_node(commit))
			indexes[commit] = i
		for commit in self.commits:
			for parent in commit.parents:
				try:
					self.graph['links'].append(self._make_edge(commit, parent, indexes))
				except KeyError:
					pass

	def render_graph(self, fname, view=False):
		template = file('template.html').read()
		template = template.replace("--DATAHERE--", json.dumps(self.graph))
		groups = sorted(set([g for v in self.labels.values() for g in v]))
		template = template.replace("--GROUPSHERE--", json.dumps(dict(zip(groups, count()))))
		file(fname, 'w').write(template)

	def _make_node(self, commit):
		poss_labels = self.labels[commit].copy()
		poss_labels -= set(['remotes/origin/HEAD', 'HEAD'])
		return {"name": self.display_name(commit), "group": max(poss_labels)}

	def _make_edge(self, commit, parent, indexes):
		return {"source": indexes[parent], "target": indexes[commit], "value": 1}

if __name__ == '__main__':
	import commit_labeler
	import sys
	from git import Repo
	labeler = commit_labeler.Labeler()
	repo = Repo(sys.argv[1])
	labeler.label_commits(repo)
	grapher = D3Grapher(labeler.labels)
	grapher.make_graph()
	grapher.render_graph('test.html', True)
