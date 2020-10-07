La fonction de réduction transforme une empreinte en un nouveau mot de passe.
Afin d'éviter des problèmes de collision, plusieurs fonctions de réduction sont utilisées

```python
import hashlib
chars="abcdefghijklmnopqrstuvwxyz"
chars_len = len(chars)

def reduce(i):
    # reduces int i to a 5 char password
    # think of i as a number encoded in base l
    pwd=""
    while len(pwd)<5:
        pwd = pwd + chars[ i%chars_len ]
        i = i // chars_len
    return pwd


table=[]
# generate 10 chains of 1000 pwd, print start and end
for s in range(0,10):
    # we can use reduce to generate the start of a chain
    start=reduce(s)

    p=start
    for i in range(0,1000):
        # hash
        h=hashlib.md5(p.encode('ascii')).hexdigest()
        # reduce
        p=reduce(int(h,16))

    table.append([start,p])

print (table)
```

Autre implémentation plus poussé en python : https://github.com/clu8/RainbowTable


Source : 
https://www.wikiwand.com/fr/Rainbow_table
https://stackoverflow.com/questions/57101012/how-to-implement-a-reduced-rainbow-table-in-python