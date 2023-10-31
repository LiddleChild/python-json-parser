from json_parser.tokenizer import Tokenizer
from json_parser.ast_parser import AST

class JSONParser:
  def parse(json_str):
    t = Tokenizer()
    token_stream = t.tokenize(json_str)

    ast = AST()
    json = ast.generate(token_stream)

    return json