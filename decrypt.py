import os
import sys
import json
import base64

from Crypto.Cipher import AES  # pip install pycrypto

salt = "tu89geji340t89u2"
passphrase = bytes.fromhex('a7ca9f3366d892c2f0bef417341ca971b69ae9f7bacccffcf43c62d1d7d021f9')
cipher = AES.new(passphrase, AES.MODE_CBC, salt)

def encrypt_save_file(in_json_file, out_save_file):
    if os.path.isfile(in_json_file):
        file_contents = open(in_json_file, "r").read()
        
        encrypted = base64.b64encode(cipher.encrypt(utils.pkcs7_pad_str(file_contents)))
        open(out_save_file, "w").write(encrypted)
    else:
        raise Exception("Input file \"{}\" doesn't exist!".format(input_file))

def decrypt_save_file(in_save_file, out_json_file, pretty_json = True):
    if os.path.isfile(in_save_file):
        file_contents = open(in_save_file, "rb").read()
        
        decrypted = cipher.decrypt(base64.b64decode(file_contents))
        decrypted = decrypted.decode('ascii')
        
        if decrypted[-1] != "}":  #fix numerous different paddings
            decrypted = decrypted.rstrip(decrypted[-1])
        
        if pretty_json:
            decrypted = json.dumps(json.loads(decrypted), indent=4)
        
        open(out_json_file, "w").write(decrypted)
    else:
        raise Exception("Input file \"{}\" doesn't exist!".format(input_file))

class utils(object):
    @staticmethod
    def pkcs7_pad_str(s):
        padding_count = (16 - len(s) % 16)
        return s + (padding_count * chr(padding_count))

try:
    args = [sys.argv[x] for x in range(1, len(sys.argv))]  #remove first arg
    if len(args) == 3:
        mode = args[0].lower()
        input_file = args[1]
        output_file = args[2]
        if mode == "decrypt" or mode == "encrypt":
            if mode == "decrypt":
                print("Decrypting \"{}\" to \"{}\"...".format(input_file, output_file))
                decrypt_save_file(input_file, output_file)
                print("Done!")
            elif mode == "encrypt":
                print("Encrypting \"{}\" to \"{}\"...".format(input_file, output_file))
                encrypt_save_file(input_file, output_file)
                print("Done!")
        else:
            print("Invalid mode specified.")
            print("Mode should be either encrypt or decrypt.")
    else:
        print("Not enough arguments (" + str(len(args)) + " given out of 3)")
        print("USAGE: (encrypt/decrypt) (input file) (output file)")
except Exception as err:
    print(err.args)

print("Press ENTER to exit...")
input()  #wait on enter

'''
#example for modding lunchboxes
num_boxes = 4000
modded_json = json.loads(open("modded.json", "r").read())
for x in range(0, num_boxes):
    modded_json["vault"]["LunchBoxesByType"].append(0)
    modded_json["vault"]["LunchBoxesCount"] += 1
open("modded.json", "w").write(json.dumps(modded_json))
'''