#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

HOST = '127.0.0.1'
PORT = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    print('Please enter the mode (1 or 2)\nMode 1 for manual\nMode 2 for auto read txt file\n q for exit')
    mode = input('Mode : ')
    match mode:
        case 'q':     #quit
            s.close()
            print("Quit~")   #connection break
            print("Connection close !")
            break
        case '1':     #single line command mode
            while True:
                print('Enter your formula(enter q to stop looping)')
                outdata = input()
                if(outdata == 'q'):break
                print('send: ' + outdata)
                s.send(outdata.encode())
                indata = s.recv(1024)
                print('Recieved from server ->' + indata.decode())
            s.send(('quit mode').encode())
            
        case '2':     #txt file mode
            s.send(('write file').encode())
            
            print("sending: " + 'Testcase.txt')
            with open('Testcase.txt', 'rb') as f:
                raw = f.read()
            # Send actual length ahead of data, with fixed byteorder and size
            s.sendall(len(raw).to_bytes(8, 'big'))
            # You have the whole thing in memory anyway; don't bother chunking
            s.sendall(raw)

            
            f=open('Testcase.txt', mode='r')
            data=f.readlines()

            f=open('Ans.txt', mode='w')
            res=[]
            for lines in data:
                lines.replace('\n', '')
                s.send(lines.encode())

                indata = s.recv(1024)
                res.append(indata.decode()+'\n')
            f.writelines(res)
            f.close()
            s.send(('exit write file').encode())
        case _:         #error input, input again
            print('Invalid mode')
            mode = input('Mode : ')