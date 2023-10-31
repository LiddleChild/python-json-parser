import sys
from json_parser.json_parser import JSONParser

with open(sys.argv[1], "r") as f:
  json_str = f.read()

json = JSONParser.parse(json_str)

print(json)