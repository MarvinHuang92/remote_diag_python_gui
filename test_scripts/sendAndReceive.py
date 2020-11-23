# -*- coding: UTF-8 -*-

import time

def main(msg):
    if not msg == '':
        print("Tx: " + msg)
        time.sleep(0.2)
        
def main_return(msg):
    if not msg == '':
        return ("Tx2: " + msg)

if __name__ == "__main__":
    main()