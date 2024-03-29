Keystate = [0x6A, 0x7C, 0xC0, 0xEA, 0x4C, 0xC9, 0xA3, 0x37, 0xA9, 0x78, 0x55, 0x37, 0x16, 0x57, 0xC1, 0x15,
0xBF, 0x2A, 0x69, 0xE9, 0x8B, 0x5D, 0xE1, 0xCB, 0x42, 0xEB, 0xEE, 0xA9, 0xB2, 0x33, 0x07, 0xA2,
0xE7, 0x09, 0x3D, 0x78, 0x52, 0xD1, 0xA8, 0x3F, 0x42, 0x85, 0xED, 0x43, 0xAA, 0xBC, 0x56, 0x7B,
0xB9, 0x79, 0x0F, 0xE8, 0x7E, 0x9C, 0x2A, 0x5B, 0x07, 0xEA, 0xB3, 0xA8, 0x43, 0xB6, 0x9A, 0x24,
0xD0, 0x5E, 0x26, 0xCD, 0xD7, 0xA7, 0x83, 0x66, 0x03, 0x06, 0xAD, 0xC4, 0xD6, 0x2F, 0x81, 0xEE,
0x1E, 0x17, 0x73, 0x85, 0xE5, 0xFB, 0x90, 0xBA, 0x71, 0x6F, 0xC7, 0xDD, 0x83, 0xD4, 0xD9, 0x42,
0x22, 0x92, 0xCE, 0x50, 0x6E, 0x24, 0xC4, 0x92, 0xB8, 0x2D, 0x62, 0xEC, 0xA8, 0x47, 0xFD, 0xB5,
0x7C, 0x8B, 0x27, 0x4A, 0x63, 0x12, 0xB9, 0x80, 0x00, 0xF8, 0xAC, 0xB6, 0x61, 0xEA, 0x0C, 0xA9,
0x58, 0x53, 0x04, 0x12, 0x47, 0xE6, 0xF3, 0xA4, 0xF3, 0x34, 0x49, 0xA3, 0xE0, 0x9E, 0x36, 0x0D,
0xC9, 0xA0, 0x1F, 0x0F, 0xFE, 0x0A, 0x54, 0x79, 0xF8, 0x29, 0xA3, 0xE8, 0x98, 0xBF, 0x43, 0x7E,
0x80, 0x00, 0xD6, 0x6E, 0x81, 0xE0, 0x2D, 0x9F, 0x5B, 0x65, 0x07, 0x24, 0xE2, 0xCD, 0x8E, 0x8C,
0xC5, 0xED, 0x71, 0xAC, 0xBF, 0xD6, 0x6A, 0x95, 0x11, 0x06, 0x66, 0x74, 0x03, 0xC0, 0xAF, 0x7E,
0x39, 0x4A, 0x8F, 0xB8, 0xDD, 0x0A, 0x88, 0xC9, 0x9A, 0xB2, 0x46, 0x71, 0xD1, 0xBF, 0x7D, 0x7E,
0x38, 0xD6, 0xE3, 0x94, 0x84, 0xBD, 0x30, 0x7C, 0x37, 0x81, 0x8D, 0xEF, 0xDF, 0x75, 0x35, 0xE4,
0x56, 0x78, 0x02, 0x37, 0x9A, 0x25, 0x45, 0xE4, 0x7C, 0x8C, 0x28, 0x4B, 0x81, 0xC1, 0x2D, 0x80,
0x26, 0xB2, 0xD2, 0x70, 0xB4, 0x25, 0x5E, 0xE4, 0xDE, 0x93, 0x89, 0x52, 0xA1, 0x43, 0xF7, 0xB1]

import sys, zlib, os

#RC4 based off of https://github.com/bozhu/RC4-Python/blob/master/rc4.py

def KSA():

    S = range(256)
    counter = 0
    v9 = 0
    while counter < 256:
        wide_val = Keystate[counter]
        lookup_val = S[counter]
        v9 = lookup_val + wide_val + v9
        v9 = v9 & 0xFF
        v9_value = S[v9]
        S[counter] = v9_value
        counter += 1
        S[v9] = lookup_val

    return S
 

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  

        K = S[(S[i] + S[j]) % 256]
        yield K

def RC4():
    S = KSA()
    return PRGA(S)


def Get_Files(folder):
    file_list = []
    for filename in os.listdir(folder):
        file_list.append(os.path.join(folder, filename))
    return file_list

def FileWriter(path, data):

    with open(path + "_decrypted", "wb") as f:
        f.write(data)

    return

def FileReader(path):

    with open(path, "rb") as f:
        filebytes = f.read()

    return filebytes

def main(argv):

    if len(sys.argv) < 2:
        print "[!] Script Requires Path To NODE.JS Script Folder!"
        return
    scripts_dir = argv[1]

    print "[*] Getting List of Scripts to Decrypt..."
    file_list = []
    file_list = Get_Files(scripts_dir)

    for filename in file_list:
        decrypted = ""
        print "[*] Reading Script %s into Memory..." % filename
        filebytes = FileReader(filename)
        print "[*] Generating Keystream..."
        keystream = RC4()
        print "[*] Attempting to Decrypt %s..." % filename
      
        for char in filebytes:
            decrypted += chr(ord(char) ^ keystream.next())

        size = decrypted[0:4]
        decrypted = decrypted[4:]

        print "[*] Decompressing %s and Writing to %s_decrypted" % (filename, filename)
        try:
            FileWriter(filename, zlib.decompress(decrypted))
        except Exception as E:
            print "[!] Error Decompressing %s!" % filename
            print "[!]", E

print "[*] Finished Decrypting!"

if __name__ == "__main__":
    main(sys.argv)
