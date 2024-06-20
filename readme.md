# Railfence Cipher

This Python script implements the Railfence cipher, which is a form of transposition cipher that encrypts a plaintext message by writing it diagonally across a set of "rails" and then reading the ciphertext off in rows.

## Description

The script provides two main functions:

1. `encrypt_railfence(plaintext, num_rails)`: Converts the plaintext string into a set of "rails". The encrypted message, along with the number of rails, is saved in `encrypted_message.json`.

2. `decrypt_railfence(ciphertext, num_rails)`: Decrypts the encrypted message stored in `encrypted_message.json` using the provided number of rails. The decrypted text is saved in `decrypted_message.txt`.

## Usage
$ `python railfence.py --help`

Usage: railfence.py [OPTIONS] [PLAINTEXT]

  The utility either encrypts or decrypts a message using railfence encryption.

Options:
  -r, --rails INTEGER  Number of rails.  [default: 3]
  -e, --encrypt        Encrypt the plaintext.
  -d, --decrypt        Decrypt the encrypted text.
  --version            Show the version and exit.
  --help               Show this message and exit.

To encrypt a plaintext message:
$ `python railfence.py -r 3 -e "WEAREDISCOVEREDFLEEATONCE"`

This will create a file `encrypted_message.json` containing the encrypted message and the number of rails used.

To decrypt an encrypted message:
$ `python railfence.py -d`

This will read the `encrypted_message.json` file and decrypt the message using the stored number of rails, creating a `decrypted_message.json` file with the original plaintext.

If only a message is provided on the command line, it will be encrypted. If there is no message and no options, `encrypted_message.txt` will be decrypted.

## Example

Below is a sample encryption of the plaintext "WEAREDISCOVEREDFLEEATONCE" using a railfence with 3 rails to generate the ciphertext:

The message is written diagonally...

`W . . . E . . . C . . . R . . . L . . . T . . . E`</br>
`. E . R . D . S . O . E . E . F . E . A . O . C .`</br>
`. . A . . . I . . . V . . . D . . . E . . . N . .`</br>

but when read laterally, left to right and top to bottom, we get:

`WECRLTEERDSOEEFEAOCAIVDEN`

## Note

- The code requires knowing the number of rails used for encryption to decrypt the message correctly. If the number of rails is unknown, decryption is not possible.