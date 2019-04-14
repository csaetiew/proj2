import socket
import sys
import thread
# Use of thread format comes from https://stackoverflow.com/questions/10810249/python-socket-multiple-clients

# Method that runs on a new thread to accept nonblocking inputs from user
def listen(s, msgbox):
    while True:
        MESSAGE = raw_input() # obtain input from user

        # prints message box and resets box
        if MESSAGE == "timeline":
            print(msgbox[0] + "\n")
            msgbox[0] = ""
            continue
        # Checks that the tweet confirms to length and legal symbols
        if MESSAGE.split(" ")[0] == "tweet":
            message_array = MESSAGE.split("\"")
            new_message = ""
            for x in range(1, len(message_array) - 1):
                new_message += message_array[x]
            if len(new_message) > 150:
                print("Length of message is over 150 characters" + "\n")
                continue
            if len(new_message) < 1:
                print("message format illegal" + "\n")
                continue
        s.send(MESSAGE.encode("utf-8")) # Send message to server

def main():
    # Checks the number of arguements
    if len(sys.argv) !=4:
        print("args should contain <ServerIP>   <ServerPort>   <Username>" + "\n")
        return

    # Initialize IP, PORT, BUFFER_SIZE, initial login message, and username
    TCP_IP = sys.argv[1]
    TCP_PORT = int(sys.argv[2])
    BUFFER_SIZE = 1024
    MESSAGE = "login " + sys.argv[3]
    userName = sys.argv[3]

    # Test range of IP
    IP_test = TCP_IP.split(".")
    for ip in IP_test:
        if int(ip) < 0 or int(ip) > 255:
            print("IP should be in [0, 255]" + "\n")
            return

    # Test range of PORT numbers
    if TCP_PORT < 0 or TCP_PORT > 65535:
        print("port number should be in [1,65535]" + "\n")
        return

    # Initialize message box for user
    msgbox = []
    msgbox.append("")

    # Create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Attempt to connect to server, exit if failed
    try:
        s.connect((TCP_IP, TCP_PORT))
    except socket.error:
        print ("connection error, please check your server: connection refused" + "\n")
        return
    # Start a new thread to allow input from user and send the socket and message box
    thread.start_new_thread(listen,(s, msgbox))

    # Send the login message 
    s.send(MESSAGE.encode("utf-8"))

    while True:
        # Receive data from the server
        data = ''
        while True:
            part = s.recv(BUFFER_SIZE)
            data += part
            if len(part) < BUFFER_SIZE:
                break
        # check the code for success or error and go throught the
        # if statement to print correct report
        code = data.split(" ")[0]
        if code == "err0": # Login error where the username is already taken
            print("The user " + sys.argv[3] + " is already logged in" + "\n")
            break
        elif code == "succ0": # Login success, print confirmation
            print("logged in as " + sys.argv[3] + "\n")
        elif code == "err1": # Subscription error due to 3 limitation or already subscribed
            print("sub " + data.split(" ")[1] + " failed, already exists or exceeds 3 limitation" + "\n")
        elif code == "succ1": # Subscription successful. Print confirmation
            print("Subscribed to " + data.split(" ")[1] + "\n")
        elif code == "exited": # Successfully exited, print confirmation
            print("Successfully Logged out" + "\n")
            break
        elif code == "err2": #
            print("You're not subscribed to " +  data.split(" ")[1] + "\n")
        elif code == "succ2":
            print("Successfully unsubscribed from " +  data.split(" ")[1] + "\n")
        elif code == "err3":
            print("Length of message is over 150 characters" + "\n")
        elif code == "succ3":
            pass 
            # print("Successfully tweeted")
        elif code == "err4":
            print("No messages" + "\n")
        elif code == "succ4":
            print(msgbox)
        elif code == "succ5":
            print("user: " + userName + ", get message: " + data[6:] + "\n")
            if len(msgbox[0]) == 0:
                msgbox[0] += "user: " + userName + ", get timeline: " + data[6:]
            else:
                msgbox[0] += "\n" + "user: " + userName + ", get timeline: " + data[6:]

        elif code =="err5":
            print("Not a proper command" + "\n")
    s.close()


if __name__== "__main__":
  main()