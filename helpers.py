'''
	Side structures and helpers to the semantic analyser.
'''
# TODO 
# Remove symbols and make a list of types (no use for the symbol names)
# Better way to import CMMTypes from ast (welcome to dependency hell)

insideLoops = 0;

def canBreakOrReturn():
	return insideLoops != 0;

currentProc = None;
currentFunc = None;

currentType = None;
currentScope = 0;

currentParams = [];

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
		symbols[symbol] = [getScopeDelimiter(currentScope), {
			'symbol' : symbol, 
			'type' : sType 
		}];

def addParam(symbol, sType):
	if (symbols.has_key(symbol)):
		symbolTable = symbols[symbol];
		symbolTable.append(getScopeDelimiter(currentScope + 1));
		symbolTable.append({
			'symbol' : symbol, 
			'type' : sType 
		});
	else:
		symbols[symbol] = [getScopeDelimiter(currentScope + 1), {
			'symbol' : symbol, 
			'type' : sType 
		}];

def addNewScope():
	for key in symbols:
		if (symbols[key] is list):
			symbols[key].append(getScopeDelimiter(currentScope + 1));

def removeScope():
	for key in symbols:
		if (symbols[key] is list):
			if (len(symbols[key]) > 0):
				while (symbols[key].pop() != getScopeDelimiter(currentScope - 1)):
					if (len(symbols[key]) == 0):
						break;
				pass;

def getScopeDelimiter(scope):
	return "scope-" + str(scope);

def canCreateFuncOrProc(funcOrProc):
	return (not symbols.has_key(funcOrProc));

def addFunction(func):
	global currentParams;
	
	for param in currentParams:
		func['paramTypes'].append(param[1]);
		addParam(param[0], param[1]);

	symbols[func['name']] = func;
	currentParams = [];

def addProcedure(proc):
	if (not symbols.has_key(proc['name'])):
		symbols[proc['name']] = [proc];

def getVariableType(var):
	if (symbols.has_key(var)):
		symbolList = symbols[var][:];
		symbolList.reverse();
		return element['type'];
	else:
		return False;

def canCreateVar(var):
	if (not symbols.has_key(var)):
		return True;
	if (len(symbols[var]) == 0):
		return True;
	return symbols[var][len(symbols[var]) - 1] == currentScope;

def printSymbols():
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