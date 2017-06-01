from abc import ABCMeta, abstractmethod

class TreeNode:
	__metaclass__ = ABCMeta

	def __init__(self, data, children):
		self.data = data;
		self.children = children;

	def getType(self):
		return self.__class__.__name__;

	@abstractmethod
	def evaluate(self): pass;

	@abstractmethod
	def prettyPrintNode(self): pass;


class ProgramTreeNode(TreeNode):

	def evaluate(self):
		return True;

	def prettyPrintNode(self):
		print "Program";
		print self.children[0].prettyPrintNode();

class IfTreeNode(TreeNode):

	def evaluate(self):
		if (self.children[0].evaluate() == True or self.children[0].evaluate() == False):
			return True;
		return False;

	def prettyPrintNode(self):
		print "If stmt";
		print self.children[0].prettyPrintNode();
		print self.children[1].prettyPrintNode();

class BlockTreeNode(TreeNode):

	def evaluate(self):
		return True;

	def prettyPrintNode(self):
		print self.getType();

class ExpressionTreeNode(TreeNode):

	def evaluate(self):
		return True;

	def prettyPrintNode(self):
		print self.getType();


ifnode = IfTreeNode(None, [BlockTreeNode(None, []), ExpressionTreeNode(None, [])]);

print ifnode.prettyPrintNode();
