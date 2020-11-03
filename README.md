# rainbow-attack
Implement an attack on password tables with a rainbow table for academic purpose.

This implementation use multiprocessing to improve performance. It is using also pickle protocols for serializing and de-serializing of Python object structure to reduce table file size.

### Architecture :

rainbowattack_main.py :

rainbowattack_util.py :

### Installation :

```bash
pip install -r requirements.txt
```

### Usage :

From rainbow-attack/ directory :

- Create a table with 1 millions chains of 1000 columns and generate 100 hashes to test the table for 8 length passwords :
```bash
python3 source/python/rainbowattack_main.py -r 8 8 -s 1000 1000000 -g 100
```
RainbowTable_8.pickle file will be created in results/ directory.

- Load a table of 10 millions chains of 5000 columns named RainbowTable_6.pickle for 6 length passwords, and crack all the hashes from hash_to_crack.txt file :
```bash
python3 source/python/rainbowattack_main.py -r 6 6 -s 5000 10000000 -l RainbowTable_6.pickle -i hash_to_crack.txt
```

- Create a table with 10 millions chains of 1000 columns and and crack all the hashes from hash_to_crack.txt file for from 8 to 12 length passwords :
```bash
python3 source/python/rainbowattack_main.py -r 8 12 -s 1000 10000000 -i hash_to_crack.txt
```
A table for each password length will be created.