import socket
s = socket.socket(socket.AF_INET ,socket.SOCK_DGRAM)
s.bind(('127.0.0.1' , 12344))

print("server is running ........")
print("ip : 127.0.0.1 , port : 12344 \n")
while True:
   # recieve data from client 
   rData , address = s.recvfrom(1024)
   # decode received data
   data = rData.decode('UTF-8')
   print(" data : -- {} -- received from : {} ".format(data ,address))
   # send data to client 
   print("input your msg ")
   sData = input()
   s.sendto(sData.encode('UTF-8') , address )