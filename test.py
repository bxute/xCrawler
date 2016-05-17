from os import mkdir,chdir,path
import re

a='Aar Me Na Par Mai Rang Daalem Jogaar me (Dholki monster)  Dj Ravi '
b='Chonga Bil Harmar Boma Ho Gail  (Dholki Monstor)  Dj Ravi.mp3'
print(a.rstrip()+'.mp3')

sa=open('asdf.mp3','r').readline()
print(len(re.findall('\<\!',sa)))