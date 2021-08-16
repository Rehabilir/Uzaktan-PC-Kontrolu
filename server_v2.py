
from socket import socket
from threading import Thread
from zlib import compress

from mss import mss

import socket

import pygame
from pygame.locals import KEYDOWN
from pygame.locals import K_ESCAPE
import autopy
from time import sleep

WIDTH = 300
HEIGHT = 300


def retreive_screenshot(conn,conc):
    a=2
    with mss() as sct:
        
        rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}   
        
        while True :
            
            if a==1:
                a=a+1
            while a>1 :
                img = sct.grab(rect)                        
            
                pixels = compress(img.rgb, 9)               

            
                size = len(pixels)                          
                size_len = (size.bit_length() + 7) // 8
                conn.send(bytes([size_len]))

                size_bytes = size.to_bytes(size_len, 'big') 
                conn.send(size_bytes)

                conn.sendall(pixels)                        
                data = conc.recv(1024)

                data1 = data.decode('utf-8')

                data2=data1.split(',')
                ch=data2[0]
                X=int(data2[1])
                Y=int(data2[2])
                LB=int(data2[3])
                CB=int(data2[4])
                RB=int(data2[5])
                print (ch, X, Y, LB, CB, RB)
                mi.setMouseValues(ch,X,Y,LB,CB,RB)
                a=a-1
PORT=5001
def main(host='192.168.1.37', port=5000):
    
    pygame.init()
    
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))

    c=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    c.bind((host, PORT))

    
    try:
        s.listen()
        c.listen()
        print('Server started.')

        while True :
            
            conn, addr = s.accept()
            print('Client connected IP:', addr)
            conc, addr = c.accept()
            print('Client connected IP:', addr)

            retreive_screenshot(conn,conc)
        
    finally:
        s.close()
        c.close()
        print(1)
        
class MouseClass:
	def getMouseValues(self,done):
		(ch, LB, CB, RB) = ('None',0, 0, 0)
		for event in pygame.event.get():

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					
				else:
					print (pygame.key.name(event.key))
					ch = pygame.key.name(event.key)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				print ("in mousebuttondown")
				print ("mouse  : %d" %event.button)
				if event.button == 1:
					LB = 1
				elif event.button == 2:
					CB = 1
				elif event.button == 3:
					RB = 1
		(X,Y) = pygame.mouse.get_pos()
		print ("%d %d %d %d %d" %(X ,Y ,LB ,CB ,RB))
		return (ch, X, Y, LB, CB, RB)

	def setMouseValues(self, ch, X, Y, LB, CB, RB):
		autopy.mouse.move(int(X),int(Y))
		if " " in ch:
				ch = ch.split(" ")[1]
		if len(ch) == 1:
			autopy.key.toggle(ch,True)
		elif ch == "space":
			autopy.key.toggle(' ',True)
		if LB == 1:
			autopy.mouse.click(LEFT_BUTTON)
		elif CB == 1:
			autopy.mouse.click(CENTER_BUTTON)
		elif RB == 1:
			autopy.mouse.click(RIGHT_BUTTON)
			
if __name__ == '__main__':
    
      mi=MouseClass()
      main()

      
      
