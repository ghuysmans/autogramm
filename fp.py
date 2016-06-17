"""Function definition parser"""
import sys


from ply import lex
tokens = ('ID', 'LPAR', 'RPAR', 'COMMA', 'STAR')

def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
	pass

t_ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
t_LPAR = r"\("
t_RPAR = r"\)"
t_COMMA = ","
t_STAR = r"\*"
t_ignore = "\t "

def t_error(t):
	print >>sys.stderr, "Illegal character:", t.value[0]
	t.lexer.skip(1)

lexer = lex.lex()


from ply import yacc

precedence = (
	('left', 'STAR'),
)

class Function(object):
	def __init__(self, ret, name, args):
		self.ret = ret
		self.name = name
		self.args = args
	def pretty(self, i):
		indent = "\t"*i
		ret = indent+'a function "'+self.name+'" returning:\n'
		ret += self.ret.pretty(i+1)
		if self.args != None:
			for arg in self.args:
				ret += indent+"taking "+arg.name+":\n"
				ret += arg.type.pretty(i+1)
		return ret


class Indirect(object):
	def __init__(self, indirection, data):
		self.indirection = indirection
		self.data = data
	def pretty(self, i):
		indent = "\t"*i
		if self.indirection:
			p = indent+"a pointer to "*self.indirection
			if self.indirection > 1:
				p += "("+str(self.indirection)+")\n"
			else:
				p += "\n"
		else:
			p = ""
		if isinstance(self.data, str):
			return p+indent+self.data+"\n"
		else:
			return p+self.data.pretty(i)

class Argument(object):
	def __init__(self, type, name):
		self.type = type
		self.name = name

class Arguments(object):
	"""Linked list"""
	def __init__(self, arg, next):
		self.arg = arg
		self.next = next
	def __iter__(self):
		h = self
		while h != None:
			yield h.arg
			h = h.next

def p_funcT(p):
	'''
	type : type name LPAR args RPAR
	'''
	p[0] = Indirect(p[2].indirection, Function(p[1], p[2].data, p[4]))

def p_type(p):
	'''
	type : simple
	'''
	p[0] = p[1]

def p_simple(p):
	'''
	simple : ID
	'''
	p[0] = Indirect(0, p[1])

def p_simpleP(p):
	'''
	simple : simple STAR
	'''
	p[0] = Indirect(p[1].indirection+1, p[1].data)

def p_npar(p):
	'''
	name : LPAR name RPAR
	'''
	p[0] = p[2]

def p_name(p):
	'''
	name : ID
	'''
	p[0] = Indirect(0, p[1])

def p_nptr(p):
	'''
	name : STAR name
	'''
	p[0] = Indirect(p[2].indirection+1, p[2].data)

def p_argument(p):
	'''
	arg	: type name
		| type
	'''
	if len(p) == 3:
		indirection = p[1].indirection+p[2].indirection
		name = p[2].data
	else:
		indirection = p[1].indirection
		if isinstance(p[1].data, Function):
			name = p[1].data.name
		else:
			name = "<anonymous>"
	p[0] = Argument(Indirect(indirection, p[1].data), name)

def p_args(p):
	'''
	args	: arg tail
			|
	'''
	if len(p) == 3:
		p[0] = Arguments(p[1], p[2])
	else:
		p[0] = None

def p_argsT(p):
	'''
	tail	: COMMA arg tail
			|
	'''
	if len(p) == 4:
		p[0] = Arguments(p[2], p[3])
	else:
		p[0] = None

def p_error(p):
	if p != None:
		where = "near line "+str(p.lineno)
		print >>sys.stderr, "Syntax error", where+": unexpected", p.type

yacc = yacc.yacc()


if __name__=="__main__":
	inp = sys.stdin.read()
	if "-l" in sys.argv:
		lexer.input(inp)
		for token in lexer:
			print token.lineno, token.type, token.value
	else:
		root = yacc.parse(inp, debug=("-d" in sys.argv))
		if root == None:
			print >>sys.stderr, "no input or syntax error"
		else:
			print root.pretty(0),
