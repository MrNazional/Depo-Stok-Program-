from PyQt5 import uic

with open("Depo_stok.py" , "w" , encoding="utf-8") as fout:
    uic.compileUi("depo_stok.ui", fout)