import string
import hashlib
import time
from itertools import product
from multiprocessing import Pool
import os

from single_core_cracker import read_file

# Generating all candidate strings of a given length
# Returns: a list of all possible passwords of a given length 
def generate_passwords(characters: str, length: int):
    return [''.join(p) for p in product(characters, repeat=length)]

# Checking if any of the candidate passwords match any of the passwords in the hashes file
# Returns: a list of cracked passwords in tuple form (password, hashed_password)
def check_chunk(candidates, password_hashes):
    found = []
    for candidate in candidates:
        hashed_candidate = hashlib.md5(candidate.encode()).hexdigest()
        if hashed_candidate in password_hashes:
            found.append((candidate, hashed_candidate))
    return found

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

    # Set up a multiprocessing pool based on available CPU cores
    num_cores = os.cpu_count()
    pool = Pool(processes=num_cores)

    # Iterating infinitely until the password set is empty
    while passwords:
        # Generating candidate passwords
        candidates = generate_passwords(characters, num_characters)
        
        # Dividing the candidates list for each core 
        chunk_size = len(candidates) // num_cores + 1
        chunks = []
        i = 0
        while i < len(candidates):
            chunk = candidates[i:i+chunk_size]
            chunks.append(chunk)
            i += chunk_size

        # Preparing args and executing check_chunk in parallel 
        args = []
        for chunk in chunks:
            args.append((chunk, passwords))
        matches = pool.starmap(check_chunk, args)

        # Iterating through the list of cracked passwords
        for match in matches:
            for password, hashed_password in match:
                elapsed = time.time() - starting_time
                print(f"{password}\tin {elapsed} seconds.")
                passwords.remove(hashed_password)

        num_characters += 1

    # Cleaning
    pool.close()
    pool.join()

# Starting code @ MAIN
if __name__ == '__main__':
    main()
