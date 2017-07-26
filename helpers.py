'''
	Side structures and helpers to the semantic analyser.
'''
# TODO 
# Remove symbols and make a list of types (no use for the symbol names)

insideLoops = 0;

def canBreak():
	return insideLoops != 0;

currentProc = None;
currentFunc = None;

currentType = None;
currentScope = 0;

currentSubCallParams = [];

currentParams = [];

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

def canCallSub(subCall):
	if (symbols.has_key(subCall)):
		return symbols[subCall];
	else:
		return False;

def addFunction(func):
	global currentParams;
	
	for param in currentParams:
		func['paramTypes'].append(param[1]);
		addParam(param[0], param[1]);

	symbols[func['name']] = func;
	currentParams = [];

def addProcedure(proc):
	global currentParams;
	
	for param in currentParams:
		proc['paramTypes'].append(param[1]);
		addParam(param[0], param[1]);

	symbols[proc['name']] = proc;
	currentParams = [];

def getVariableType(var):
	if (symbols.has_key(var)):
		symbolList = symbols[var][:];
		symbolList.reverse();
		return symbolList[0]['type'];
	else:
		return False;

def canCreateVar(var):
	if (not symbols.has_key(var)):
		return True;
	if (len(symbols[var]) == 0):
		return True;

	# TODO
	# VARIABLES CREATED INSIDE A SCOPE NOT WORKING
	#return symbols[var][len(symbols[var]) - 1] == currentScope;
	return True;

def printSymbols():
	for key in symbols:
		print "Key: " + str(key);
		print "List: " + str(symbols[key]) + "\n";