#!/usr/bin/env python2
from parser import yacc, definitions, Definition

def to_gv():
	print "digraph {"
	#print "rankdir=LR;"
	to_gv_r(axiom)
	print "}"

def quote(s):
	return '"%s"' % s

def to_gv_r(v):
	#Update v's counter and print it using a unique identfier.
	#Terminal symbols are added here to simplify the functions above.
	if v not in definitions:
		if v!=None and v[0].islower():
			print >>sys.stderr, repr(v), "doesn't exist."
			#keep going anyway...
		#let's pretend it's a new terminal symbol
		definitions[v] = Definition()
	d = definitions[v] #shortcut
	d.used += 1
	id = d.name(v) #unique dot identifier
	if v == None:
		v = "&epsilon;"
	print quote(id), "[label=\"%s\"];"%v
	if d.used == 1:
		#first time
		for i, option in enumerate(d.rules):
			if len(d.rules) == 1:
				#there is just one possible derivation
				#let's avoid a useless "0" node
				opt = id
			else:
				#there are multiple ways of derivating v
				#let's assign a number to each of them
				opt = id+"_o"+str(i)
				print quote(opt), "[label=\"%d\"];"%i
				print quote(id), "->", quote(opt), "[style=dashed];"
			if option == None:
				#hack to avoid redundancy
				option = [None]
			for symbol in option:
				other = to_gv_r(symbol)
				print quote(opt), "->", quote(other), ";"
				is_var = symbol!=None and symbol[0].islower()
				explored = definitions[symbol].used>1
				#TODO understand why this test is even needed
				diff = other!=symbol #avoid loops
				if is_var and explored and args.back and diff:
					print quote(other), "->", quote(symbol), "[style=dashed];"
	print >>sys.stderr, "returning", repr(id)
	return id


if __name__=="__main__":
	import sys
	import argparse
	p = argparse.ArgumentParser()
	p.add_argument("script", help="input file")
	p.add_argument("--back", action="store_true", help="show backreferences")
	p.add_argument("--unused", action="store_true", help="show unused rules")
	args = p.parse_args()
	if args.script == "-":
		inp = sys.stdin.read()
	else:
		inp = open(args.script, "r").read()
	axiom = yacc.parse(inp, debug=("-d" in sys.argv))
	if axiom == None:
		print >>sys.stderr, "No PLY rules could be found."
	else:
		to_gv()
		if args.unused:
			for v in definitions:
				if not definitions[v].used:
					print >>sys.stderr, repr(v), "is never used."
