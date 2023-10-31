from tokenizer import Tokenizer

json_str = """
{
  "first1": 111,
  "second2": 222,
}
"""
tokenizer = Tokenizer()
for i in tokenizer.tokenize(json_str):
  print(i)