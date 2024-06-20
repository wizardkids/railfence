"""
    Filename: railfence.py
     Version: 0.1
      Author: Richard E. Rawson
        Date: 2023-05-02
 Description: Take a plaintext message and encrypt it then decrypt it, using railfence cipher. The encrypted and decrypted message are printed to the terminal.

CODENOTE: The plaintext message and the number of rails must be entered manually at the end of this program.

Below is a sample encryption of the plaintext "WEAREDISCOVEREDFLEEATONCE" using a railfence with 3 rails to generate the ciphertext:
    "WECRLTEERDSOEEFEAOCAIVDEN"

We write the message diagonally...

W . . . E . . . C . . . R . . . L . . . T . . . E
. E . R . D . S . O . E . E . F . E . A . O . C .
. . A . . . I . . . V . . . D . . . E . . . N . .
The ciphertext is obtained by reading the rails from left to right, top to bottom:
    WECRLTEERDSOEEFEAOCAIVDEN

Implement the functions:
    encrypt_railfence(plaintext, num_rails)
    decrypt_railfence(ciphertext, num_rails)

Source: https://en.wikipedia.org/wiki/Rail_fence_cipher

"""

import json
from pprint import pprint

import click
from icecream import ic

VERSION = "0.1"


@click.command(help="", epilog="")
@click.argument("plaintext", type=str, required=False)
@click.option("-r", "--rails", default=3, show_default=True, type=int, help="Number of rails.")
@click.option("-e", "--encrypt", is_flag=True, type=bool, default=False, help="Encrypt the plaintext.")
@click.option("-d", "--decrypt", is_flag=True, type=bool, default=False, help="Decrypt the encrypted text.")
@click.version_option(version=VERSION)
def cli(plaintext: str, rails: int, encrypt: bool, decrypt: bool) -> None:

    print()
    ic(plaintext)
    ic(type(rails), rails)
    ic(type(encrypt), encrypt)
    ic(type(decrypt), decrypt)
    print()

    # If there's plaintext, then encrypt, regardless of --encrypt or --decrypt.
    if plaintext is not None:
        encrypt = True
        decrypt = False

    # If -e is set but there's not plaintext.
    if encrypt and plaintext is None:
        print("\nNo plaintext message was provided.\n", sep="")
        exit()

    # If there's no plaintext, then we must mean to decrypt.
    if plaintext is None:
        decrypt = True
        encrypt = False

    if encrypt:
        encrypt_message(plaintext, rails)

    elif decrypt:
        decrypt_cipher()

    else:
        print(f"Invalid command line arguments.\n", sep="")


def encrypt_message(plaintext: str, rails: int):
    """
    Converts the plaintext string into a set of "rails". The "rails" are subsets of the outer list: list[list[str]], where each element of a rail is a letter from plaintext. Encrypted message, along with the number of rails, is saved in "encrypted_message.json".

    Parameters
    ----------
    plaintext (str): the original text to be encrypted
    rails (int): the number of rails, specified initially

    """

    # Create an empty 2D array to hold the characters from "plaintext".
    # There will be one sublist for each rail.
    cipher_list: list[any] = []
    for rail in range(rails):
        cipher_list.append([])

    rail, direction, ndx = 0, 1, -1
    while True:
        # Put the next letter (at "ndx") in plaintext to be placed into [encrypted].
        ndx += 1
        cipher_list[rail].append(plaintext[ndx])

        # Update the rail number based on the direction.
        rail += direction

        # If the rail number reaches one less than the number of rails or 0, reverse the direction.
        if rail == rails - 1 or rail == 0:
            direction *= -1

        # If we're at the end of plaintext, stop.
        if ndx == len(plaintext) - 1:
            break

    cipher_string: list[str] = flatten_list(cipher_list)
    encrypted_dict: dict[str, str | int] = {"cipher": "".join(cipher_string), "rails": rails}

    with open("encrypted_message.json", "w", encoding="utf-8") as file:
        json.dump(encrypted_dict, file)


