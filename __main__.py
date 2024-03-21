import os
import sys
from htmlparser.tokenizer.htmltokenizer import HtmlTokenizer
from htmlparser.parser.parser import HtmlParser
from htmlparser.app import App

args = sys.argv[1:]
if len(args) > 1:
    print("Wrong number of arguments!\nEx: $ htmlparser <file>")
    exit(69)
elif len(args) == 0:
    print("Please input a file as an argument!\nEx: $ htmlparser <file>")
    exit(69)

if not os.path.isfile(args[0]):
    print("File not found!\nTry again: $ htmlparser <path_to_file>")
    exit(69)

f = open(args[0])
source = f.read()

h = HtmlTokenizer(source=source)
toks = h.readTokens()
p = HtmlParser(toks)
app = App(p.buildTree())
