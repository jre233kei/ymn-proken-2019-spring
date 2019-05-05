import urllib.request as ul
import urllib.error
from bs4 import BeautifulSoup

html = ul.urlopen("http://www.cs.waseda.ac.jp")

soup = BeautifulSoup(html)

A = soup.find_all("a")

print(A)