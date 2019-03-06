from misc import *

class Entry:
	def __init__(self, lexeme, token):
		self.lexeme = lexeme
		self.token  = token

	def __repr__(self):
		return str(self.lexeme) + '\t' + str(self.token)

class Symbtab:
	def __init__(self):
		self.entries = [Entry("println", PRINTLN)]

	def __repr__(self):
		sep = "\n--------------------------"
		res = "@\tlexeme\ttoken" + sep + "\n"
		p = 0
		for e in self.entries:
			res = res + str(p) + '\t' + str(e) + '\n'
			p = p + 1
		return res

	def lookup(self, lexeme):
		p = 0
		for e in self.entries:
			if e.lexeme == lexeme: return p
			else: p = p + 1
			return None

	def insert(self, lexeme, token):
		p = self.lookup(lexeme)
		if p is None:
			self.entries.append(Entry(lexeme, token))
			return len(self.entries) - 1
		else:
			return p

	def gettoken(self, p):
		return self.entries[p].token
