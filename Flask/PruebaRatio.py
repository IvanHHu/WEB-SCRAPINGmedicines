from difflib import SequenceMatcher as SM
from collections import Counter




s1 = 'losartan'
s2 = 'Losartan 50 mg Caja Con 15 Tabletas...'

caracteres = Counter(s1)
print(caracteres)
print(caracteres[' '])



coincidencia = SM(None, s1, s2).ratio()
print(coincidencia)

if coincidencia >= 0.8:

    print("coincidencia")
else:
    print(" no se parecen en una mierda")

