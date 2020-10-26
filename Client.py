'''
we use these libraries to gain access to system functions, thread usage and other things
the librari socket enable us use the endpoint that receives data, the eof point that receives the communication in that endpoint that is in an IP and a port
'''
import socket
from pathlib import Path
import os
from prettytable import PrettyTable


    
'''this method gives the list of options to the client to execute a command'''
def pane_option():
    t = PrettyTable(['Option', 'Name Option'], )
    t.add_row([1, "Create bucket"])
    t.add_row([2, "Delete bucket"])
    t.add_row([3, "List bucket"])
    t.add_row([4, "Upload bucket"])
    t.add_row([5, "List file"])
    t.add_row([6, "Delete file"])
    t.add_row([7, "Download bucket"])
    print(t)

'''
With connection method to establish the connection with the server through the socket.

'''
def connection():

    #Creating a Socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) #Socket family type (AF_INET: IPV4), actual type of socket (SOCK_STREAM: TCP)
    client.connect((socket.gethostname(),1232))
    pane_option()
    print('Please, input a command: ')
    command=input()
    options(command,client)
    decision = input('\n Press 1 for to decision or 0 for to finish :') 

    #Sending data
    while True:
        
        while(decision=='1') :
            pane_option()
            print('Please, input a command: ')
            command=input()
            options(command,client)
            decision = input('\nPress 1 for to decision or 0 for to finish :') 
        
        break
    print("The client is over")
    client.close()   


'''With this method we identify the option or command that is entered from the client'''
def options(command,client):

    if (command=="1"):
        create_bucket(command,client)
    elif (command=="2"):
        delete_bucket(command,client)
    elif (command=="3"):
        list_bucket(command, client)
    elif (command=="4"):
        upload(command,client)
    elif (command=="5"):
        list_files(command,client)
    elif (command=="6"):
        delete_files(command,client)
    elif (command=="7"):
        download_files(command,client)
    else:
        print('Option is declined, please input a correct option: ')
        
'''this method sends the request to create a bucket, sending its name'''
def create_bucket(command, client):
    print("Input the bucket name that you want to create: ")
    bucket_name=input()
    while(bucket_name.isspace() or  len(bucket_name)==0):
        print("Bucket name is declined, please input a correct bucket name with out space or create a bucket: ")
        bucket_name=input()
    command_send=command+" "+bucket_name
    client.send(bytes(command_send,'utf-8'))
    confirmation_server(client)

'''this method sends the request to delete a bucket, sending its name'''
def delete_bucket(command, client):
    print('Please, input the bucket name for to delete: ')
    bucket_name=input()
    while(bucket_name.isspace() or  len(bucket_name)==0 or not os.path.isdir('./Buckets/'+bucket_name) ):
        print("Bucket name is declined, please input a correct bucket name with out space or create a bucket: ")
        bucket_name=input()
    command_send=command+" "+bucket_name
    client.send(bytes(command_send,'utf-8'))
    confirmation_server(client)

'''this method sends the request to list the existing buckets'''
def list_bucket(command, client):
    client.send(bytes(command,'utf-8'))
    confirmation_server(client)

'''this method sends a request to upload a file specifying the path and file name'''
def upload(command, client):
    print('Please, input the bucket name for to add files: ')
    bucket_name=input()
    while(bucket_name.isspace() or  len(bucket_name)==0 or not os.path.isdir('./Buckets/'+bucket_name) ):
        print("Bucket name is declined, please input a correct bucket name with out space or create a bucket: ")
        bucket_name=input()

    print('Input the name file with the type (Ex: .png, .txt, .pdf, etc): ')
    file_name=input()
    while(file_name.isspace() or len(file_name)==0):
        print("File name is declined, please input a correct file name with out space or create a bucket: ")
        file_name=input()
    print('Please, input the path where is the file for to upload:')
    path=input()
    while(path.isspace() or len(path)==0):
        print("Path is declined, please input a correct path with out space: ")
        path=input()
    file_origin=path+"/"+file_name
    file_exist=Path(file_origin)
    if (file_exist.exists()):
        command_send=command+" "+bucket_name+" "+file_name+" "+path
        client.send(bytes(command_send,'utf-8'))  
        file_size = os.path.getsize(path+"/"+file_name)    
        while True:
            origin_file=path+"/"+file_name
            file = open(origin_file,"rb")
            content = file.read(file_size)
                
            while content:
                # Send content
                client.send(content)
                content = file.read(file_size)
            break

        try:
            client.send(chr(1))        
        except TypeError:
            # Compatibilidad con Python 3.  
            client.send(bytes(chr(1), "utf-8"))                           
        # Cerrar conexión y archivo.
        file.close()
        print("The file is send successfully.")
        confirmation_server(client)
    else:
         print("The file doesn't exists, please create other")

