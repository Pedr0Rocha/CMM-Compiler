'''
	Side structures and helpers to the semantic analyser.
'''
insideLoops = 0;

def canBreakOrReturn():
	return insideLoops != 0;

currentProc = None;
currentFunc = None;

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
		symbols[symbol] = [{
			'symbol' : symbol, 
			'type' : sType 
		}];

def addNewScope(mark):
	for key in symbols:
		symbols[key].append(mark);

def removeScope(mark):
	for key in symbols:
		if (len(symbols[key]) > 1):
			while (symbols[key].pop() != mark):
				pass;
	
def addFunctionOrProc(method):
	if (not symbols.has_key(method['name'])):
		symbols[method['name']] = [method];
	else:
		return "Semantic error: There is already a function or procedure named " + method['name'];

def getVariableType(var):
	if (symbols.has_key(var)):
		symbolTable = symbols[var][:];
		symbolTable.reverse();
		for element in symbolTable:
			if (element['symbol'] == var):
				return element['type'];
	else:
		return False;

def prettyPrintSymbols():
	for key in symbols:
		print "Key: " + str(key);
		print "List: " + str(symbols[key]);

# addOrUpdateSymbol('a', 'INT1');
# addOrUpdateSymbol('a', 'INT2');
# addOrUpdateSymbol('b', 'STRING');

# print "A Var Type " + str(getVariableType('a'));

# addNewScope('scope1');

# addOrUpdateSymbol('a', 'INT3');
# addOrUpdateSymbol('a', 'INT4');
# addOrUpdateSymbol('b', 'STRING');

# print "A Var Type " + str(getVariableType('a'));

# addNewScope('scope2');

# addOrUpdateSymbol('c', 'INT5');
# addOrUpdateSymbol('a', 'INT6');
# addOrUpdateSymbol('b', 'STRING');
# print "A Var Type " + str(getVariableType('a'));

# prettyPrintSymbols()

# removeScope('scope2');
# print "Removed Scope 2";

# prettyPrintSymbols()
