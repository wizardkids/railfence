"""
    Filename: railfence.py
     Version: 0.1
      Author: Richard E. Rawson
        Date: 2023-05-02
 Description: Railfence Cipher

Below is a sample encryption of the plaintext "WEAREDISCOVEREDFLEEATONCE" using a railfence with 3 rails to generate the ciphertext "WECRLTEERDSOEEFEAOCAIVDEN"

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


def generate_cipher_string(plaintext: str, rails: int) -> str:
    """
    Converts the plaintext string into a set of "rails". The "rails" are subsets of the outer list: list[list[str]], where each element of a rail is a letter from plaintext.

    Args:
        plaintext (str): the original text to be encrypted
        rails (int): the number of rails, specified initially

    Return:
        [list[list[str]]]: the set of rails populated with characters from the "plaintext" string.
    """

    # Create the 2D array to hold the characters from "plaintext".
    cipher_list = []
    for rail in range(rails):
        cipher_list.append([])

    rail, direction, ndx = 0, 1, -1
    while True:
        # Put the next letter (at "ndx") in plaintext to be placed into [encrypted].
        ndx += 1
        cipher_list[rail].append(plaintext[ndx])

        # Update the rail number based on the direction
        rail += direction

        # If the rail number reaches 2 or 0, reverse the direction
        if rail == rails - 1 or rail == 0:
            direction *= -1

        # If we're at the end of plaintext, stop.
        if ndx == len(plaintext) - 1:
            break

    cipher_string = []
    for i in cipher_list:
        for j in i:
            cipher_string.append(j)

    return "".join(cipher_string)


def decode_cipher(cipher: str, rails: int) -> str:
    """
    Considering that the math behind deciphering a rail fence crypto is beyond me, I asked Bing chat to generate the following code. This code takes a string that is the encryption of the original plain text and decrypts it.

    CODENOTE: Neither Bing,Bard, nor chatGPT could provide code for decrypting a string if the key (number of rails) was unknown.

    CODENOTE: This code requires knowing how many rails there are.

    Args:
        cipher (str): the cipher of the original "plaintext" string
        rails (int): the number of rails (sublists)

    Returns:
        str: the decrypted string, the same as the original "plaintext"
    """

    # Initialize an empty string for the plaintext
    decrypted_cipher = ""

    # Calculate the length of the ciphertext
    length = len(cipher)

    # Create an empty rail matrix with the same size as the ciphertext
    rail = [["\n" for i in range(length)] for j in range(rails)]

    # Set the direction to move down
    dir_down = None
    # Initialize the row and column indices
    row, col = 0, 0

    # Mark the places with '*' where the letters will be placed
    for i in range(length):
        # If we reach the top or bottom rail, change the direction
        if row == 0:
            dir_down = True
        elif row == rails - 1:
            dir_down = False

        # Mark the place with '*'
        rail[row][col] = '*'

        # Move to the next column
        col += 1

        # Move up or down the row based on the direction
        if dir_down:
            row += 1
        else:
            row -= 1

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
        if dir_down:
            row += 1
        else:
            row -= 1

    return decrypted_cipher


def main(plaintext, rails):
    """
    "WEAREDISCOVEREDFLEEATONCE"

    W . . . E . . . C . . . R . . . L . . . T . . . E
    . E . R . D . S . O . E . E . F . E . A . O . C .
    . . A . . . I . . . V . . . D . . . E . . . N . .

    "WECRLTEERDSOEEFEAOCAIVDEN"

    """

    cipher = generate_cipher_string(plaintext, rails)

    decrypted_cipher = decode_cipher(cipher, rails)

    print(plaintext)
    print()
    print(cipher)
    print()
    print(decrypted_cipher)


if __name__ == '__main__':

    plaintext = "WEAREDISCOVEREDFLEEATONCE"
    # cipher_text = "WECRLTEERDSOEEFEAOCAIVDEN"

    plaintext = "In the café, the bánh mì sandwich is a popular choice among the regulars. The flaky baguette, stuffed with savory grilled pork, pickled daikon and carrots, fresh cilantro, and a dollop of sriracha mayo, is the perfect lunchtime indulgence. As I sipped my matcha latte, I noticed the barista's shirt had a cute ねこ (neko, or cat) graphic on it. It reminded me of the time I visited Tokyo and saw the famous 東京タワー (Tokyo Tower) at night, aglow with colorful lights. The world is full of unique and beautiful symbols, and Unicode makes it possible to express them all in one cohesive language."

    rails = 3  # number of rails; MUST be < len(plaintext)

    main(plaintext, rails)
