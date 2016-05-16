import sys
from ply import yacc
from lexer import lex, tokens

precedence = (
	('left', 'NL'),
	('left', 'OR'),
)

def p_program(p):
	'''
	program	: PYTHON program
			| block program
			|
	'''
	pass

def p_block(p):
	'''
	block	: BLOCK rules BLOCK
	'''
	pass

def p_rules(p):
	'''
	rules	: rule NL rules
			| rule
	'''
	pass

def p_rule(p):
	'''
	rule	: VARIABLE COLON disj
	'''
	pass

def p_disj(p):
	'''
	disj	: terms NL OR disj
			| terms
	'''
	pass

def p_terms(p):
	'''
	terms	: VARIABLE terms
			| TOKEN terms
			|
	'''
	pass

def p_error(p):
	where = "near line "+str(p.lineno)
	print >>sys.stderr, "Syntax error", where+": unexpected", p.type


yacc = yacc.yacc()
if __name__=="__main__":
	import sys
	inp = sys.stdin.read()
	yacc.parse(inp, debug=("-d" in sys.argv))
