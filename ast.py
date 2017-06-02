from abc import ABCMeta, abstractmethod
from enum import Enum

class CMMTypes(Enum):
	INT 	= 0;
	STRING 	= 1;
	BOOL 	= 2;

class TreeNode:
	__metaclass__ = ABCMeta

	def __init__(self, data):
		self.data = data;

	def getNodeClass(self):
		return self.__class__.__name__;

	@abstractmethod
	def evaluate(self): pass;

	@abstractmethod
	def prettyPrintNode(self): pass;

class NumTreeNode(TreeNode):

	def evaluate(self):
		return CMMTypes.INT;

	def prettyPrintNode(self):
		pass;

class ExpressionTreeNode(TreeNode):

	def evaluate(self):
		switch(self.data['op']):
			case 'NOT':
			case 'TERNARYIF':

class BinopTreeNode(TreeNode):

	def evaluate(self):
		leftEval = self.data['left'].evaluate();
		rightEval = self.data['right'].evaluate();

		op = self.data['op'];

		if (op == '+' or op == '-' or 
			op == '*' or op == '/' or op == '%'):
			if (leftEval == CMMTypes.INT and rightEval == CMMTypes.INT):
				return CMMTypes.INT;
		elif (op == '&&' or op == '||'):
			if (leftEval == CMMTypes.BOOL and rightEval == CMMTypes.BOOL):
				return CMMTypes.BOOL;
		elif (leftEval == rightEval):
				return leftEval;
		else:
			print "Semantic error at line " + self.data['pos'][0] + " and column " + self.data['pos'][1];


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
