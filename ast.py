from abc import ABCMeta, abstractmethod
from enum import Enum
import helpers

# TODO
# Check precedences, expressions not working without parenthesis
# Implement BreakTreeNode to 'for' and 'while'
# Implement SubCallNode
# Make a generic sequence tree node - SeqTreeNode

def semanticError(pos):
	print "Semantic error at line " + str(pos['line']) + " and column " + str(pos['column']);

def getCMMType(varType):
    if (varType == 'int'):
    	return CMMTypes.INT;
    if (varType == 'string'):
    	return CMMTypes.STRING;
    if (varType == 'bool'):
    	return CMMTypes.BOOL;
    if (varType == 'array_int'):
    	return CMMTypes.ARRAY_INT;
    if (varType == 'array_string'):
    	return CMMTypes.ARRAY_STRING;
    if (varType == 'array_bool'):
    	return CMMTypes.ARRAY_BOOL;

def getCMMTypeName(num):
	if (num == 0):
		return "INT";
	elif (num == 1):
		return "STRING";
	elif (num == 2):
		return "BOOL";
	elif (num == 3):
		return "ARRAY_INT";
	elif (num == 4):
		return "ARRAY_STRING";
	elif (num == 5):
		return "ARRAY_BOOL";

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
	def printNode(self): pass;

class ProgramTreeNode(TreeNode):

	def evaluate(self):
		self.data['program'].evaluate();

	def printNode(self):
		print "Program Start";
		self.data['program'].printNode();
		print "Program End";

class DecSeqTreeNode(TreeNode):

	def evaluate(self):
		self.data['dec'].evaluate();
		if (self.data.has_key('decSeq')):
			self.data['decSeq'].evaluate();

	def printNode(self):
		print "Sequence of declarations";
		self.data['dec'].printNode();
		if (self.data.has_key('decSeq')):
			self.data['decSeq'].printNode();

class ExpSeqTreeNode(TreeNode):

	def evaluate(self):

		self.data['exp'].evaluate();
		if (self.data.has_key('expSeq')):
			self.data['expSeq'].evaluate();

	def printNode(self):
		print "Sequence of declarations";
		self.data['exp'].printNode();
		if (self.data.has_key('expSeq')):
			self.data['expSeq'].printNode();

class DecFuncTreeNode(TreeNode):

	def evaluate(self):
		if (helpers.canCreateFuncOrProc(self.data['id'])):
			if (self.data['paramList'] != None):
				self.data['paramList'].evaluate();
			data = {
				'name' 	 	 : self.data['id'],
				'type' 	 	 : self.data['type'],
				'paramTypes' : [],
			}
			helpers.addFunction(data);
			helpers.currentScope = helpers.currentScope + 1;
			helpers.currentFunc = self.data['type'];
			self.data['block'].evaluate();
			helpers.currentScope = helpers.currentScope - 1;
			helpers.currentFunc = None;

	def printNode(self):
		self.data['id'] + " Function Declaration - Type: " + self.data['type'];
		if (self.data['paramList'] != None):
			self.data['paramList'].printNode();
		self.data['block'].printNode();

class DecProcTreeNode(TreeNode):

	def evaluate(self):
		if (helpers.canCreateFuncOrProc(self.data['id'])):
			if (self.data['paramList'] != None):
				self.data['paramList'].evaluate();
			data = {
				'name'		 : self.data['id'],
				'paramTypes' : [],
			}
			helpers.addProcedure(data);
			helpers.currentScope = helpers.currentScope + 1;
			helpers.currentProc = self.data['id'];
			self.data['block'].evaluate();
			helpers.currentScope = helpers.currentScope - 1;
			helpers.currentProc = None;

	def printNode(self):
		print self.data['id'] + " Procedure Declaration";
		if (self.data['paramList'] != None):
			self.data['paramList'].printNode();
		self.data['block'].printNode();

class VarDecTreeNode(TreeNode):

	def evaluate(self):
		helpers.currentType = self.data['type'];
		self.data['varSpecSeq'].evaluate();

	def printNode(self):
		self.data['varSpecSeq'].printNode();

