import sys
import fasttext as ft

argvs = sys.argv
input_file = argvs[1]
output = argvs[2]

classifier = ft.supervised(input_file, output)
