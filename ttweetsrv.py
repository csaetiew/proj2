#!/usr/bin/python           # This is server.py file                                                                                                                                                                           

import socket               # Import socket module
import thread
import sys

current_users = []  # list of users in str
addr_user = {}
user_tags = {}
tweet_box = {}      # username to list of tweets
user_socket = {}

def on_new_client(clientsocket,addr):
    user = ""
    while True:
        msg = clientsocket.recv(1024).decode('ASCII')
        command = msg.split(" ")[0]
        print("received " + msg)

        if command == "exit":
            if exit(clientsocket, addr, user):
                ret = "exited"
                clientsocket.send(ret.encode())
            else:
                print("Something is wrong with exiting")
            break

        elif command == "tweet":
            message_array = msg.split("\"")
            new_message = ""
            print(message_array)
            for x in range(1, len(message_array) - 1):
                new_message += message_array[x]
            print(new_message)
            if len(new_message) > 150:
                print("Length of message is over 150 characters")
                ret = "err3"
                clientsocket.send(ret.encode())
            tag = message_array[len(message_array) - 1][1:]

            tweet(clientsocket, addr, new_message, tag)
            ret = "succ3"
            clientsocket.send(ret.encode())
        

        elif command == "login":
            username = msg.split(" ")[1]
            user = username
            if not login(clientsocket, addr, user):
                print("login failed")
                ret = "err0"
                clientsocket.send(ret.encode())
                break
            else:
                print("login succeded")
                ret = "succ0"
                clientsocket.send(ret.encode())

        elif command == "subscribe":
            tag = msg.split(" ")[1]
            if not subscribe(clientsocket, addr, tag, user):
                print("subscription failed")
                ret = "err1 " + tag
                clientsocket.send(ret.encode())
            else:
                print("subscription succeded")
                ret = "succ1 " + tag
                clientsocket.send(ret.encode())

        elif command == "unsubscribe":
            tag = msg.split(" ")[1]
            if not unsubscribe(clientsocket, addr, tag, user):
                print("unsubscription failed")
                ret = "err2 " + tag
                clientsocket.send(ret.encode())
            else:
                print("unsubscription succeded")
                ret = "succ2 " + tag
                clientsocket.send(ret.encode())

        elif command == "timeline":
            ret = ""
            for message in tweet_box[user]:
                ret = ret + message + "\n"
            if ret =="":
                retval = "err4"
                clientsocket.send(retval.encode())
            else:
                retval = "succ4 " + ret
                clientsocket.send(retval.encode())
        else:
            ret = "err5"
            clientsocket.send(ret.encode())

        # something = "hello my friend"

        #do some checks and if msg == someWeirdSignal: break:

        #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
    clientsocket.close()

def login(clientsocket, addr, username):
    print("on login")

    for user in current_users:
        if username == user:
            return False
    print("  " + username)
    addr_user[addr] = username
    current_users.append(username)
    tweet_box[username] = []
    user_tags[username] = []
    user_socket[username] = clientsocket

    print(current_users)
    return True

def exit(clientsocket, addr, username):
    print("on exit")
    current_users.remove(username)
    tweet_box.pop(username, None)
    user_tags.pop(username, None)
    user_socket.pop(username, None)
    addr_user.pop(addr, None)
    return True

def tweet(clientsocket, addr, message, tags):
    print("on tweet")
    print(tags)
    tags_tweeted = tags.split("#")
    tags_tweeted.append("ALL")
    print(tags_tweeted)

    for user in user_tags:
        target = False
        for tag in user_tags[user]:
            if target:
                break
            for tag_tweeted in tags_tweeted:
                if target:
                    break
                if tag == tag_tweeted or tag == "ALL": 
                    target = True
                    twt = "succ5 " + addr_user[addr] + ": " + message + " " + tags
                    user_socket[user].send(twt.encode())
                    break
                

    return True

def subscribe(clientsocket, addr, tag, username):
    tag = tag[1:]
    print("on subscribe")
    current_tags = user_tags[username]
    for subbed_tag in current_tags:
        if subbed_tag == tag:
            return True
    if len(current_tags) == 3:
        return False
    user_tags[username].append(tag)
    return True

        


def unsubscribe(clientsocket, addr, tag, username):
    tag = tag[1:]
    print(tag)
    print("on unsubscribe")
    current_tags = user_tags[username]
    for subbed_tag in current_tags:
        if subbed_tag == tag:
            user_tags[username].remove(subbed_tag)
            return True
    return False

def timeline(clientsocket, addr, msg):
    print("on timeline")
    return


def main():
    if len(sys.argv) !=2:
        print("python ttweetsrv.py <Port>")

    s = socket.socket()         # Create a socket object
    host = '127.0.0.1' # Get local machine name
    port = int(sys.argv[1])                # Reserve a port for your service.

    print ('Server started!')
    print ('Waiting for clients...')

    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.

    while True:
        if len(current_users) >5:
            continue
        c, addr = s.accept()     # Establish connection with client.
        thread.start_new_thread(on_new_client,(c,addr))
        #Note it's (addr,) not (addr) because second parameter is a tuple
        #Edit: (c,addr)
        #that's how you pass arguments to functions when creating new threads using thread module.
    s.close()

if __name__== "__main__":
  main()