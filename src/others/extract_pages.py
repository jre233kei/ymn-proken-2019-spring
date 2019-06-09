import re

content = open('../data/raw/jawiki-latest-pages-articles (1).xml').readlines()
pattern = r"<page>.*?</page>"
compiled_pattern = re.compile(pattern, flags=(re.MULTILINE | re.DOTALL))
results = re.findall(compiled_pattern, content)

print(results)
