import sys
from ply import lex
from ply.lex import TOKEN

tokens = ('BLOCK', 'NL', 'VARIABLE', 'COLON', 'TOKEN', 'OR')
states = (('gramm', 'exclusive'), ('comment', 'exclusive'))

ident = '[a-z_][a-zA-Z0-9_]*'
block = r"def\ p_"+ident+r"\("+ident+r"\):(\s|\n)*('''|\"\"\")(\s|\n)*"
@TOKEN(block)
def t_BLOCK(t):
	t.lexer.lineno += t.value.count("\n")
	if "p_error(" not in t.value:
		t.lexer.begin('gramm')
		return t
	else:
		t.lexer.begin('comment')
def t_PYTHON(t):
	r'.[^\n]*'
	pass
def t_NL(t):
	r'\n'
	t.lexer.lineno += 1
t_ignore = ' \t'

t_gramm_ignore = ' \t'
t_gramm_VARIABLE = ident
t_gramm_COLON = ':'
t_gramm_TOKEN = '[A-Z_][A-Z0-9_]*'
def t_gramm_OR(t):
	r'\n\s*\|'
	t.lexer.lineno += 1
	return t
def t_gramm_PREC(t):
	r'%prec\s+[a-zA-Z0-9_]+' #spaces must be escaped because of re.VERBOSE
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

def t_comment_END(t):
	r"(.|\n)*('''|\"\"\")"
	t.lexer.lineno += t.value.count("\n")
	t.lexer.begin('INITIAL')
def t_comment_error(t):
	assert(False)
t_comment_ignore = ''


lex = lex.lex()
if __name__=="__main__":
	lex.input(sys.stdin.read())
	for token in lex:
		print token.type