def decrypt_cipher() -> None:
    """
    Considering that the math behind deciphering a rail fence crypto is beyond me, I asked Bing chat to generate the following code. This code takes a string that is the encryption of the original plain text and decrypts it.

    CODENOTE: No AI could even suggest code for decrypting a string if the key (number of rails) was unknown. DON'T LOSE THE KEY!

    CODENOTE: This code requires knowing how many rails there are.

    Parameters
    ----------
    cipher : str -- the cipher of the original "plaintext" string
    rails : int -- the number of rails (sublists)

    Returns
    -------
    str -- the decrypted string, the same as the original "plaintext"
    """

    with open("encrypted_message.json", "r", encoding="utf-8") as file:
        encrypted_dict = json.load(file)

    cipher: str = encrypted_dict["cipher"]
    rails: int = encrypted_dict["rails"]

    # Initialize an empty string for the plaintext
    decrypted_cipher: str = ""

    # Calculate the length of the ciphertext
    length: int = len(cipher)

    # Create an empty rail matrix with the same size as the ciphertext
    rail: list[list[str]] = [["\n" for i in range(length)] for j in range(rails)]

    # Initialize the row and column indices, and dir_down.
    row, col, dir_down = 0, 0, None

    # Mark the places with '*' where the letters will be placed
    c_loc = 0  # index to track the ciphertext
    for i in range(length):
        # If we reach the top or bottom rail, change the direction
        if row == 0 or row == rails - 1:
            dir_down: bool = not dir_down

        # Mark the place with '*'
        rail[row][col] = '*'

        # Move to the next column.
        col += 1

        # Move up or down the row based on the direction.
        row += 1 if dir_down else -1

    # Initialize the index to track the ciphertext
    index = 0

    # Fill the rail matrix with the letters of the ciphertext in row order
    for i in range(rails):
        for j in range(length):
            if rail[i][j] == '*' and index < length:
                rail[i][j] = cipher[index]
                index += 1

    # Reset the row and column indices
    row, col = 0, 0

    # Read the decrypted_cipher from the rail matrix in zig-zag order
    for i in range(length):
        # If we reach the top or bottom rail, change the direction
        if row == 0:
            dir_down = True
        elif row == rails - 1:
            dir_down = False

        # Append the letter to the decrypted_cipher
        decrypted_cipher += rail[row][col]

        # Move to the next column
        col += 1

        # Move up or down the row based on the direction
        row: int = row + 1 if dir_down else row - 1

    with open("decrypted_message.json", "w", encoding="utf-8") as file:
        json.dump(decrypted_cipher, file)


def flatten_list(target: list[list[str]]) -> list[str]:
    """
    Flattens an n-dimensional list into a one-dimensional list. "n" can be any value.

    Parameters
    ----------
    target : list -- any n-dimensional list

    Returns
    -------
    list -- flattened list
    """

    return sum((flatten_list(sub) if isinstance(sub, list) else [sub] for sub in target), [])


if __name__ == '__main__':

    plaintext = "WEAREDISCOVEREDFLEEATONCE"
    # cipher_text = "WECRLTEERDSOEEFEAOCAIVDEN"

    # plaintext = "In the café, the bánh mì sandwich is a popular choice among the regulars. The flaky baguette, stuffed with savory grilled pork, pickled daikon and carrots, fresh cilantro, and a dollop of sriracha mayo, is the perfect lunchtime indulgence. As I sipped my matcha latte, I noticed the barista's shirt had a cute ねこ (neko, or cat) graphic on it. It reminded me of the time I visited Tokyo and saw the famous 東京タワー (Tokyo Tower) at night, aglow with colorful lights. The world is full of unique and beautiful symbols, and Unicode makes it possible to express them all in one cohesive language."

    rails = 3  # number of rails; MUST be < len(plaintext)

    print()
    cli()