class VarDecListTreeNode(TreeNode):

	def evaluate(self):
		if (self.data.has_key('varDec')):
			if (self.data['varDec'] != None):
				self.data['varDec'].evaluate();

		if (self.data.has_key('varDecList')):
			if (self.data['varDecList'] != None):
				self.data['varDecList'].evaluate();

	def printNode(self):
		print "Variable Declaration List";
		self.data['varDec'].printNode();
		self.data['varDecList'].printNode();

class StmtListTreeNode(TreeNode):

	def evaluate(self):
		if (self.data.has_key('stmt')):
			if (self.data['stmt'] != None):
				self.data['stmt'].evaluate();

		if (self.data.has_key('stmtList')):
			if (self.data['stmtList'] != None):
				self.data['stmtList'].evaluate();

	def printNode(self):
		print "Statements List";
		self.data['stmt'].printNode();
		self.data['stmtList'].printNode();

class LiteralSeqTreeNode(TreeNode):

	def evaluate(self):
		self.data['lit'].evaluate();
		if (self.data.has_key('litSeq')):
			self.data['litSeq'].evaluate();

	def printNode(self):
		self.data['lit'].printNode();
		if (self.data.has_key('litSeq')):
			self.data['litSeq'].printNode();
		
class VarSeqTreeNode(TreeNode):

	def evaluate(self):
		self.data['var'].evaluate();
		if (self.data.has_key('varSeq')):
			self.data['varSeq'].evaluate();

	def printNode(self):
		self.data['var'].printNode();
		if (self.data.has_key('varSeq')):
			self.data['varSeq'].printNode();

class ParamSeqTreeNode(TreeNode):

	def evaluate(self):
		# param is vector[id, type]
		# TODO check same name params
		param = self.data['param'].evaluate();
		helpers.currentParams.append(param);
		if (self.data.has_key('paramSeq')):
			self.data['paramSeq'].evaluate();

	def printNode(self):
		self.data['param'].printNode();
		if (self.data.has_key('paramSeq')):
			self.data['paramSeq'].printNode();

class SeqTreeNode(TreeNode):

	def evaluate(self):
		self.data['base'].evaluate();
		if (self.data.has_key('seq')):
			self.data['seq'].evaluate();

	def printNode(self):
		self.data['base'].printNode();
		if (self.data.has_key('seq')):
			self.data['seq'].printNode();

class VarTreeNode(TreeNode):

	def evaluate(self):
		if (helpers.canCreateVar(self.data['id'])):
			addVar = True;

			if (self.data.has_key('literal')):
				literalEval = self.data['literal'].evaluate();
				currentTypeCMM = getCMMType(helpers.currentType);
				if (currentTypeCMM != literalEval):
					semanticError(self.data['pos']);
					print "Wrong type assigned to variable '" + self.data['id'] + "'. Expecting " + getCMMTypeName(currentTypeCMM) + ", found " + getCMMTypeName(literalEval) + ".\n";
					addVar = False;

			if (self.data.has_key('size')):
				if (self.data.has_key('literalSeq')):
					literalSeqEval = self.data['literalSeq'].evaluate();
					if (getCMMType("array_" + helpers.currentType) != literalSeqEval):
						semanticError(self.data['pos']);
						print "Wrong type assigned to vector. Expecting array of " + helpers.currentType + ".\n";
						addVar = False;

			if (addVar):
				helpers.addOrUpdateSymbol(self.data['id'], helpers.currentType);
		else:
			semanticError(self.data['pos']);
			print "Variable '" + self.data['id'] + "' already defined on the same scope\n";

	def printNode(self):
		print self.data['id'] + " variable declaration";

class ParamTreeNode(TreeNode):

	def evaluate(self):
		paramType = self.data['type'];
		if (self.data['isVector']):
			if (paramType == 'int'):
				return [self.data['id'], "array_int"];
			elif (paramType == 'str'):
				return [self.data['id'], "array_str"];
			elif (paramType == 'bool'):
				return [self.data['id'], "array_bool"];
		else:
			return [self.data['id'], paramType];	

	def printNode(self):
		print self.data['id'] + " Parameter - Type: " + self.data['type'] + " isVector: " + str(self.data['isVector']);

class BlockTreeNode(TreeNode):

	def evaluate(self):
		helpers.addNewScope();
		if (self.data['varDecList'] != None):
			self.data['varDecList'].evaluate();
		if (self.data['stmtList'] != None):
			self.data['stmtList'].evaluate();
		helpers.removeScope();

	def printNode(self):
		print "Block"
		self.data['varDecList'].printNode();
		self.data['stmtList'].printNode();

