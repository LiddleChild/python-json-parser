from tokenizer import Tokenizer
from ast_parser import AST

# json_str = """
# {
#   "integer1": 987654,
#   "string1": "hello, world",
#   "float1": 123.456
#   "body1": {
#     "integer2": 645321,
#     "string2": "hi!"
#   },
#   "body2": {
#     "array1": [1, "2", "3", 4],
#     "array2": []
#   }
# }
# """
json_str = """
{
  "float1":  123.456,
  "float2": +123.456,
  "float3": -123.456,
  "integer1": 123,
  "integer2": +123,
  "integer3": -123,
}
"""

tokenizer = Tokenizer()
token_stream = tokenizer.tokenize(json_str)
# for i in token_stream:
#   print(i)

ast = AST()
json = ast.generate(token_stream)

print(json)