'''
we use these libraries to gain access to system functions, thread usage and other things
the librari socket enable us use the endpoint that receives data, the eof point that receives the communication in that endpoint that is in an IP and a port
'''
import socket
import os
import shutil
import pathlib
from os import remove
from pathlib import Path
from _thread import *
import threading 

lock = threading.Lock() 

'''
With connection method to establish the connection with the client through the socket, we use the priority queues for the clients which will be managed by means of threads and also we link the IP and ports tuple.

'''
def connection():
   
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
    print("Socket is create now...")

    client=socket.socket()

    server.bind((socket.gethostname(),1232))  

    server.listen(5) 
    print("Listening...")
   
    while True:
        client, address = server.accept()  
        lock.acquire()
        print('Connected to :', address[0], ':', address[1])
        start_new_thread(threadeds_client, (client,)) 

'''

With threadeds_client  receive the commands we send from the client to carry out the requests that the client requests, which are encapsulated in arrangements and each position of that arrangement corresponds to a piece of information.
'''
def threadeds_client(client):
    while True: 
       
        data = client.recv(1024) 
        if not data: 
            print("The server connection is over")  
            
            lock.release() 
            break
      
  
    
        data_received= (data.decode("latin-1")).split(" ")
       

        if (data_received[0]=="1"):
            name_bucket=data_received[1]
            create_bucket(name_bucket,client)

        elif (data_received[0]=="2"):
            name_bucket=data_received[1]
            if not os.path.isdir('./Buckets/'+name_bucket):
                client.send("The bucket doesn't exists!".encode())
            else:
                delete_bucket(name_bucket,client)
            
        elif(data_received[0]=="3"):             
            list_buckets(client)

        elif(data_received[0]=="4"):
            name_bucket=data_received[1] 
            name_file=data_received[2] 
            path_origin=data_received[3]
            path_destiny="./Buckets/"+name_bucket+"/"+name_file   
            file = Path(path_destiny)
            file_origin=path_origin+"/"+name_file
            if(file.exists()):
                    print("The file is exists!")
                    client.send("The file is exists!".encode())
            else:
                file_size = os.path.getsize(file_origin)
                file= open(path_destiny,"wb")
                upload_files(client,file,file_size)

        elif(data_received[0]=="5"):
            name_bucket=data_received[1]
            list_files(client,name_bucket)

        elif(data_received[0]=="6"):
            name_bucket=data_received[1]
            name_file=data_received[2]
            path="./Buckets/"+name_bucket+"/"+name_file
            delete_files(client,path)

        elif (data_received[0]=="7"):
            if not os.path.isdir('./Downloads'):
                os.mkdir("./Downloads")
            name_bucket=data_received[1]
            name_file=data_received[2]
            path="./Downloads/"+name_file
            file = Path(path)
            if(file.exists()):
                print("The file is exists!")
            else:
                download_files(name_bucket,name_file,client)

    client.send(data) 
  
    
  
'''
With create_bucket, the buckets are created with the names that the client supplies, also the base folder (Buckets) is created for storing them (each bucket is unique)
'''  
def create_bucket(name_bucket,client):
    if not os.path.isdir('./Buckets'):
        os.mkdir("./Buckets")

    path="./Buckets/"+name_bucket

    try:
        os.mkdir(path)
    except OSError:
        print("The name of this directory already exists, choose another!")
    else:
        print("The directory is create successfully.")
    client.send("The directory is create successfully.".encode())


'''
With this method, the buckets corresponding to the name that the client supplies are eliminated, also if it does not exist in the Buckets folder, the error shows them, also delete its content (delete in tree or waterfall).
'''
def delete_bucket(name_bucket,client):
    path="./Buckets/"+name_bucket
    try:
        shutil.rmtree(path) 
    except OSError:
        print("The name of this directory already exists, choose another")
        client.send("The bucket doesn't exists, choose another!".encode())
    else:
        print("The directory has been delete successfully.")
        client.send("The bucket has been delete!".encode())

'''
with this method we list the contents of the Bucke folder.
'''
def list_buckets(client):
    path="./Buckets"
    list_content=""
    content = os.listdir(path)
    for i,j in enumerate(content):
        list_content=list_content + str(i+1) +"->"+str(j)+"\n" 
        print (i+1,j)
    client.send(list_content.encode())
    print("The buckets is list successfully!") 
   
'''
With this method we can, from a name and a path that the client's server receives, upload any file that is found on the computer to the bucket specified in the client's request.
'''
def upload_files(client,file,file_size):
    
    while True:
        try:
           
            data_received = client.recv(file_size)
            if data_received:
            
                if isinstance(data_received, bytes): 
                    
                    eof = data_received[0] == 1
                        
                else:
                    eof = data_received == chr(1) 

                if not eof:
                    file.write(data_received)
                    print("The file is receive successfully.")
                    client.send("The file is receive successfully!".encode())
                break

        except:

            print("read error.")
            file.close()
            break

    file.close() 
'''
With this method received a bucket can list its content
'''
def list_files(client,name_bucket):
    list_content=""
    path="./Buckets/"+name_bucket
    content = os.listdir(path)
    for i,j in enumerate(content):
        list_content="\n" + list_content + str(i+1) +"->"+str(j) 
        print (i+1,j)
    client.send(list_content.encode())
    print("The file is send succesfully!")
    


'''
with this method received the name of a bucket and the name of a file that exists in it from the client we can delete the file
'''
def delete_files(client,path):
    file = Path(path)
    if not (file.exists()):
        print("The file doesn't exists!")
        client.send("The file doesn't exists!".encode())
    else:
        remove(path)
        print("The file has been deleted successfully.") 
        client.send("The file has been deleted from bucket".encode())

'''
With this method given a specific bucket and the name of a file that is in it, we can download the file in a download folder that is created automatically
'''
def download_files(name_bucket,name_file,client):
    dir="./Buckets/"+name_bucket+"/"+name_file
    file_size = os.path.getsize(dir)
    
    while True:
            
        file = open(dir,"rb")
        content = file.read(file_size)
            
        while content:
       
            client.send(content)
            content = file.read(file_size)
            print("The file is send succesfully!")
            client.send("The file is receive successfully.".encode())
        break

    try:
        client.send(chr(1))
        
    except TypeError:
        
        client.send(bytes(chr(1), "utf-8"))                
                
    file.close()
    
'''Server main '''
if __name__ == "__main__":
    connection()