'''this method sends a request to list the files in a bucket, giving the name of the bucket'''
def list_files(command, client):
    print('Please, input the bucket name for to list file: ')
    bucket_name=input()
    while(bucket_name.isspace() or  len(bucket_name)==0 or not os.path.isdir('./Buckets/'+bucket_name) ):
        print("Bucket name is declined, please input a correct bucket name with out space or create a bucket: ")
        bucket_name=input()
    command_send=command+" "+bucket_name
    client.send(bytes(command_send,'utf-8'))
    confirmation_server(client)

'''this method sends a request to delete a file from a bucket, giving the name of the bucket and the name of the file to delete'''
def delete_files(command,client):
    print('Please, input the bucket name for to delete file: ')
    bucket_name=input()
    while(bucket_name.isspace() or  len(bucket_name)==0 or not os.path.isdir('./Buckets/'+bucket_name)):
        print("Bucket name is declined, please input a correct bucket name with out space or create a bucket: ")
        bucket_name=input()
    print('Please, input the file name that you want to delete with the type (Ex: .png, .txt, .pdf, etc): ')
    file_name=input()
    while(file_name.isspace() or  len(file_name)==0 or not os.path.isfile('./Buckets/'+bucket_name+'/'+file_name)):
        print("File name is declined, please input a correct file name with out space or create a bucket: ")
        file_name=input()
    command_send=command+" "+bucket_name+" "+file_name
    client.send(bytes(command_send,'utf-8'))
    confirmation_server(client)


'''this method verifies that the file is available for download (that it exists)'''
def download_files(command,client):
    print('Input the bucket name where is the file that you want to download: ')
    bucket_name=input()
    while(bucket_name.isspace() or  len(bucket_name)==0  or not os.path.isdir('./Buckets/'+bucket_name)):
        print("Bucket name is declined, please input a correct bucket name with out space or create a bucket: ")
        bucket_name=input()
    print('Input the file name that you want to download: ')
    file_name=input()
    while(file_name.isspace() or  len(file_name)==0 or not os.path.isfile('./Buckets/'+bucket_name+'/'+file_name)):
        print("Input a correct name file: ")
        file_name=input()
    command_send=command+" "+bucket_name+" "+file_name
    client.send(bytes(command_send,'utf-8'))
    
    
    destiny_path="./Downloads/"+file_name
    file = Path(destiny_path)
    origin_path="./Buckets/"+bucket_name+"/"+file_name
    file_exist = Path(origin_path)
    if(file.exists()):
        print("The file alredy exists!")
    elif not (file_exist.exists()):
        print("The file doesn't exists!")
    else:
        download_if_not_exists(bucket_name,file_name,client,origin_path)


'''This method sends a request to download a specific file from a bucket, giving the name of the file and the bucket where it is (MUST EXIST)'''
def download_if_not_exists(bucket_name,file_name, client,origin_path):
    destiny_path="./Downloads/"+file_name
    file= open(destiny_path,"wb")
    file_size = os.path.getsize(origin_path)
    while True:
        try:
             # Recibir datos del cliente.
            data_received = client.recv(file_size)
            if data_received:
                 # Compatibilidad con Python 3.
                if isinstance(data_received, bytes):
                    eof = data_received[0] == 1
                        
                else:
                    eof = data_received == chr(1)
                    
                if not eof:
                    if os.path.isdir(destiny_path):
                        print("The file exists!")
                    else:
                        file.write(data_received)
                        print("The file is receive successfully.")
                        confirmation_server(client)                
            break
        except:
            file.close()
            break

    file.close() 


'''this method confirms and passes some messages from the server to the client'''
def confirmation_server(client):
    dataFromServer = client.recv(1024)
    print(dataFromServer.decode())



 '''Cliente main'''
if __name__ == "__main__":
    connection()
