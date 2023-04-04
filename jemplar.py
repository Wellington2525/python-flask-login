import shutil
import io
import pyfiglet

result = pyfiglet.figlet_format("PATH.py", font="banner3-D")
print(result)

def adextp():
    extpademi = r'./doc/extpad.txt'
    extpademR2 = r'./doc/uso/adextp.txt'
    shutil.copyfile(extpademi, extpademR2)
    return

adextp()

def bhdextp():

    extpbdh = r'./doc/extpBHDL.txt'

    extpbdhR2 = r'./doc/uso/bhdextp.txt'
    shutil.copyfile(extpbdh, extpbdhR2)
    return

bhdextp()

def brsextp():
    extpbrs = r'./doc/extpbrs.txt'
    extpbrsR2 = r'./doc/uso/brsextp.txt'
    shutil.copyfile(extpbrs, extpbrsR2)
    return

brsextp()

def bnfextp():
  
    extpbanf = r'./doc/extpbnf.txt'
    extpbanfR2 = r'./doc/uso/bnfextp.txt'
    shutil.copyfile(extpbanf, extpbanfR2)
    return

bnfextp()


def adoextp():
    extpadopem = r'./doc/extpado.txt'
    extpadopemR2 = r'./doc/uso/adoextp.txt'
    shutil.copyfile(extpadopem, extpadopemR2)
    return
adoextp()



 