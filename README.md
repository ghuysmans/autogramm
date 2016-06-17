# autogramm, a PLY grammar visualization tool
Sometimes you need to understand the context of a particular grammar rule.
This could be tedious when the grammar is a bit complex
or not as you would've written it.

autogram generates a DOT ([GraphViz](http://graphviz.org/)) script
you can fairly easily customize
to produce some nice PostScript output.

## Examples
### Simplified XML parser
```
autogramm.py sml.py|dot -Tps >sml.ps
```
yields

[![SML graph](sml.png?raw=true)](sml.dot?raw=true)

### Simplified C function definition parser
```
autogramm.py fp.py|dot -Tps >fp.ps
```
yields

[![FP graph](fp.png?raw=true)](fp.dot?raw=true)

## Usage
```
autogramm.py [--back] [--unused] script

positional arguments:
  script      input file

optional arguments:
  --back      show backreferences
  --unused    show unused rules
```
