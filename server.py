# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 03:02:43 2020

@author: bayram
"""

import socket
from threading import Thread


# ________SERVER FONKSİYONLARI________

# YAYIN MESAJI

def broadcast(msg, prefix=""):  # msg: yayına mesaj, prefix: gönderen kimliği belirleme  
    # tüm istemcilere mesaj yayınlayın
    for client_socket in clients:
        client_socket.send(prefix.encode("utf-8") + msg)

def send_msgto_multiple_client(msg, members):
    if (isinstance(members, list) != True):
        members = members.split(",")  # create a list

    for name_client in members:
        for client_socket, name in clients.items():
            if (name == name_client):
                client_socket.send(msg.encode("utf-8"))


# BAĞLANTILARI KABUL ET

def accept_connections():  # gelen istemcinin bağlantı talebini kabul et
    while True:  # wait connection
        client_conn, client_address = server.accept()  # bağlantı soketini ve soket adresini döndürür
        print("{0}:{1} bağlandı.".format(client_address[0], client_address[1]))

        client_conn.send("Lütfen adınızı yazın ve girin:".encode("utf-8"))  # bağlı istemciye gönder
        adresses[client_conn] = client_address  # bağlı istemci adresini adresin diktesine ekleyin
        Thread(target=handle_client,
               args=(client_conn,)).start()  # başlangıç ​​iş parçacığı ps: her bağlantı için init iş parçacığı


# istemci kullanma 

def handle_client(client):
    name = client.recv(BUFFER_SIZE).decode("utf-8")  # istemci adını al
    clients[client] = name  # istemcilerin diktesine istemci adı ekleyin.

    hello_msg = "Merhaba {0}. Çıkmak isterseniz kapat yazın".format(name) + "+"
    tmp = " "
    tmp = tmp.join(list(clients.values()))

    hello_msg = hello_msg + tmp

    client.send(hello_msg.encode("utf-8"))  # kullanıcıya merhaba mesajı gönder

    join_msg = "{0} sohbet odasına katıldı".format(name) + "+"
    tmp = " "
    tmp = tmp.join(list(clients.values()))
    join_msg = join_msg + tmp
    broadcast(join_msg.encode("utf-8"))  # mesajı tüm kullanıcılara yayınladı.
    while True:
        client_msg = client.recv(BUFFER_SIZE)  # istemcinin mesajını al
        decoded_msg = client_msg.decode("utf-8")

        if (decoded_msg == "kapat"):
            client.send(bytes("{quit}", "utf-8"))
            client.close()  # close connection

            del clients[client]  # istemciyi dikteden sil
            broadcast(bytes("{0} sohbetten ayrıldı".format(name), "utf-8"))
            break

        else:  # mesaj gönderme
            if name in messages.keys():
                messages[name] = messages[name] + "," + decoded_msg
            else:
                messages[name] = decoded_msg

            broadcast(client_msg, name + ": ")

clients = {}  # sunucuya bağlı istemciler için dict
adresses = {}  # Bağlı istemcinin adreslerini dikte
messages = {}


TCP_IP = "127.0.0.1"
TCP_PORT = 1  # sunucu bağlantı noktası numarası
BUFFER_SIZE = 1024  # sunucu giriş arabellek boyutu

server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)  # sunucu için soket oluştur
server.bind((TCP_IP, TCP_PORT))  # sunucuya soket adresini bağla

if __name__ == "__main__":
    server.listen(5)  # maksimum 5 bağlantı
    print("Bağlantı için bekleniliyor...")
    thread = Thread(target=accept_connections)
    thread.start()
    thread.join()
    server.close()