"Simplified XML parser"
import sys


from ply import lex
tokens = ('TEXT', 'BTAG', 'ETAG', 'ANAME', 'EQUAL', 'AVALUE', 'CTAG')
states = (('text', 'inclusive'), ('tag', 'inclusive'), )

def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
	pass

t_text_TEXT = '[^<>\n]+'
def t_text_BTAG(t):
	'<[a-zA-Z][a-zA-Z\-]*'
	t.value = t.value[1:]
	t.lexer.begin('tag')
	return t
def t_text_CTAG(t):
	'</[a-zA-Z][a-zA-Z\-]*[\t\n ]*>'
	t.value = t.value[2:-1]
	return t

def t_tag_ETAG(t):
	'>'
	t.lexer.begin('text')
	return t
t_tag_ANAME = r'[a-zA-Z][a-zA-Z\-]*'
t_tag_EQUAL = '='
def t_tag_AVALUE(t):
	'"[^"]*"'
	t.lexer.lineno += t.value.count('\n')
	return t
t_tag_ignore = "\n\t "

def t_error(t):
	print >>sys.stdout, "Illegal character:", t.value[0]
	t.lexer.skip(1)

lexer = lex.lex()
lexer.begin('text')


from ply import yacc

def p_nodes(p):
	'''
	nodes	: node nodes
			|
	'''
	if len(p) == 1:
		p[0] = []
	else:
		p[0] = [p[1]] + p[2]

def p_node(p):
	'''
	node	: TEXT
			| otag nodes CTAG
	'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		if p[1][0] != p[3]:
			raise SyntaxError
		p[0] = (p[1][0], p[1][1], p[2])

def p_otag(p):
	'''
	otag : BTAG attrs ETAG
	'''
	p[0] = (p[1], p[2])

def p_attrs(p):
	'''
	attrs	: ANAME EQUAL AVALUE attrs
			|
	'''
	if len(p) == 1:
		p[0] = []
	else:
		p[0] = [(p[1], p[3])] + p[4]

def p_error(p):
	where = "near line "+str(p.lineno)
	print >>sys.stderr, "Syntax error", where+": unexpected", p.type

yacc = yacc.yacc()


def pretty(tree, i=0):
	indent = "\t"*i
	empty = True
	for item in tree:
		empty = False
		if isinstance(item, tuple):
			print indent+item[0]+":"
			for aname, avalue in item[1]:
				print indent+"ATTR", aname, "->", avalue
			pretty(item[2], i+1)
		else:
			print indent+item.replace('\n', '\n'+indent)
	if empty:
		print indent+"EMPTY"

if __name__=="__main__":
	inp = sys.stdin.read()
	if "-l" in sys.argv:
		lexer.input(inp)
		for token in lexer:
			print token.lineno, token.type, token.value
	else:
		pretty(yacc.parse(inp, debug=("-d" in sys.argv)))
