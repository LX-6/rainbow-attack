# rainbow-attack
Implement an attack on password tables with a rainbow table for academic purpose.

This implementation uses multiprocessing to improve performance. It is also using pickle's serializing and de-serializing protocols for Python objects, to store and limit the table file size.

We currently use it to crack sha256 hashes but you can change the hash function in the do_hash function in the rainbowattack_util.py file.

### Architecture :

**rainbowattack_main.py:**
- Main script : Generates or loads a Rainbow table and performs an auto-generated test or attacks a list of hashes provided by the user.
- test_attack : Performs an attack on a set of hashes using a Rainbow table
- crack_process : Parallelized process performing an attack on one of the hashes from the attack set
- crack_hash : Cracks an hash using a Rainbow table
- back_up_chain : Finds the password corresponding to an hash in a Rainbow table

**rainbowattack_util.py:**
- RainbowTable : Class representing a Rainbow table
  - generate : Generates a Rainbow table
  - generate_chain : Generates one of the chains of the Rainbow table
  - load : Loads a Rainbow table
- Args : Iterable representing data necessary to perform an attack
  - \__iter__ : Iterates the set of data
- ArgsIterator : Iterator for Args Iterable
  - \__iter__ : Iterates the set of data
  - \__next__ : Returns data at the current index
- generate_password : Generates a plain-text according to a password policy
- reduction : Transforms a sha256 hash into a plain-text according to a password policy
- do_hash : Hashes a plain-text using sha256 hashing protocol

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

### Performance :

The hardcoded characters set is 62 size. You can modify it line 152 in source/python/rainbowattack_main.py.

To perform 60% of success you should take twice the number of possibilities.

**Example:**
A 6 lenght password with lowercase, uppercase and digit has 56 billions possibilities (62^6). You should create a table of at least 112 billions passwords to perform 60% of success.
We recommand to take the value 1000 for columns and change the number of chains to keep the crack part fast.
