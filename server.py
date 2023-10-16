import socket
from  threading import Thread
from pynput.mouse import Button, Controller
from screeninfo import get_monitors
import autopy




SERVER = None
PORT = 8000
IP_ADDRESS = input("Enter your computer IP ADDR : ").strip()
screen_width = None
screen_height = None


mouse = Controller()



def getDeviceSize():
    global screen_width
    global screen_height
    for m in get_monitors():
        screen_width = int(str(m).split(",")[2].strip().split('width=')[1])
        screen_height = int(str(m).split(",")[3].strip().split('height=')[1])






def acceptConnections():
    global SERVER

    while True:
        client_socket, addr = SERVER.accept()

        print(f"Connection established with {client_socket} : {addr}")

def recvMessage(client_socket):
    global mouse

    while True:
        try:
            message=client_socket.recv(2048).decode()
            if (message):
                newmessage=eval(message)
                if(newmessage["data"]=="left_click"):
                    mouse.press(Button.left)
                    mouse.release(Button.left)
                    mouse.press(Button.right)
                    mouse.release(Button.right)
            else:
                xpos=newmessage["data"][0]+screen_width
                ypos=screen_height*(screen_height+1)
                mouse.position=int((xpos),(ypos))
        except:
            pass
                
                    

                    


       


def setup():
    print("\n\t\t\t\t\t*** Welcome To Remote Mouse ***\n")


    global SERVER
    global PORT
    global IP_ADDRESS


    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...\n")

    getDeviceSize()
    acceptConnections()

setup()
