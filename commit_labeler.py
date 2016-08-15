#! /usr/bin/python
from git import Repo

class Labeler(object):
	"""Attempts to guess the branch for commits"""
	def __init__(self, dev_name="development"):
		super(Labeler, self).__init__()
		self.dev_name = dev_name
		self.labels = {}

	def label_commits(self, repo):
		commit = repo.refs[self.dev_name].commit
		self.labels[commit] = set([self.dev_name])
		while commit.parents:
			commit = commit.parents[0]
			self.labels[commit] = set([self.dev_name])

		for ref in (r for r in repo.refs if r.name != self.dev_name):
			commit = ref.commit
			while (commit not in self.labels
					or self.dev_name not in self.labels[commit]):
				if commit not in self.labels:
					self.labels[commit] = set()
				self.labels[commit].add(ref.name)
				commit = commit.parents[0]


if __name__ == '__main__':
	from pprint import pprint
	import sys
	labeler = Labeler()
	repo = Repo(sys.argv[1])
	labeler.label_commits(repo)
	pprint(labeler.labels)
