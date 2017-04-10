import socket
import time
import sys
import pygame
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.1.10', 10000)
command = '0x122222' #String is same thing as byte array in python

#PyGame init
pygame.init()
#windowSize = width,height = 200,150
#screen = pygame.display.set_mode(windowSize)

j = pygame.joystick.Joystick(0) # create a joystick instance

try:
    j.init() # init instance
    print ('Enabled joystick: ' + j.get_name())
except pygame.error:
    print ('no joystick found.')

try:
    sock.connect(server_address)
    #Send Key Press
    while 1:
        for event in pygame.event.get():
            shouldSend = False
            command = ""
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 1 or event.axis == 3:
                    value = str(round(event.value,3))
                    command = "A:" + str(event.axis) + ":" + value;
                    shouldSend = True
            if event.type == pygame.JOYBUTTONUP or event.type == pygame.JOYBUTTONDOWN:
                value = 1
                if event.type == pygame.JOYBUTTONUP:
                    value = 0;
                command = "B:" + str(event.button) + ":" + str(value)
                shouldSend = True;
            if shouldSend:
                print(command)
                command += "\r\n"
                sock.sendall(command.encode("ascii"))

finally:
    print (sys.stderr, 'closing socket')
    sock.close()

