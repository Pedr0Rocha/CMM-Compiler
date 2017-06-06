from abc import ABCMeta, abstractmethod
from enum import Enum
import helpers

def semanticError(pos):
	print "Semantic error at line " + pos['line'] + " and column " + pos['column'];

class CMMTypes(Enum):
	INT 			= 0;
	STRING 			= 1;
	BOOL 			= 2;
	ARRAY_INT 		= 3;
	ARRAY_STRING 	= 4;
	ARRAY_BOOL 		= 5;

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

class SimpleVarDecTreeNode(TreeNode):

	def evaluate(self):
		pass;

	def prettyPrintNode(self):
		pass;

class VarDecTreeNode(TreeNode):

	def evaluate(self):
		self.data['varSpecSeq'].evaluate();

	def prettyPrintNode(self):
		print "Variable Declaration - Type: " + self.data['type'];
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
			pass;
		else:
			pass;	

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
		if (self.data['op'] == 'not'):
			pass;
		elif (self.data['op'] == 'ternaryif'):
			pass;

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
			semanticError(self.data['pos']);
			print "Left and right hand operators of binary op don't match";

	def prettyPrintNode(self):
		pass;

class IfTreeNode(TreeNode):

	def evaluate(self):
		expEval = self.data['exp'].evaluate();

		if (expEval != CMMTypes.BOOL):
			semanticError(self.data['pos']);
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
			semanticError(self.data['pos']);
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
			semanticError(self.data['pos']);
			print "Expression of while statement must be boolean, " + expEval + " found instead."

		helpers.insideLoops += 1;
		self.data['block'].evaluate();
		helpers.insideLoops -= 1;

	def prettyPrintNode(self):
		print "While statement begin";
		print self.data['block'].prettyPrintNode();
		print "While statement end";

class ForTreeNode(TreeNode):

	def evaluate(self):
		expEval = self.data['exp'].evaluate();
		
		self.data['assignInit'].evaluate();

		if (expEval != CMMTypes.BOOL):
			semanticError(self.data['pos']);
			print "Expression of for statement must be a boolean, " + expEval + " found instead."

		self.data['assignEnd'].evaluate();
		helpers.insideLoops += 1;
		self.data['block'].evaluate();
		helpers.insideLoops -= 1;

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
				semanticError(self.data['pos']);
				print "When using operator " + self.data['op'] + " left and right hand must be type INT."
		else:
			pass;
			# check variable in symbol table, expEval must be equal to var type

	def prettyPrintNode(self):
		pass;	

class IDTreeNode(TreeNode):
	
	def evaluate(self):
		idType = helpers.getVariableType(self.data['id']);

		if (idType == False):
			semanticError(self.data['pos']);
			print "Variable " + self.data['id'] + " not declared.";
		else:
			return idType;

	def prettyPrintNode(self):
		pass;

class IDVectorTreeNode(TreeNode):
	
	def evaluate(self):
		idType = helpers.getVariableType(self.data['id']);
		expEval = self.data['exp'].evaluate();

		if (idType == False):
			semanticError(self.data['pos']);
			print "Variable " + self.data['id'] + " not declared";
		elif (expEval != CMMTypes.INT):
			semanticError(self.data['pos']);
			print "Invalid index of vector " + self.data['id'];
		else:
			if (idType == CMMTypes.ARRAY_BOOL):
				return CMMTypes.BOOL;
			elif (idType == CMMTypes.ARRAY_STRING):
				return CMMTypes.STRING;
			else:
				return CMMTypes.INT;

	def prettyPrintNode(self):
		pass;

class SubCallTreeNode(TreeNode):

	def evaluate(self):
		pass;

	def prettyPrintNode(self):
		pass;

class DecSeqTreeNode(TreeNode):

	def evaluate(self):
		return self.data['dec'].evaluate();

	def prettyPrintNode(self):
		print "Sequence of declarations";
		print self.data['dec'].prettyPrintNode();
