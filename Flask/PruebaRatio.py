from difflib import SequenceMatcher as SM

s1 = 'Hola Mundo'
s2 = 'Hola Mundo cruel'

coincidencia = SM(None, s1, s2).ratio()

if coincidencia >= 0.8:

    print(coincidencia)
else:
    print(" no se parecen en una mierda")

