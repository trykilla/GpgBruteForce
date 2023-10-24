#!/usr/bin/env python3

# Description: Este script intenta descifrar un archivo GPG con una clave

# Qué códigos ignorar para pylint
# pylint: disable=missing-module-docstring
# pylint: disable=unused-argument
# pylint: disable=redefined-outer-name
# pylint: disable=trailing-whitespace
# pylint: disable=consider-using-f-string

from time import time, sleep
from itertools import product
from multiprocessing import Pool, Manager
import string
import signal
import sys
import os
import gnupg

LETTERS = string.ascii_lowercase


def finnish(signum, frame):
    """_summary_

    Args:
        signum (_type_): _description_
        frame (_type_): _description_
    """    
    print("🛑 Ctrl + C has been detected, exiting...")
    sleep(0.5)
    print(f"🏁 Exiting process number: {os.getpid()}")
    pool.terminate()
    sys.exit(0)


def attempt_decryption(passphrase, password_found, encrypted_data, start_time):
    """Tries to decrypt the file with the next passphrase

    Args:
        passphrase (_type_): The actual passphrase to try
        password_found (_type_): A shared variable to indicate if the password has been found
        encrypted_data (_type_): The encrypted data to decrypt
        start_time (_type_): The time when the program started
    """    
    gpg = gnupg.GPG()
    if password_found.value:
        return  
    decrypted_data = gpg.decrypt(encrypted_data, passphrase=passphrase)
    
    if decrypted_data.ok:
        password_found.value = 1 
        print(f"Pass is OK: {passphrase}, if program is not exiting, wait or just press Ctrl + C")
        end_time = time()
        with open('found_pass.txt', 'w', encoding="utf-8") as output_file:
            output_file.write(passphrase)
            output_file.write("\nTime elapsed: {:.2f} seconds".format(end_time - start_time))
        # Indica que se ha encontrado la passw
        
        with open('decrypted_file.pdf', 'wb') as pdf_file:
            pdf_file.write(decrypted_data.data)
            
        print("Time elapsed: {:.2f} seconds".format(end_time - start_time))


def map_attempt_decryption(data):
    """Maps the attempt_decryption function to the data and tries to decrypt the file in a foor_loop

    Args:
        data (_type_): The list of passphrases to try and the start time
    """    
    passphrases, start_time = data
    for passphrase in passphrases:
        attempt_decryption(passphrase, password_found,
                           encrypted_data, start_time)

if __name__ == "__main__":
    
    # First we get the file to decrypt and the number of processes to use,
    
    archivo_gpg = input("Enter the name of the file to decrypt: ")
    num_processes = int(input("Enter the number of processes to use: "))
    
    signal.signal(signal.SIGINT, finnish)
    
    gpg = gnupg.GPG()
    
    with open(archivo_gpg, 'rb') as encrypted_file: # The file to open
        encrypted_data = encrypted_file.read()
        
    with Manager() as manager:
        password_found = manager.Value('i', 0) # Shared variable to indicate if the password has been found

        for password_length in range(1, 6): # From where length to start and where to finish
            
            
            if password_found.value:
                print("Password found, exiting...")
                break
            
            args = [''.join(passw) for passw in (product(LETTERS, repeat=password_length))] # Create a list of combinations with "product" function
            
            chunk_size = len(args) // num_processes
            chunks = [args[i:i + chunk_size]
                      for i in range(0, len(args), chunk_size)] # Divide the list in chunks and assign them to a process (We create a list of lists)
            
            with Pool(processes=num_processes) as pool:
                print(f"Starting the crack with {num_processes} processes")
                print(f"for length {password_length} with file '{archivo_gpg}'")
                sleep(1)
                
                start_time = time()  
                
                pool.map(map_attempt_decryption, [(chunk, start_time) for chunk in chunks])
                pool.close()
                pool.join()
