import sys
from ply import yacc
from lexer import lex, tokens

rules = {}

precedence = (
	('left', 'NL'),
	('left', 'OR'),
)

def p_programP(p):
	'''
	program : PYTHON program
	'''
	p[0] = p[2]

def p_programB(p):
	'''
	program : block program
	'''
	p[0] = p[1]

def p_programE(p):
	'''
	program :
	'''
	pass

def p_block(p):
	'''
	block : BLOCK NL rules BLOCK
	'''
	p[0] = p[3]

def p_rules(p):
	'''
	rules	: rule rules
			| rule
	'''
	p[0] = p[1]

def p_rule(p):
	'''
	rule : VARIABLE COLON disj
	'''
	if p[1] not in rules:
		rules[p[1]] = []
	rules[p[1]].extend(p[3])
	p[0] = p[1]

def p_disjE(p):
	'''
	disj : NL
	'''
	p[0] = [None]

def p_disjB(p):
	'''
	disj : terms NL
	'''
	p[0] = [p[1]]

def p_disjI(p):
	'''
	disj : terms NL OR disj
	'''
	p[0] = [p[1]] + p[4]

def p_termsB(p):
	'''
	terms	: VARIABLE
			| TOKEN
	'''
	p[0] = [p[1]]

def p_termsI(p):
	'''
	terms	: VARIABLE terms
			| TOKEN terms
	'''
	p[0] = [p[1]] + p[2]

def p_error(p):
	where = "near line "+str(p.lineno)
	print >>sys.stderr, "Syntax error", where+": unexpected", p.type


yacc = yacc.yacc()
if __name__=="__main__":
	import sys
	inp = sys.stdin.read()
	print yacc.parse(inp, debug=("-d" in sys.argv))
	for r in rules:
		print r, rules[r]
