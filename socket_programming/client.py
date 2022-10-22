import socket            
s = socket.socket(socket.AF_INET ,socket.SOCK_DGRAM)        
def chat_Info():
    print(
        """
        [1] Enter [E or e] to exit
        [2] Enter [C or c] to chat
        """
    )    
def action(data):
    data_strip = data.strip()
    
    if data_strip.lower() == 'e':
        return 
    
    elif data_strip.lower() == 'c':
        print('Enter your msg : ')
        print('To exit enter : [e or E]')
        while True : 
 
            sData = input()
            
            if sData.strip().lower() ==  'e':
                print( "EXIT DONE !")
                break
            
            s.sendto(sData.encode('UTF-8') , ('127.0.0.1' , 12344) )
 
            rData , address = s.recvfrom(512) 

            data= rData.decode('UTF-8')

            print(" data : {} received from : {} ".format(data ,address))
    else : 
        print('selection e or c')
        chat_Info()
        data_input = input()
        action(data_input) 

chat_Info()
data_input = input()
action(data_input)  
    