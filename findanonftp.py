import socket
import random
import struct
import threading
import ftplib
from ftplib import FTP


def generate_ipaddress():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))


def write_ipaddress(ipaddress):
    try:
        with open("found.txt", "a") as f:
            f.write(ipaddress + "\n")
    except FileNotFoundError as e:
        with open("found.txt", "w") as f:
            f.close()
        write_ipaddress(ipaddress)


def checkFTP(host):
    try:
        ftp = FTP(host)
        response = ftp.login()
        if "2" in response:
            print("[+] Anonymous connection allowed.")
            dirLength = len(ftp.nlst())
            dirContent = ftp.nlst()
            if dirContent is not None and dirLength != 0:
                if dirContent[0] == "." and dirContent[1] == "..":
                    print("[-] Empty directory.")
                elif dirLength == 1 and dirContent[0] == "pub":
                    ftp.cwd("pub")
                    dirLengthpub = len(ftp.nlst())
                    dirContentpub = ftp.nlst()
                    if dirLengthpub == 1:
                        if dirContentpub[0] == "." and dirContentpub[1] == "..":
                            print("[-] Empty directory.")
                        else:
                            print("[+] IP: %s" % host)
                            write_ipaddress(f"[+] IP: {host} LENGTH: {str(dirLength)}")
                    else:
                        print("[-] Empty directory.")
                else:
                    print("[+] IP: %s" % host)
                    write_ipaddress(f"[+] IP: {host} LENGTH: {str(dirLength)}")
            else:
                print("[-] Empty directory.")
        else:
            print(f"Server response: %s" % response)

    except ftplib.error_perm:
        print("[-] Anonymous not allowed")
    except Exception as e:
        print(f"Error: {e}")



def checkPort(host):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        if s.connect_ex((host, 21)) == 0:
            print("[DEBUG] %s port is open/filtered" % host)
            checkFTP(host)
    except TimeoutError as e:
        pass
    except Exception as e:
        print("Error: %s" % str(e))


def routine():
    while True:
        ip_address = generate_ipaddress()
        checkPort(ip_address)


if __name__ == '__main__':
    threads = []
    for i in range(2000):
        thread = threading.Thread(target=routine)
        thread.start()
        threads.append(thread)
