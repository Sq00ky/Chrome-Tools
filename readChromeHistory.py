import sqlite3
import sys
import os
import argparse
import getpass


def get_args():
    uName = getpass.getuser()
    defaultFile = "C:\\Users\\" + uName + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"
    parser = argparse.ArgumentParser(description='Get Browser history from Chrome database')
    parser.add_argument('-d', '--database', help='Chrome database file', required=False, default=defaultFile)
    parser.add_argument('-o', '--output', help='Output file')
    return parser.parse_args()


def get_history(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT * FROM urls")
    return c.fetchall()

def main():
    args = get_args()
    history = get_history(args.database)
    if args.output != None:
        with open(args.output, 'w', encoding="utf-8") as f:
            for url in history:
                line = ' '.join(str(x) for x in url)
                f.write(line + "\n")
        f.close()
    else:
        for url in history:
            print(url)

if __name__ == '__main__':
    main()
