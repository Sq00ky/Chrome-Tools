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
import pandas as pd
from random import randint

def encryptPassword(masterKey, password):
	sig = b"v10"
	iv = Random.new().read(AES.block_size)
	iv = iv[:12]
	cipher = AES.new(masterKey, AES.MODE_GCM, iv)
	pData = cipher.encrypt(password.encode())
	chromeBlob = sig + iv + pData
	return chromeBlob
    

def dbCall(userUrl, userEmail, encryptedPassword):
	args = get_args()
	db = sqlite3.connect(args.database)
	c = db.cursor()
	origin_url = userUrl
	action_url = userUrl + "/login"
	username_element = "email"
	username_value = userEmail
	password_element = encryptedPassword
	submit_element = ""
	signon_realm = userUrl
	date_created = randint(13182295255399971,13282295255399971)
	blacklisted_by_user = 0
	scheme = 0
	password_type = 0
	times_used = randint(1,15)
	form_data = b"\x01\x00\x00\x07\x00\x00\x00\x08\x00\x00\x00u\x00_\x000\x00_\x00a\x00_\x005\x00x\x00\x19\x00\x00\x00" + bytes(userUrl, encoding="utf-8") + b"\x00\x00\x00\x1f\x00\x00\x00" + b"https://www.facebook.com/login/" + b"\x00\x02\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00e\x00m\x00a\x00i\x00l\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00" + b"text"  + b"\x00\x00\x00\x00\xff\xff\xff\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00p\x00a\x00s\x00s\x00\x00\x00\x00\x00\x08\x00\x00\x00" + b"password" + b"\x00\x00\x00\x00\xff\xff\xff\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00"
	display_name = ""
	icon_url = ""
	federation_url = ""
	skip_zero_click = "0"
	generation_upload_status = "0"
	possible_username_pairs = b'\x00\x00\x00\x00'
	date_last_used = date_created
	moving_blocked_for = b'\x00\x00\x00\x00'
	date_password_modified = date_created
	sqlParams = (origin_url, action_url, username_element, username_value, password_element, submit_element, signon_realm, date_created, blacklisted_by_user, scheme, password_type, times_used, form_data, display_name, icon_url, federation_url, skip_zero_click, generation_upload_status, possible_username_pairs, date_last_used, moving_blocked_for, date_password_modified)
	try:
		c.execute('INSERT INTO logins (origin_url, action_url, username_element, username_value, password_element, submit_element, signon_realm, date_created, blacklisted_by_user, scheme, password_type, times_used, form_data, display_name, icon_url, federation_url, skip_zero_click, generation_upload_status, possible_username_pairs, date_last_used, moving_blocked_for, date_password_modified) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', sqlParams)
		db.commit()
	except:
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
	parser.add_argument('-s', '--defaultstate', help="This is the Chrome Default State file which contains the encrypted DPAPI master key", required=False, default=defaultLocalState )
	parser.add_argument('-i', '--input', help='Input CSV', required=True)
	return parser.parse_args()

def readUsernames(input):
	"""
	Read URLs from input file.
	"""
	column_list = ["username", "password", "url"]
	df = pd.read_csv(input, names=column_list)
	return(df["username"].tolist())


def readPasswords(input):
	"""
	Read URLs from input file.
	"""
	column_list = ["username", "password", "url"]
	df = pd.read_csv(input, names=column_list)
	return(df["password"].tolist())


def readURLs(input):
	"""
	Read URLs from input file.
	"""
	column_list = ["username", "password", "url"]
	df = pd.read_csv(input, names=column_list)
	return(df["url"].tolist())

def main():
	args = get_args()
	usernameList = readUsernames(args.input)
	cleartextPasswordsList  = readPasswords(args.input)
	urlList = readURLs(args.input)
	encryptedKey = getEncryptedKey(args.defaultstate)
	masterKey = decryptMasterKey(encryptedKey)
	for i in range(len(readPasswords(args.input))):
		encryptedPassword = encryptPassword(masterKey, cleartextPasswordsList[i])
		try:  
			dbCall(urlList[i], usernameList[i], encryptedPassword)
		except:
			print("Failed to add password for " + usernameList[i] + " to ChromeDB")
		print("Successfully added " + usernameList[i] + " to ChromeDB")

if __name__ == '__main__':
	main()
