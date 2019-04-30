import socket

client = socket.socket()
client.connect(("192.168.0.9",41000))
while True:
    msg = input(">").strip()
    if msg=='exit':
        break
    else:
        
        client.send(msg.encode())
        data = client.recv(1024)
    
        print(data)

client.close()
