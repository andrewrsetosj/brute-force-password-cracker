import string
import hashlib 
import time
from itertools import product
    
# Reading the file
# Returns: a set of strings of the hashed passwords
def read_file(file: str) -> set:
    with open(file, "r") as f:
        return {line.strip() for line in f}

# MAIN 
def main():
    # Creating a start time benchmark
    starting_time = time.time()

    # Possible characters
    symbols = "!@#$%^&*()"
    characters = string.ascii_letters + string.digits + symbols
    
    # Getting the hashes from hashes.txt
    filename = "hashes.txt"
    passwords = read_file(filename)

    num_characters = 1

    # Iterating infinitely until the password set is empty
    while passwords:        
        # Iterating through every tuple in the cartesian product
        for tuple_password in product(characters, repeat=num_characters):
            # Iterating through every password
            temp = ''.join(tuple_password)
            hashed_temp = hashlib.md5(temp.encode()).hexdigest()
            if hashed_temp in passwords:
                elapsed = time.time() - starting_time
                print(f"{temp}\tin {elapsed} seconds.")
                passwords.remove(hashed_temp)

            # Exiting early if all passwords are cracked
            if not passwords:
                break
        
        num_characters += 1
     
# Starting code @ MAIN
if __name__ == '__main__':
    main()
