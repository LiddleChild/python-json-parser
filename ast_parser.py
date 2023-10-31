from tokenizer import Token

class AST:
  """
  utility function
  """
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

  """
  parse json
  """
  def parse_json(self):
    ast = self.parse_body()
    self.consume(Token.EOF)

    return ast

  """
  parse with body
  """
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
  
  def parse_array(self):
    self.consume(Token.OPEN_BRACKET)
    arr = []

    while self.top() != Token.CLOSE_BRACKET:
      value = self.parse_value(array=True)
      self.consume(Token.COMMA, self.top() == Token.CLOSE_BRACKET)
      arr.append(value)

    self.consume(Token.CLOSE_BRACKET)

    return arr
  
  """
  parse value
  """
  def parse_value(self, array=False):
    if self.top() == Token.STRING_LITERAL:
      return self.parse_string_literal()

    if self.top() == Token.NUMBER_LITERAL:
      return self.parse_number_literal()

    if self.top() == Token.OPEN_BRACES and not array:
      return self.parse_body()
  
    if self.top() == Token.OPEN_BRACKET:
      return self.parse_array()
    
    raise Exception("Unexcepted value")
  
  """
  literal parser
  """
  def parse_string_literal(self):
    key = self.consume(Token.STRING_LITERAL)
    return key[1:-1]
  
  def parse_number_literal(self):
    key = float(self.consume(Token.NUMBER_LITERAL))
    return int(key) if key == round(key, 0) else key

  """
  generate
  """
  def generate(self, token_stream):
    self.token_stream = token_stream
    self.index = 0

    return self.parse_json()