#!/usr/bin/env python

import socket
import sys
import thread

def listen(s, msgbox):
    print("the thred runs")
    while True:
        MESSAGE = input()
        if MESSAGE == "timeline":
            print(msgbox[0])
            msgbox[0] = ""
            continue
        # if MESSAGE.split(" ")[0] == "tweet":
        #     if 
        s.send(MESSAGE.encode())

def main():
    if len(sys.argv) !=4:
        print("python ttweetcl.py <ServerIP> <ServerPort> <Username>")
        return

    TCP_IP = sys.argv[1]
    TCP_PORT = int(sys.argv[2])
    BUFFER_SIZE = 1024
    MESSAGE = "login " + sys.argv[3]

    IP_test = TCP_IP.split(".")
    for ip in IP_test:
        if int(ip) < 0 or int(ip) > 255:
            print("IP should be in [0, 255]")
            return

    if TCP_PORT < 0 or TCP_PORT > 65535:
        print("port number should be in [1,65535]")
        return

    msgbox = []
    msgbox.append("")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((TCP_IP, TCP_PORT))
    except socket.error:
        print ("Could not connect with server")
        return

    thread.start_new_thread(listen,(s, msgbox))
    s.send(MESSAGE.encode())

    while True:
        data = ''
        while True:
            part = s.recv(BUFFER_SIZE).decode('ASCII')
            data += part
            if len(part) < BUFFER_SIZE:
                break
        code = data.split(" ")[0]
        if code == "err0":
            print("The user " + sys.argv[3] + " is already logged in")
            break
        elif code == "succ0":
            print("logged in as " + sys.argv[3])
        elif code == "err1":
            print("Could not subscribe to " + data.split(" ")[1])
        elif code == "succ1":
            print("successfully subscribed to " + data.split(" ")[1])
        elif code == "exited":
            print("Successfully Logged out")
            break
        elif code == "err2":
            print("You're not subscribed to " +  data.split(" ")[1])
        elif code == "succ2":
            print("Successfully unsubscribed from " +  data.split(" ")[1])
        elif code == "err3":
            print("Length of message is over 150 characters")
        elif code == "succ3":
            print("Successfully tweeted")
        elif code == "err4":
            print("No messages")
        elif code == "succ4":
            print(msgbox)
        elif code == "succ5":
            if len(msgbox[0]) == 0:
                msgbox[0] +=  data[6:]
            else:
                msgbox[0] +=  "\n" + data[6:]

        elif code =="err5":
            print("Not a proper command")
        print ("received data:", data)

    s.close()


if __name__== "__main__":
  main()