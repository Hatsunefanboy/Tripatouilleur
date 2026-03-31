import sys
sys.path.insert(0, r"C:\Users\cogne\OneDrive\Bureau\code\Tripatouilleur\src\tripatouilleur\tripa")
from coretest import Tripa, FileTripa, ImageTripa,VirtualTripa
__all__=["Tripa"]

def plus(a,b):
    return a*b
n=8
t=VirtualTripa(2,1,plus,dynamic=True)
t.extend(n)
for i in range(t.height):
    print(str(t.default[i])+"-",end="")
    for j in range(i+1):
        print(t._read_seed(i,j),end="-")
    print(str(str(t.default[i])+"-")*(t.height-i)+"\n")



