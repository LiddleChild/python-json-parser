from tokenizer import Token

class AST:
  def consume(self, expected_token, optional=False):
    token, content = self.token_stream[self.index]
    
    if token != expected_token:
      if not optional:
        raise Exception(f"Parsing failed at index {self.index}: '{content}' expected: {expected_token}")
      else:
        return None
    
    self.index += 1

    return content

  def top(self):
    return self.token_stream[self.index][0]
  
  def next(self):
    if self.index + 1 < len(self.token_stream):
      return self.token_stream[self.index + 1][0]
    else:
      return None

  def parse_json(self):
    ast = self.parse_body()
    self.consume(Token.EOF)

    return ast

  def parse_body(self):
    self.consume(Token.OPEN_BRACES)
    ast = dict()
    while self.top() == Token.STRING_LITERAL:
      key = self.parse_string_literal()
      self.consume(Token.COLON)
      value = self.parse_value()
      self.consume(Token.COMMA, self.top() == Token.CLOSE_BRACES)

      ast[key] = value

    self.consume(Token.CLOSE_BRACES)

    return ast
  
  def parse_value(self, array=False):
    if self.top() == Token.STRING_LITERAL:
      return self.parse_string_literal()

    if self.top() == Token.INT_LITERAL:
      return self.parse_integer_literal()

    if self.top() == Token.OPEN_BRACES and not array:
      return self.parse_body()
  
    if self.top() == Token.OPEN_BRACKET:
      return self.parse_array()
    
    raise Exception("Unexcepted value")
    
  def parse_string_literal(self):
    key = self.consume(Token.STRING_LITERAL)
    return key[1:-1]
  
  def parse_integer_literal(self):
    key = self.consume(Token.INT_LITERAL)
    return int(key)
  
  def parse_array(self):
    self.consume(Token.OPEN_BRACKET)
    arr = []

    while self.top() != Token.CLOSE_BRACKET:
      value = self.parse_value(array=True)
      self.consume(Token.COMMA, self.top() == Token.CLOSE_BRACKET)
      arr.append(value)

    self.consume(Token.CLOSE_BRACKET)

    return arr

  def generate(self, token_stream):
    self.token_stream = token_stream
    self.index = 0

    return self.parse_json()