
from socket import socket
from zlib import decompress
import socket
import pygame
from pygame.locals import KEYDOWN
from pygame.locals import K_ESCAPE
import autopy
from time import sleep

WIDTH = 300
HEIGHT = 300


def recvall(conn, length):
    """ Retreive all pixels. """

    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf

PORT=5001
def main(host='192.168.1.37', port=5000):
    
	    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    done = False
    mi = MouseClass()
    
    clock = pygame.time.Clock()
    watching = True    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

     s.connect((host,port))
     c=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     c.connect((host,PORT))
     try:
        while watching:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    watching = False
                    break

            size_len = int.from_bytes(s.recv(1), byteorder='big')
            size = int.from_bytes(s.recv(size_len), byteorder='big')
            pixels = decompress(recvall(s, size))

            img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')
            
            screen.blit(img, (0, 0))
            pygame.display.flip()
            clock.tick(60)
            (ch, X, Y, LB, CB, RB) = mi.getMouseValues(done)

            string = ch+","+str(X)+","+str(Y)+","+str(LB)+","+str(CB)+","+str(RB)
            x=X.to_bytes(2,'big')

            print(string)
            bayt=bytes(string, 'utf-8')

            print(type(bayt))
            print(bayt)
            c.send(bayt)
            print(100)

     finally:
        s.close()
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
		else:
			try:
				autopy.key.toggle(eval("autopy.key.K_"+ch.upper()), True)
			except:
				pass
		if LB == 1:
			autopy.mouse.click(LEFT_BUTTON)
		elif CB == 1:
			autopy.mouse.click(CENTER_BUTTON)
		elif RB == 1:
			autopy.mouse.click(RIGHT_BUTTON)


if __name__ == '__main__':
    main()
