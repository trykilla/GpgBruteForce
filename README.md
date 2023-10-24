# GPG File Decryptor

## Description
This script is designed to attempt decrypting a GPG file using a passphrase. It utilizes multiple processes to speed up the decryption process. 

## Prerequisites
- Python 3.x
- GnuPG (GPG) installed and configured on your Linux system.

## Installation

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/trykilla/GpgBruteForce.git
   ```

2. Change your current directory to the project folder:

   ```shell
   cd gpg-file-decryptor
   ```

3. Install the required Python packages using pip:

   ```shell
   pip install -r requirements.txt
   ```

## Usage

1. Make sure you have the GPG-encrypted file you want to decrypt in the project folder.

2. Open your terminal and navigate to the project folder.

3. Run the script with the following command:

   ```shell
   ./decrypt.py
   ```

4. You will be prompted to enter the name of the GPG-encrypted file you want to decrypt.

5. Enter the number of processes you want to use. It's recommended to use a number of processes equal to the number of CPU cores on your machine for optimal performance (In my case 12 but it depends on your device).

6. The script will start attempting to decrypt the GPG file. It will try different passphrases using multiple processes. If it successfully decrypts the file, it will display the passphrase and the time it took. It will also create the decrypted file in the project folder and a txt with the password and the time it took too. 

7. If you want to stop the script, press `Ctrl + C`. The script will exit gracefully.

## Disclaimer
Please use this script responsibly and only on files for which you have the legal right to attempt decryption. Decrypting files without proper authorization may be illegal in your jurisdiction.

**Note:** This script is intended for educational purposes and as a demonstration of how GPG decryption can be automated.