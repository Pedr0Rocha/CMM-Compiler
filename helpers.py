'''
	Side structures and helpers to the semantic analyser.
'''
# TODO 
# tirar symbol e fazer lista de tipos apenas
#

insideLoops = 0;

def canBreakOrReturn():
	return insideLoops != 0;

currentProc = None;
currentFunc = None;

currentType = None;
currentScope = 0;

def getCurrentFuncType():
	pass;

symbols = {};

def addOrUpdateSymbol(symbol, sType):
	if (symbols.has_key(symbol)):
		symbolTable = symbols[symbol];
		symbolTable.append({
			'symbol' : symbol, 
			'type' : sType 
		});
	else:
		symbols[symbol] = [currentScope, {
			'symbol' : symbol, 
			'type' : sType 
		}];
	print symbols;

def addNewScope():
	scopeDelimiter = "scope-" + str(currentScope + 1);
	for key in symbols:
		symbols[key].append(scopeDelimiter);

def removeScope():
	scopeDelimiter = "scope-" + str(currentScope - 1);
	for key in symbols:
		if (len(symbols[key]) > 0):
			while (symbols[key].pop() != scopeDelimiter):
				if (len(symbols[key]) == 0):
					break;
			pass;
	
def addFunctionOrProc(method):
	if (not symbols.has_key(method['name'])):
		symbols[method['name']] = [method];

def getVariableType(var):
	if (symbols.has_key(var)):
		symbolList = symbols[var][:];
		symbolList.reverse();
		return element['type'];
	else:
		return False;

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

def canCreateVar(var):
	if (len(symbols[var]) == 0):
		return True;
	return symbols[var][len(symbols[var]) - 1] != currentScope;

def prettyPrintSymbols():
	for key in symbols:
		print "Key: " + str(key);
		print "List: " + str(symbols[key]);

# addOrUpdateSymbol('a', 'INT1');
# addOrUpdateSymbol('a', 'INT2');
# addOrUpdateSymbol('b', 'STRING');

# addNewScope('scope1');

# addOrUpdateSymbol('a', 'INT3');
# addOrUpdateSymbol('a', 'INT4');
# addOrUpdateSymbol('b', 'STRING2');

# addNewScope('scope2');

# addOrUpdateSymbol('c', 'INT5');
# addOrUpdateSymbol('a', 'INT6');
# addOrUpdateSymbol('b', 'STRING3');

# prettyPrintSymbols()

# removeScope('scope2');
# print "Removed Scope 2";

# prettyPrintSymbols()