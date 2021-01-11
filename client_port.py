# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 03:02:52 2020

@author: bayram
"""
import sys
import socket  # BSD Soket Arayüzüne erişim sağlar
from threading import Thread

import tkinter as tk


# _____CLIENT FONKSİYONLARI_____
global client_name, first_time, message_records

client_name = " "
first_time = True
message_records = []
def receive_msg():
    while True:
        try:
            msg = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            global client_name

            if (msg == "+shwmsg"):
                top = tk.Tk()
                msg_history = tk.Listbox(top, bg="#D27933", height=15, width=50, font=("Courier", 12, "bold"))
                for i, jmsg in enumerate(message_records):
                    if (i > 0):
                        msg_history.insert(tk.END, jmsg)
                msg_history.pack()
                top.mainloop()

            elif (msg.find("Eğer çıkmak istiyorsan") != -1):
                msg_to_print = msg.split("+")[0]
                online_users = msg.split("+")[1]

                users_listbox.insert(tk.END, "Çevrimiçi Kullanıcılar:")
                for user in online_users.split(" "):
                    users_listbox.insert(tk.END, user)

                msg_list.insert(tk.END, msg_to_print)
            elif (msg.find("sohbet odasına katıldı") != -1):
                msg_to_print = msg.split("+")[0]
                online_users = msg.split("+")[1]
                users_listbox.delete(0, tk.END)

                users_listbox.insert(tk.END, "Çevrimiçi Kullanıcılar:")
                for user in online_users.split(" "):
                    users_listbox.insert(tk.END, user)

                msg_list.insert(tk.END, msg_to_print)


            elif (msg.find("shwuserbymsg+") != -1):
                msgs = msg.split("+")[1].split(",")
                selected_client = msg.split("+")[2]

                top = tk.Tk()
                lbox = tk.Listbox(top, bg="white", height=15, width=50)
                for i in msgs:
                    i = selected_client + ": " + i
                    lbox.insert(tk.END, i)

                button = tk.Button(top, text="Okey", command=top.destroy)
                lbox.pack()
                button.pack()
                top.mainloop()

            else:
                message_records.append(msg)
                # save to the messages.txt file
                if msg != "Lütfen adınızı yazın ve girin:":
                    with open("messages.txt", "a") as output:
                        output.write(msg + '\n')

                if (msg != "+shwmsg"):
                    msg_list.insert(tk.END, msg)

        except OSError:
            pass  # Probabaly client has left the chat


def send_msg(event=None):
    global first_time, client_name
    if first_time == True:
        msg = my_msg.get()
        client_name = msg
        root.title(client_name)
        first_time = False

    msg = my_msg.get()

    if (msg != "" or msg != " "):  # mesaj boş değilse
        my_msg.set("")  # Giriş alanını temizler.

        if msg.find("$") != -1:
            msg = msg + "+" + client_name
            client_socket.send(msg.encode("utf-8"))  # mesaj gönderme

        elif msg == "{quit}":  # close client
            client_socket.close()
            root.quit()
        else:

            client_socket.send(msg.encode("utf-8"))  # mesaj gönderme

def on_closing(event=None):  # kinter uygulamasını kapatmadan önce bağlantıyı kapatın
    my_msg.set("{quit}")


# send_msg()

# TKINTER WINDOW
WIDTH = 1200
HEIGHT = 400

root = tk.Tk()
root.title("Chat Room")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

user_frame = tk.Frame(canvas, bg="#5EB619")
user_frame.place(relx=0, rely=0, relwidth=0.60, relheight=1)

result_frame = tk.Frame(canvas, bd=5, bg="white")
result_frame.place(relx=0.60, y=0, relwidth=0.40, relheight=1)

users_listbox = tk.Listbox(result_frame, bg="#07c5e6", font=("Courier", 12, "bold"))
users_listbox.place(relx=0.50, rely=0, relheight=1, relwidth=0.50)

msg_frame = tk.Frame(user_frame, bd=5, bg="#5EB619")
msg_frame.place(relx=0, rely=0, relheight=0.80, relwidth=1)

button_frame = tk.Frame(user_frame, bd=5, bg="#5EB619")
button_frame.place(relx=0, rely=0.80, relheight=0.20, relwidth=1)

my_msg = tk.StringVar()

my_msg.set("Buraya yaz...")

scrollbar = tk.Scrollbar(msg_frame)

msg_list = tk.Listbox(msg_frame, height=15, width=80, yscrollcommand=scrollbar.set, font=("Courier", 12, "bold"))
# paketleme

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)

# yazma alanı

entry_field = tk.Entry(button_frame, textvariable=my_msg, font=("Courier", 12, "bold"), bg="#e1e118")
entry_field.bind("<Return>", send_msg)
entry_field.place(relx=0, rely=0, relheight=0.5, relwidth=1)

send_button = tk.Button(button_frame, text="Gönder", command=send_msg)
send_button.place(relx=0, rely=0.5, relheight=0.5, relwidth=0.40)


root.protocol("WM_DELETE_WINDOW", on_closing)  # tkinter penceresi kapatıldığında on_closing işlevini çağırın

BUFFER_SIZE = 1024
TCP_IP = "127.0.0.1"

TCP_PORT = int(sys.argv[1])  # port numarası

SERVER_ADD = (TCP_IP, TCP_PORT)

client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)

client_socket.connect(SERVER_ADD)

receive_thread = Thread(target=receive_msg)
receive_thread.start()

root.mainloop()