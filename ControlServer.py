
import socket
import sys
import serial
from _thread import *

LEFT_AXIS = 1
LEFT_MOTOR = '0'
RIGHT_AXIS = 3
RIGHT_MOTOR = '2'
LINEAR_BUTTF = 4
LINEAR_BUTTB = 6
LINEAR_MOTOR = '6'
HOPPER_MOTOR = '1'
HOPPER_BUTT = 5
HOPPER_HALFBUTT= 7
BUCKET_MOTOR = '7'
BUCKET_BUTTF = 3
BUCKET_BUTTB = 0
ARM_MOTOR = '3'
ARM_BUTTF = 1
ARM_BUTTB = 2

ESTOP_BUTT = 8

FSPEED = 999
HSPEED = 650
BSPEED= 0
ARMSPEED = 50
STOP = 500

def clientThread(conn):
	port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)
	hopperHalf = False
	incArmPlus = False
	incArmMinus = False
	armPos = 500;
	port.write(("S:" + ARM_MOTOR + ":" + str(armPos) + "\r\n").encode("ascii"))
	while True:
		data = ''
		while('\r\n' not in data):
			data += conn.recv(1).decode('ascii')
		data.replace('\r\n', '')
		if 'A' in data or 'B' in data:
			splitData = data.split(':')
			serialCmd = "S:"
			
			if splitData[0] == 'A':
				speed = float(splitData[2])
				speed = speed*-1
				cmdSpeed = int(round((speed+1)*499))
				if int(splitData[1]) == LEFT_AXIS:
					serialCmd += LEFT_MOTOR
				else:
					serialCmd += RIGHT_MOTOR
				serialCmd += ':' + str(cmdSpeed)
			else:
				buttNo = splitData[1]
				buttVal = splitData[2]
				cmdSpeed = STOP
				if int(buttNo) == ESTOP_BUTT:
					serialCmd+="S"
				elif int(buttNo) == LINEAR_BUTTF or int(buttNo) == LINEAR_BUTTB:
					serialCmd+=LINEAR_MOTOR + ':'
					if int(buttVal) != 0 :
						if int(buttNo) == LINEAR_BUTTF:
							cmdSpeed = FSPEED
						else:
							cmdSpeed = BSPEED
				elif int(buttNo) == HOPPER_HALFBUTT:
					hopperHalf = not hopperHalf
				elif int(buttNo) == HOPPER_BUTT:
					if int(buttVal) !=0:
						if hopperHalf:
							cmdSpeed = HSPEED
						else:
							cmdSpeed = FSPEED
					serialCmd += HOPPER_MOTOR + ':'
				elif int(buttNo) == BUCKET_BUTTF or int(buttNo) == BUCKET_BUTTB:
					serialCmd+=BUCKET_MOTOR + ':'
					if int(buttVal) != 0:
						if int(buttNo) == BUCKET_BUTTF:
							cmdSpeed = FSPEED
						else:
							cmdSpeed = BSPEED
				elif int(buttNo) == ARM_BUTTF:
					incArmPlus = not incArmPlus
				elif int(buttNo) == ARM_BUTTB:
					incArmMinus = not incArmMinus
				if "S:S" not in serialCmd:
					serialCmd += str(cmdSpeed)
			serialCmd  += '\r\n'	
			port.write(serialCmd.encode("ascii"))
		if incArmPlus or incArmMinus:
			if incArmPlus:
				armPos+=ARMSPEED
				if armPos > 999:
					armPos = 999
			elif incArmMinus:
				armPos-=ARMSPEED
				if armPos < 0:
					armPos = 0
		port.write(("S:" + ARM_MOTOR + ":" + str(armPos) + "\r\n").encode("ascii"))
				
def powerMonitorThread():
	while True:
		print('h')

#Main Program
HOST = ''
PORT = 10000

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	s.bind((HOST, PORT))
except:
	print ('Fatal Error, no recovery available. Socket failed to bind.')

s.listen(5)
while 1:
	conn, addr = s.accept()
	print ('Connected with ' + addr[0] + ':' + str(addr[1]))
	start_new_thread(clientThread, (conn,))
	#s.close()
    
