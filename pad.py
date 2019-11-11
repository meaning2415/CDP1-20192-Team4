from tkinter import *
from tkinter import ttk
from socket import *
import picamera
import os

global clientSock
global camera

def get_Fsize(fname):
    fileSize = os.path.getsize("./" + fname)
    return str(fileSize)

def getFData(fname):
    data = b""
    with open("./" + fname, "rb") as f:
        for  line in f:     
            data += line

    return data

def button_pressed(value):
    number_entry.insert("end",value)
    clientSock.send(str(value).encode())
    for i in range(1, 6):
        fname = str(i) + ".jpg"
        camera.capture(fname)

        #send filesize
        clientSock.send(get_Fsize(fname).encode())

        clientSock.sendall(getFData(fname))
        
        #clientSock.recv(1)
    
    print(value,"pressed")
     
def star_button_pressed(value):
    print(value,"pressed")
    clientSock.send(str(value).encode())
    result = clientSock.recv(1).decode()
    print(result)
    
def num_button_pressed():
    print("# pressed")
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


address = '192.168.43.126'
port = 8080

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect((address, port))

camera = picamera.PiCamera()

root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
#root.geometry("%dx%d+0+0" % (w, h))
root.geometry("800x640")
 
entry_value = StringVar(root, value='')
 
number_entry = ttk.Entry(root, textvariable = entry_value, width=20)
number_entry.grid(row=0, columnspan=3) 
 
 
button7 = ttk.Button(root, text="7", command = lambda:button_pressed('7'))
button7.grid(row=1, column=0,sticky='NSEW')
button8 = ttk.Button(root, text="8", command = lambda:button_pressed('8'))
button8.grid(row=1, column=1,sticky='NSEW')
button9 = ttk.Button(root, text="9", command = lambda:button_pressed('9'))
button9.grid(row=1, column=2,sticky='NSEW')

button4 = ttk.Button(root, text="4", command = lambda:button_pressed('4'))
button4.grid(row=2, column=0,sticky='NSEW')
button5 = ttk.Button(root, text="5", command = lambda:button_pressed('5'))
button5.grid(row=2, column=1,sticky='NSEW')
button6 = ttk.Button(root, text="6", command = lambda:button_pressed('6'))
button6.grid(row=2, column=2,sticky='NSEW')

button1 = ttk.Button(root, text="1", command = lambda:button_pressed('1'))
button1.grid(row=3, column=0,sticky='NSEW')
button2 = ttk.Button(root, text="2", command = lambda:button_pressed('2'))
button2.grid(row=3, column=1,sticky='NSEW')
button3 = ttk.Button(root, text="3", command = lambda:button_pressed('3'))
button3.grid(row=3, column=2,sticky='NSEW')
#마지막줄 AC,0,=,- 버튼추가
# -버튼 -> math_button_pressed() 로 연결.
# AC,0 버튼 -> button_pressed() 로 연결
# = 버튼 -> equal_button_pressed() 로 연결
button_ac = ttk.Button(root, text="*", command = lambda:star_button_pressed('*'))
button_ac.grid(row=4, column=0,sticky='NSEW')
button0 = ttk.Button(root, text="0", command = lambda:button_pressed('0'))
button0.grid(row=4, column=1,sticky='NSEW')
button_equal = ttk.Button(root, text="#", command = lambda:num_button_pressed())
button_equal.grid(row=4, column=2,sticky='NSEW') 
 
root.mainloop()
