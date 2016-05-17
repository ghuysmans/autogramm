import sys
from ply import lex

tokens = ('PYTHON', 'BLOCK', 'NL',
	'VARIABLE', 'COLON', 'TOKEN', 'OR')
states = (('gramm', 'exclusive'), )

def t_NL(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
	#hack
	t.type = 'PYTHON'
	return t
def t_BLOCK(t):
	"'''|\"\"\""
	#TODO handle this nicely
	t.lexer.begin('gramm')
	return t
t_PYTHON = '.[^\'"\n]*'

t_gramm_ignore = ' \t'
t_gramm_VARIABLE = '[a-z_][a-zA-Z0-9_]*'
t_gramm_COLON = ':'
t_gramm_TOKEN = '[A-Z_][A-Z0-9_]*'
t_gramm_OR = r'\|'
def t_gramm_PREC(t):
	r'%prec\ [a-zA-Z0-9_]+' #spaces must be escaped because of re.VERBOSE
	pass
def t_gramm_NL(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
	return t
def t_gramm_BLOCK(t):
	"'''|\"\"\""
	t.lexer.begin('INITIAL')
	return t
def t_error(t):
	#this should never run!
	assert(False)
def t_gramm_error(t):
	where = "at line "+str(t.lexer.lineno)
	print >>sys.stderr, "Illegal character", repr(t.value[0]), where
	t.lexer.skip(1)

lex = lex.lex()
if __name__=="__main__":
	lex.input(sys.stdin.read())
	for token in lex:
		print token.type
