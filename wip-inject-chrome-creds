import sqlite3
import sys
import os
import argparse
import getpass
import win32crypt
from Crypto import Random
from Crypto.Cipher import AES
import json
import base64
from random import randint
def encryptPassword(masterKey, password):
    sig = b"v10"
    iv = Random.new().read(AES.block_size)
    iv = iv[:12]
    cipher = AES.new(masterKey, AES.MODE_GCM, nonce=iv)
    pData = cipher.encrypt(password.encode())
    chromeBlob = sig + iv + pData
    return chromeBlob

def dbCall(passwd):
    args = get_args()
    db = sqlite3.connect(args.database)
    c = db.cursor()
    date_created = randint(13182295255399971,13282295255399971)
    sqlParams = ("https://www.linkedin.com", "https://www.linkedin.com", "https://www.linkedin.com", "admin", passwd,date_created,"0","0")
    c.execute('INSERT INTO logins (origin_url,action_url,signon_realm,username_element,password_element,date_created,blacklisted_by_user,scheme) VALUES (?,?,?,?,?,?,?,?)', sqlParams)
    db.commit()
    db.close()

def getEncryptedKey(json_file):
    with open(json_file, encoding='utf-8') as json_data:
        d = json.load(json_data)
        os_crypt_key = d['os_crypt']['encrypted_key']
    return os_crypt_key

def decryptMasterKey(encryptedKey):
    encryptedKey = base64.b64decode(encryptedKey)
    encryptedKey = encryptedKey[5:]
    masterKey = win32crypt.CryptUnprotectData(encryptedKey, None, None, None, 0)
    return masterKey[1]

def get_args():
    uName = getpass.getuser()
    defaultFile = "C:\\Users\\" + uName + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
    defaultLocalState = "C:\\Users\\" + uName + "\\AppData\\Local\\Google\\Chrome\\User Data\\Local State"
    parser = argparse.ArgumentParser(description='Inject password data into ChromeDB')
    parser.add_argument('-d', '--database', help='Chrome database file', required=False, default=defaultFile)
    parser.add_argument('-s', '--defaultstate', help="This is the Chrome Default State file which contains the DPAPI master key", required=False, default=defaultLocalState )
    parser.add_argument('-i', '--input', help='Input CSV', required=False)
    return parser.parse_args()



def main():
    args = get_args()
    encryptedKey = getEncryptedKey(args.defaultstate)
    masterKey = decryptMasterKey(encryptedKey)
    chromePass = encryptPassword(masterKey, "Hello World!")
    dbCall(chromePass)

if __name__ == '__main__':
    main()
