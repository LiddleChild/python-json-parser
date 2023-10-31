from tokenizer import Tokenizer
from ast_parser import AST

json_str = """
{
  "integer1": 987654,
  "string1": "hello, world",
  "body1": {
    "integer2": 645321,
    "string2": "hi!"
  },
  "body2": {
    "array1": [1, "2", "3", 4],
    "array2": []
  }
}
"""
tokenizer = Tokenizer()
token_stream = tokenizer.tokenize(json_str)
# for i in token_stream:
#   print(i)

ast = AST()
json = ast.generate(token_stream)

print(json)