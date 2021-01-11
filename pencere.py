# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 03:02:52 2020

@author: bayram
"""
import subprocess
import tkinter as tk
from tkinter import *
import tkinter.messagebox as tm
# _____CLIENT FONKSİYONLARI_____
global client_name, first_time, message_records

client_name = " "
first_time = True

def giris_bolumu(event = None):
    kullanıcı_bilgisi=Kullanıcı.get()
    if not Kullanıcı.get():
        bosluk=tm.askyesno(title="Hata!",
                           message="Gerekli yerleri doldurmadınız,tekrar giriş yapmak ister misiniz?")
        if bosluk == False:
            pencere.destroy()
    if(kullanıcı_bilgisi == '5'):
        olumlu=tm.showinfo('Giriş','Hoşgeldiniz')
        pencere.destroy()
        subprocess.run(["python", "client_port.py", "5"])

    if (kullanıcı_bilgisi == '4'):
        olumlu=tm.showinfo('Giriş','Hoşgeldiniz')
        pencere.destroy()
        subprocess.run(["python", "client_port.py", "4"])
        
    if(kullanıcı_bilgisi == '3'):
        olumlu=tm.showinfo('Giriş','Hoşgeldiniz')
        pencere.destroy()
        subprocess.run(["python", "client_port.py", "3"])
        
    if(kullanıcı_bilgisi == '2'):
        olumlu=tm.showinfo('Giriş','Hoşgeldiniz')
        pencere.destroy()
        subprocess.run(["python", "client_port.py", "2"])
        
    if(kullanıcı_bilgisi == '1'):
        olumlu=tm.showinfo('Giriş','Hoşgeldiniz')
        pencere.destroy()
        subprocess.run(["python", "client_port.py", "1"])
        
    if (kullanıcı_bilgisi != '5' or kullanıcı_bilgisi != '4' or kullanıcı_bilgisi != '3' or kullanıcı_bilgisi != '2' or kullanıcı_bilgisi != '1' ):
        tm.showerror('Hata','yanlış doktor numarası')
        

pencere=tk.Tk()
pencere.geometry('600x150+300+300')
pencere.title('Planlama')
Kullanıcı_Adi = Label(pencere,text='Seçilen doktorun sayısını yazınız:\n 1-(Ordu-Ünye Devlet Hastanesi Ahmet Yolvermez\n 2-(İstanbul-Maltepe Devlet Hastanesi= Orhan Sarı\n 3-(Ankara-Beypazarı Devlet Hastanesi Ali Açıkgöz\n 4-(Samsun-Samsun Devlet Hastanesi Alev Batmaz\n 5-(Sinop-Sinop Devlet Hastanesi Kadriye Solmaz').grid(row=0,column=0)
Kullanıcı = Entry(pencere)
Kullanıcı.grid(row=0,column=1)   
Giris_Button = Button(pencere,text='   Giriş    ',width=7,command=giris_bolumu).place(relx=0.65,rely=0.45)

pencere.mainloop()