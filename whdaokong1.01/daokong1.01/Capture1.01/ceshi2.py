import requests
import re
url = 'http://www.sohu.com/a/283136355_267106?code=f8786ddab63f5d69ecd8af1bf10d6274#comment_area'
resp = requests.get(url).text
p1 = re.compile(r'title: "(.*?)"', re.S)
title = re.findall(p1,resp)
print(title[0])