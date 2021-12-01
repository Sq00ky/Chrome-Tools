import sqlite3
import sys
import os
import argparse
import getpass

def arg_parser():
    uName = getpass.getuser()
    defaultFile = "C:\\Users\\" + uName + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
    parser = argparse.ArgumentParser(description='Get Login Data from Chrome database')
    parser.add_argument('-d', '--database', help='Chrome database file', required=False, default=defaultFile)
    return parser.parse_args()


def get_history(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT * FROM logins")
    print(c.fetchall())
    return c.fetchall()

def main():
    args = arg_parser()
    get_history(args.database)

if __name__ == '__main__':
    main()