class NumTreeNode(TreeNode):

	def evaluate(self):
		return CMMTypes.INT;

	def printNode(self):
		pass;

class StrTreeNode(TreeNode):

	def evaluate(self):
		return CMMTypes.STRING;

	def printNode(self):
		pass;

class LogicTreeNode(TreeNode):

	def evaluate(self):
		return CMMTypes.BOOL;

	def printNode(self):
		pass;

class ExpressionTreeNode(TreeNode):

	def evaluate(self):
		if (self.data['op'] == 'not'):
			pass;
		elif (self.data['op'] == 'ternaryif'):
			pass;

	def printNode(self):
		pass;

class BinopTreeNode(TreeNode):

	def evaluate(self):
		leftEval = self.data['left'].evaluate();
		rightEval = self.data['right'].evaluate();

		op = self.data['op'];

		if (not isinstance(leftEval, int)):
			leftEval = getCMMType(leftEval);
		if (not isinstance(rightEval, int)):
			rightEval = getCMMType(rightEval);

		if (op == '+' or op == '-' or 
			op == '*' or op == '/' or op == '%'):
			if (leftEval == CMMTypes.INT and rightEval == CMMTypes.INT):
				return CMMTypes.INT;
		elif (op == '&&' or op == '||'):
			if (leftEval == CMMTypes.BOOL and rightEval == CMMTypes.BOOL):
				return CMMTypes.BOOL;
		elif (op == '<' or op == '>' or
			  op == '<=' or op == '>=' or
			  op == '==' or op == '!='):
			if (leftEval == CMMTypes.INT and rightEval == CMMTypes.INT):
				return CMMTypes.BOOL;
		elif (leftEval == rightEval):
				return leftEval;
		else:
			semanticError(self.data['pos']);
			print "Left and right hand operators of binary op don't match.\n";

	def printNode(self):
		pass;

class IfTreeNode(TreeNode):

	def evaluate(self):
		expEval = self.data['exp'].evaluate();

		if (not isinstance(expEval, int)):
			expEval = getCMMType(expEval);

		if (expEval != CMMTypes.BOOL):
			semanticError(self.data['pos']);
			print "Expression of if statement must be boolean, " + getCMMTypeName(expEval) + " found instead.\n"

		self.data['block'].evaluate();

	def printNode(self):
		print "If statement begin";
		self.data['exp'].printNode();
		self.data['block'].printNode();
		print "If statement end";

class IfElseTreeNode(TreeNode):

	def evaluate(self):
		expEval = self.data['exp'].evaluate();

		if (not isinstance(expEval, int)):
			expEval = getCMMType(expEval);

		if (expEval != CMMTypes.BOOL):
			semanticError(self.data['pos']);
			print "Expression of ifelse statement must be boolean, " + getCMMTypeName(expEval) + " found instead.\n"

		self.data['block'].evaluate();
		self.data['blockElse'].evaluate();

	def printNode(self):
		print "Ifelse statement begin";
		self.data['exp'].printNode();
		self.data['block'].printNode();
		self.data['blockElse'].printNode();
		print "Ifelse statement end";

class WhileTreeNode(TreeNode):

	def evaluate(self):
		expEval = self.data['exp'].evaluate();

		if (not isinstance(expEval, int)):
			expEval = getCMMType(expEval);

		if (expEval != CMMTypes.BOOL):
			semanticError(self.data['pos']);
			print "Expression of while statement must be boolean, " + getCMMTypeName(expEval) + " found instead.\n"

		helpers.insideLoops += 1;
		self.data['block'].evaluate();
		helpers.insideLoops -= 1;

	def printNode(self):
		print "While statement begin";
		self.data['block'].printNode();
		print "While statement end";

