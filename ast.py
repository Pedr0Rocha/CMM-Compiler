from abc import ABCMeta, abstractmethod
from enum import Enum

class CMMTypes(Enum):
	INT 	= 0;
	STRING 	= 1;
	BOOL 	= 2;

insideLoops = 0;

canBreak():
	return insideLoops == 0;

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

class ProgramTreeNode(TreeNode):

	def evaluate(self):
		return self.data['program'].evaluate();

	def prettyPrintNode(self):
		print "Program Start";
		print self.data['program'].prettyPrintNode();
		print "Program End";

class DecFuncTreeNode(TreeNode):

	def evaluate(self):
		# check symbol table for function ID
		self.data['paramList'].evaluate();
		self.data['block'].evaluate();

	def prettyPrintNode(self):
		print self.data['id'] + " Function Declaration - Type: " + self.data['type'];
		print self.data['paramList'].prettyPrintNode();
		print self.data['block'].prettyPrintNode();

class DecProcTreeNode(TreeNode):

	def evaluate(self):
		# check symbol table for procedure ID
		self.data['paramList'].evaluate();
		self.data['block'].evaluate();

	def prettyPrintNode(self):
		print self.data['id'] + " Procedure Declaration";
		print self.data['paramList'].prettyPrintNode();
		print self.data['block'].prettyPrintNode();

class VarDecTreeNode(TreeNode):

	def evaluate(self):
		# check symbol table for procedure ID
		self.data['varSpecSeq'].evaluate();

	def prettyPrintNode(self):
		print self.data['id'] + " Variable Declaration - Type: " + self.data['type'];
		print self.data['varSpecSeq'].prettyPrintNode();

class VarDecListTreeNode(TreeNode):

	def evaluate(self):
		self.data['varDec'].evaluate();
		self.data['varDecList'].evaluate();

	def prettyPrintNode(self):
		print "Variable Declaration List"
		print self.data['varDec'].prettyPrintNode();
		print self.data['varDecList'].prettyPrintNode();

class ParamTreeNode(TreeNode):

	def evaluate(self):
		# check symbol table for procedure ID
		if (self.data['isVector']):
		else:		

	def prettyPrintNode(self):
		print self.data['id'] + " Parameter - Type: " + self.data['type'] + " isVector: " + self.data['isVector'];

class BlockTreeNode(TreeNode):

	def evaluate(self):
		self.data['varDecList'].evaluate();
		self.data['stmtList'].evaluate();

	def prettyPrintNode(self):
		print "Block"
		print self.data['varDecList'].prettyPrintNode();
		print self.data['stmtList'].prettyPrintNode();

class NumTreeNode(TreeNode):

	def evaluate(self):
		return CMMTypes.INT;

	def prettyPrintNode(self):
		pass;

class StrTreeNode(TreeNode):

	def evaluate(self):
		return CMMTypes.STRING;

	def prettyPrintNode(self):
		pass;

class LogicTreeNode(TreeNode):

	def evaluate(self):
		return CMMTypes.BOOL;

	def prettyPrintNode(self):
		pass;

class ExpressionTreeNode(TreeNode):

	def evaluate(self):
		switch(self.data['op']):
			case 'not':
			case 'ternaryif':

	def prettyPrintNode(self):
		pass;

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
			print "Semantic error at line " + self.data['pos']['line'] + " and column " + self.data['pos']['column'];
			print "Left and right hand operators of binary op don't match";

	def prettyPrintNode(self):
		pass;

class IfTreeNode(TreeNode):

	def evaluate(self):
		expEval = self.data['exp'].evaluate();

		if (expEval != CMMTypes.BOOL):
			print "Sematic error at line " + self.data['pos']['line'] + " and column " + self.data['pos']['column'];
			print "Expression of if statement must be boolean, " + expEval + " found instead."

		self.data['block'].evaluate();

	def prettyPrintNode(self):
		print "If statement begin";
		print self.data['exp'].prettyPrintNode();
		print self.data['block'].prettyPrintNode();
		print "If statement end";

class IfElseTreeNode(TreeNode):

	def evaluate(self):
		expEval = self.data['exp'].evaluate();

		if (expEval != CMMTypes.BOOL):
			print "Sematic error at line " + self.data['pos']['line'] + " and column " + self.data['pos']['column'];
			print "Expression of ifelse statement must be boolean, " + expEval + " found instead."

		self.data['block'].evaluate();
		self.data['blockElse'].evaluate();

	def prettyPrintNode(self):
		print "Ifelse statement begin";
		print self.data['exp'].prettyPrintNode();
		print self.data['block'].prettyPrintNode();
		print self.data['blockElse'].prettyPrintNode();
		print "Ifelse statement end";

class WhileTreeNode(TreeNode):

	def evaluate(self):
		expEval = self.data['exp'].evaluate();

		if (expEval != CMMTypes.BOOL):
			print "Sematic error at line " + self.data['pos']['line'] + " and column " + self.data['pos']['column'];
			print "Expression of while statement must be boolean, " + expEval + " found instead."

		self.data['block'].evaluate();

	def prettyPrintNode(self):
		print "While statement begin";
		print self.data['block'].prettyPrintNode();
		print "While statement end";

class ForTreeNode(TreeNode):

	def evaluate(self):
		expEval = self.data['exp'].evaluate();
		
		self.data['assignInit'].evaluate();

		if (expEval != CMMTypes.BOOL):
			print "Sematic error at line " + self.data['pos']['line'] + " and column " + self.data['pos']['column'];
			print "Expression of for statement must be a boolean, " + expEval + " found instead."

		self.data['assignEnd'].evaluate();
		self.data['block'].evaluate();

	def prettyPrintNode(self):
		print "For statement begin";
		print self.data['assignInit'].prettyPrintNode();
		print self.data['exp'].prettyPrintNode();
		print self.data['assignEnd'].prettyPrintNode();
		print self.data['block'].prettyPrintNode();
		print "For statement end";

class ReadTreeNode(TreeNode):

	def evaluate(self):
		self.data['var'].evaluate();

	def prettyPrintNode(self):
		print "Reading: " + self.data['var'].prettyPrintNode();

class WriteTreeNode(TreeNode):

	def evaluate(self):
		self.data['expList'].evaluate();

	def prettyPrintNode(self):
		print "Writing: " + self.data['var'].prettyPrintNode();

class AssignTreeNode(TreeNode):
	# varEval wont work here
	def evaluate(self):
		varEval = self.data['var'].evaluate();
		expEval = self.data['exp'].evaluate();

		if (self.data['op'] != '='):
			if (varEval == CMMTypes.INT and
				expEval == CMMTypes.INT):
				return CMMTypes.INT;
			else:
				print "Sematic error at line " + self.data['pos']['line'] + " and column " + self.data['pos']['column'];
				print "When using operator " + self.data['op'] + " left and right hand must be type INT."
		else:
			# check variable in symbol table, expEval must be equal to var type

	def prettyPrintNode(self):
		pass;		
