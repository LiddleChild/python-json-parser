from enum import Enum
import re

class Token(Enum):
  OPEN_BRACES,   \
  CLOSE_BRACES,  \
  OPEN_BRACKET,  \
  CLOSE_BRACKET, \
  COLON,         \
  COMMA,         \
  STRING_LITERAL,\
  NUMBER_LITERAL,   \
  EOF,           \
  = range(9)

class Tokenizer:
  def match_token(self):
    return [
      (lambda curr, nxt: curr.isspace(), None),
      (lambda curr, nxt: curr == "\n", None),
      (lambda curr, nxt: curr == "\t", None),
      (lambda curr, nxt: curr == "{",  Token.OPEN_BRACES),
      (lambda curr, nxt: curr == "}",  Token.CLOSE_BRACES),
      (lambda curr, nxt: curr == "[",  Token.OPEN_BRACKET),
      (lambda curr, nxt: curr == "]",  Token.CLOSE_BRACKET),
      (lambda curr, nxt: curr == ":",  Token.COLON),
      (lambda curr, nxt: curr == ",",  Token.COMMA),
      (lambda curr, nxt: re.match(r"""\"([^"\\]|\\[\s\S])*\"""", curr) != None, Token.STRING_LITERAL),
      (lambda curr, nxt: re.match(r"""[+-]?([0-9]*[.])?[0-9]+""", curr) != None and not nxt.isnumeric() and not nxt == ".", Token.NUMBER_LITERAL),
    ]
  
  def tokenize(self, json_str):
    token_stream = []
    buffer = ""

    i = 0
    while i < len(json_str):
      buffer += json_str[i]      
      nxt = json_str[i + 1] if i + 1 < len(json_str) else None

      # print(f"<{buffer}>")

      for func, val in self.match_token():
        if func(buffer, nxt) and val == None:
          buffer = ""
          break

        if func(buffer, nxt) and val != None:
          token_stream.append((val, buffer))
          buffer = ""
          break

      i += 1

    token_stream.append((Token.EOF, None))

    return token_stream