class ForTreeNode(TreeNode):

	def evaluate(self):
		expEval = self.data['exp'].evaluate();
		
		self.data['assignInit'].evaluate();

		if (not isinstance(expEval, int)):
			expEval = getCMMType(expEval);

		if (expEval != CMMTypes.BOOL):
			semanticError(self.data['pos']);
			print "Expression of for statement must be a boolean, " + getCMMTypeName(expEval) + " found instead.\n"

		self.data['assignEnd'].evaluate();
		helpers.insideLoops += 1;
		self.data['block'].evaluate();
		helpers.insideLoops -= 1;

	def printNode(self):
		print "For statement begin";
		self.data['assignInit'].printNode();
		self.data['exp'].printNode();
		self.data['assignEnd'].printNode();
		self.data['block'].printNode();
		print "For statement end";

class ReadTreeNode(TreeNode):

	def evaluate(self):
		self.data['var'].evaluate();

	def printNode(self):
		print "Reading: " + self.data['var'].printNode();

class WriteTreeNode(TreeNode):

	def evaluate(self):
		self.data['expList'].evaluate();

	def printNode(self):
		print "Writing: " + self.data['var'].printNode();

class AssignTreeNode(TreeNode):
	def evaluate(self):
		varEval = self.data['var'].evaluate();
		expEval = self.data['exp'].evaluate();

		if (not isinstance(varEval, int)):
			varEval = getCMMType(varEval);
		if (not isinstance(expEval, int)):
			expEval = getCMMType(expEval);

		if (self.data['op'] != '='):
			if (varEval == CMMTypes.INT and
				expEval == CMMTypes.INT):
				return CMMTypes.INT;
			else:
				semanticError(self.data['pos']);
				print "When using operator '" + self.data['op'] + "' left and right hand must be type INT.\n"
		else:
			if (varEval != expEval):
				semanticError(self.data['pos']);
				print "Wrong type assigned to variable '" + self.data['var'].getVarName() + "'. Expecting " + getCMMTypeName(varEval) + ", found " + getCMMTypeName(expEval) + ".\n";

	def printNode(self):
		pass;	

class IDTreeNode(TreeNode):
	
	def evaluate(self):
		idType = helpers.getVariableType(self.data['id']);

		if (idType == False):
			semanticError(self.data['pos']);
			print "Variable " + self.data['id'] + " not declared.\n";
		else:
			return idType;

	def getVarName(self):
		return self.data['id'];

	def printNode(self):
		pass;

class IDVectorTreeNode(TreeNode):
	
	def evaluate(self):
		idType = helpers.getVariableType(self.data['id']);
		expEval = self.data['exp'].evaluate();

		if (not isinstance(expEval, int)):
			expEval = getCMMType(expEval);

		if (not isinstance(idType, int)):
			idType = getCMMType(idType);

		if (idType == False):
			semanticError(self.data['pos']);
			print "Variable " + self.data['id'] + " not declared.\n";
		elif (expEval != CMMTypes.INT):
			semanticError(self.data['pos']);
			print "Invalid index of vector " + self.data['id'] + ".\n";
		else:
			if (idType == CMMTypes.ARRAY_BOOL):
				return CMMTypes.BOOL;
			elif (idType == CMMTypes.ARRAY_STRING):
				return CMMTypes.STRING;
			else:
				return CMMTypes.INT;

	def getVarName(self):
		return self.data['id'];

	def printNode(self):
		pass;

class ReturnTreeNode(TreeNode):

	def evaluate(self):
		if (helpers.currentFunc != None):
			if (self.data.has_key('exp')):
				expEval = self.data['exp'].evaluate();
				if (expEval != None):
					if (not isinstance(expEval, int)):
						expEval = getCMMType(expEval);
					if (getCMMType(helpers.currentFunc) != expEval):
						semanticError(self.data['pos']);
						print "Expecting return type of " + getCMMTypeName(getCMMType(helpers.currentFunc)) + ", found " + getCMMTypeName(expEval) + ".\n";
					else:
						return getCMMType(expEval);
				else:
					semanticError(self.data['pos']);
					print "Returning a broken variable.\n";

		else:
			semanticError(self.data['pos']);
			print "You can't return outside a scope.\n";

	def printNode(self):
		print "Return stmt";

class BreakTreeNode(TreeNode):

	def evaluate(self):
		if (helpers.canBreak()):
			return;
		else:
			semanticError(self.data['pos']);
			print "You can't use 'break' outside a loop.\n";

	def printNode(self):
		print "Break stmt";


class SubCallTreeNode(TreeNode):

	def evaluate(self):
		pass;

	def printNode(self):
		pass;

