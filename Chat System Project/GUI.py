#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from chat_utils import *
import json
import pickle
from time import sleep
from PIL import ImageGrab,Image,ImageTk
import emoji
import socket
import requests
import urllib.request
import gzip
from tkinter import filedialog
import os
#from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex 
import socket
import getpass
import hashlib
from quicktranslate import get_translate_youdao
import random



# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""
        
        self.load1=Image.open('1dice.png')
        self.dice1=ImageTk.PhotoImage(self.load1)
        
        self.load2=Image.open('2dice.png')
        self.dice2=ImageTk.PhotoImage(self.load2)
        
        self.load3=Image.open('3dice.png')
        self.dice3=ImageTk.PhotoImage(self.load3)
        
        self.load4=Image.open('4dice.png')
        self.dice4=ImageTk.PhotoImage(self.load4)
        
        self.load5=Image.open('5dice.png')
        self.dice5=ImageTk.PhotoImage(self.load5)
        
        self.load6=Image.open('6dice.png')
        self.dice6=ImageTk.PhotoImage(self.load6)
        
        self.diceNumbers={
            "1":self.dice1,
            "2":self.dice2,
            "3":self.dice3,
            "4":self.dice4,
            "5":self.dice5,
            "6":self.dice6
            }
        
        self.ldm1 = Image.open('facepalm.png')
        self.memes1 = ImageTk.PhotoImage(self.ldm1)
        
        self.ldm2 = Image.open('smart.png')
        self.memes2 = ImageTk.PhotoImage(self.ldm2)
        
        self.ldm3 = Image.open('smirk.png')
        self.memes3 = ImageTk.PhotoImage(self.ldm3)
        
        self.ldm4 = Image.open('concerned.png')
        self.memes4 = ImageTk.PhotoImage(self.ldm4)
        
        self.memesdic = {
            "1":self.memes1,
            "2":self.memes2,
            "3":self.memes3,
            "4":self.memes4,
            }

    def login(self):
        self.flag = False
        self.login_name = ''
        # login window
        self.login = Toplevel()
        self.login.title("Login")
        self.login.geometry('450x300')
        self.pls = Label(self.login, 
                       text = "Please login to continue",
                       font = "Helvetica 14 bold")
        self.pls.place(x = 60, y = 65)
        
        # Label - username / password
        self.labelName = Label(self.login,
                               text = "Username: ",
                               font = "Helvetica 12")
        self.labelName.place(x = 90, y = 130)
        self.labelPwd = Label(self.login, 
                               text = "Password: ",
                               font = "Helvetica 12")
        self.labelPwd.place(x = 90, y = 170)
        
        # entry box - username / password
        self.var_usr_name = StringVar()
        self.entry_usr_name = Entry(self.login, textvariable = self.var_usr_name)
        self.entry_usr_name.place(x=180,y=130)
        self.var_usr_pwd = StringVar()
        self.entry_usr_pwd = Entry(self.login,textvariable = self.var_usr_pwd, show = '*')
        self.entry_usr_pwd.place(x=180,y=170)
        
        # button - login / registration / quit
        self.bt_login = Button(self.login, text = 'Login', command = lambda: self.usr_log_in(self.var_usr_name.get(),self.var_usr_pwd.get()))
        self.bt_login.place(x = 110, y = 230)
        self.bt_logreg = Button(self.login,text='Registration',command = lambda: self.usr_sign_up())
        self.bt_logreg.place(x = 180, y = 230)
        self.bt_logquit = Button(self.login,text='Quit',command = lambda: self.usr_sign_quit())
        self.bt_logquit.place(x = 290, y = 230)
        
        self.Window.mainloop()
    
    #登录函数
    def usr_log_in(self,var_usr_name,var_usr_pwd):
        #输入框获取用户名密码
        usr_name = var_usr_name
        usr_pwd = var_usr_pwd
        #从本地字典获取用户信息，如果没有则新建本地数据库
        try:
            with open('usr_info.pickle','rb') as usr_file:
                usrs_info = pickle.load(usr_file)
        except FileNotFoundError:
            with open('usr_info.pickle','wb') as usr_file:
                usrs_info = {'admin':'admin'}
                pickle.dump(usrs_info, usr_file)
        
        #用户名密码不能为空
        if usr_name == '' or usr_pwd == '' :
            messagebox.showerror(message = 'Username or password is empty.')
        
        #判断用户名和密码是否匹配
        if usr_name in usrs_info:
            if usr_pwd == usrs_info[usr_name]:
                messagebox.showinfo(message = 'Welcome '+usr_name+'!')
                self.flag = True
                self.login_name = usr_name
                self.gopage = Toplevel(self.login)
                self.gopage.title("CHATROOM")
                self.gopage.geometry('450x300')
                self.wel = Label(self.gopage, 
                               text = "Welcome to Our Chatroom!",
                               font = "Helvetica 14 bold")
                self.wel.place(x = 60, y = 65)
                self.go = Button(self.gopage,
                             text = "CONTINUE", 
                             font = "Helvetica 14 bold", 
                             command = lambda: self.goAhead(self.login_name))
                self.go.place(x = 80, y = 120)
            else:
                messagebox.showerror(message = 'Incorrect password.')   
        #不在数据库中弹出是否注册的框
        else:
            is_signup = messagebox.askyesno(message = 'You have not registered yet, would you like to register now?')
            if is_signup:
                self.usr_sign_up()
    
    #注册函数
    def usr_sign_up(self):
        #确认注册时的相应函数
        def signtoreg():
            #获取输入框内的内容
            nn = var_new_name.get()
            np = var_new_pwd.get()
            npf = var_new_pwd_confirm.get()
 
            #本地加载已有用户信息,如果没有则已有用户信息为空
            try:
                with open('usr_info.pickle','rb') as usr_file:
                    exist_usr_info=pickle.load(usr_file)
            except FileNotFoundError:
                exist_usr_info={}           
            
            #检查用户名存在、密码为空、密码前后不一致
            if nn in exist_usr_info:
                messagebox.showerror('Error!','Username already exists.')
            elif np == '' or nn == '':
                messagebox.showerror('Error!','Username or password is empty.')
            elif np !=npf:
                messagebox.showerror('Error!','Inconsistent passwords.')
            #注册信息没有问题则将用户名密码写入数据库
            else:
                messagebox.showinfo('Registered successfully!','Welcome!')
                self.flag = True
                self.login_name = nn
                #注册成功关闭注册框
                window_sign_up.destroy()
                exist_usr_info[nn]=np
                with open('usr_info.pickle','wb') as usr_file:
                    pickle.dump(exist_usr_info,usr_file)
                self.gopage = Toplevel(self.login)
                self.gopage.title("CHATROOM")
                self.gopage.geometry('450x300')
                self.wel = Label(self.gopage, 
                               text = "Welcome to Out Chatroom!",
                               font = "Helvetica 14 bold")
                self.wel.place(x = 60, y = 65)
                self.go = Button(self.gopage,
                             text = "CONTINUE", 
                             font = "Helvetica 14 bold", 
                             command = lambda: self.goAhead(self.login_name))
                self.go.place(x = 80, y = 120)
                
        #新建注册界面
        window_sign_up=Toplevel(self.login)
        window_sign_up.geometry('350x200')
        window_sign_up.title('Registration')
    
        #用户名变量及标签、输入框
        var_new_name=StringVar()
        new_name = Label(window_sign_up, text = 'Username：').place(x=10,y=10)
        enter_new_name = Entry(window_sign_up, textvariable = var_new_name).place(x=150,y=10)
        #密码变量及标签、输入框
        var_new_pwd=StringVar()
        new_pwd = Label(window_sign_up, text = 'Password：').place(x=10,y=50)
        enter_new_pwd = Entry(window_sign_up, textvariable = var_new_pwd, show = '*').place(x=150,y=50)    
        #重复密码变量及标签、输入框
        var_new_pwd_confirm=StringVar()
        new_pwd_confirm = Label(window_sign_up, text = 'Confirm Password：').place(x=10,y=90)
        enter_new_pwd_confirm = Entry(window_sign_up, textvariable = var_new_pwd_confirm, show = '*').place(x=150,y=90)    
    
        #确认注册按钮及位置
        bt_confirm_sign_up = Button(window_sign_up, text='Complete Registration', command = signtoreg)
        bt_confirm_sign_up.place(x = 150, y = 130)
        
        window_sign_up.mainloop()
    
    #退出的函数
    def usr_sign_quit(self):
        self.login.destroy()
    
    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action":"login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state = NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")   
                self.textCons.insert(END, menu +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)
                # while True:
                #     self.proc()
        # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()
  
    # The main layout of the chat
    def layout(self,name):
       
        
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#17202A")
        self.labelHead = Label(self.Window,
                             bg = "#17202A", 
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
          
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
          
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
        

        self.textCons = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14", 
                             padx = 5,
                             pady = 5)
         
        self.textCons.place(relheight = 0.662,
                            relwidth = 1, 
                            rely = 0.08)
        
        self.load=Image.open('dice2.png')
        self.render=ImageTk.PhotoImage(self.load)
       # self.img=Label(self.Window,image=self.render)
       # self.img.image=self.render
        #self.img.place(x=50,y=50,width=100,height=100)
          
          
        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
          
        self.labelBottom.place(relwidth = 1,
                               rely = 0.745)
         
        
        # emojis
        self.e1Button = Button(self.labelBottom,text=emoji.emojize(':thumbs_up:',use_aliases=True),command= lambda: self.sendEmoji(':thumbs_up:'))
        self.e1Button.place(x=5,y=77,height=30,width=30)
        
        self.e2Button = Button(self.labelBottom,text=emoji.emojize(':heart:',use_aliases=True),command= lambda: self.sendEmoji(':heart:'))
        self.e2Button.place(x=40,y=77,height=30,width=30)
        
        self.e3Button = Button(self.labelBottom,text=emoji.emojize(':fire:',use_aliases=True),command= lambda: self.sendEmoji(':fire:'))
        self.e3Button.place(x=75,y=77,height=30,width=30)
        
        self.e4Button = Button(self.labelBottom,text=emoji.emojize(':satisfied:',use_aliases=True),command= lambda: self.sendEmoji(':satisfied:'))
        self.e4Button.place(x=110,y=77,height=30,width=30)
        
        self.e5Button = Button(self.labelBottom,text=emoji.emojize(':yum:',use_aliases=True),command= lambda: self.sendEmoji(':yum:'))
        self.e5Button.place(x=145,y=77,height=30,width=30)
        
        self.e6Button = Button(self.labelBottom,text=emoji.emojize(':eyes:',use_aliases=True),command= lambda: self.sendEmoji(':eyes:'))
        self.e6Button.place(x=180,y=77,height=30,width=30)
        
        self.e7Button = Button(self.labelBottom,text=emoji.emojize(':tongue:',use_aliases=True),command= lambda: self.sendEmoji(':tongue:'))
        self.e7Button.place(x=215,y=77,height=30,width=30)
        
        self.e8Button = Button(self.labelBottom,text=emoji.emojize(':droplet:',use_aliases=True),command= lambda: self.sendEmoji(':droplet:'))
        self.e8Button.place(x=250,y=77,height=30,width=30)
        
        self.e9Button = Button(self.labelBottom,text=emoji.emojize(':heart_eyes:',use_aliases=True),command= lambda: self.sendEmoji(':heart_eyes:'))
        self.e9Button.place(x=285,y=77,height=30,width=30)
        
        self.e10Button = Button(self.labelBottom,text=emoji.emojize(':tada:',use_aliases=True),command= lambda: self.sendEmoji(':tada:'))
        self.e10Button.place(x=320,y=77,height=30,width=30)
        
        self.e11Button = Button(self.labelBottom,text=emoji.emojize(':beers:',use_aliases=True),command= lambda: self.sendEmoji(':beers:'))
        self.e11Button.place(x=355,y=77,height=30,width=30)
        
        self.e12Button = Button(self.labelBottom,text=emoji.emojize(':muscle:',use_aliases=True),command= lambda: self.sendEmoji(':muscle:'))
        self.e12Button.place(x=390,y=77,height=30,width=30)
        
        self.e13Button = Button(self.labelBottom,text=emoji.emojize(':fearful:',use_aliases=True),command= lambda: self.sendEmoji(':fearful:'))
        self.e13Button.place(x=5,y=107,height=30,width=30)
        
        self.e14Button = Button(self.labelBottom,text=emoji.emojize(':cry:',use_aliases=True),command= lambda: self.sendEmoji(':cry:'))
        self.e14Button.place(x=40,y=107,height=30,width=30)
        
        self.e15Button = Button(self.labelBottom,text=emoji.emojize(':scream:',use_aliases=True),command= lambda: self.sendEmoji(':scream:'))
        self.e15Button.place(x=75,y=107,height=30,width=30)
        
        self.e16Button = Button(self.labelBottom,text=emoji.emojize(':rage:',use_aliases=True),command= lambda: self.sendEmoji(':rage:'))
        self.e16Button.place(x=110,y=107,height=30,width=30)
        
        self.e17Button = Button(self.labelBottom,text=emoji.emojize(':shit:',use_aliases=True),command= lambda: self.sendEmoji(':shit:'))
        self.e17Button.place(x=145,y=107,height=30,width=30)
        
        self.e18Button = Button(self.labelBottom,text=emoji.emojize(':nail_care:',use_aliases=True),command= lambda: self.sendEmoji(':nail_care:'))
        self.e18Button.place(x=180,y=107,height=30,width=30)
        
        self.e19Button = Button(self.labelBottom,text=emoji.emojize(':scream_cat:',use_aliases=True),command= lambda: self.sendEmoji(':scream_cat:'))
        self.e19Button.place(x=215,y=107,height=30,width=30)
        
        self.e20Button = Button(self.labelBottom,text=emoji.emojize(':pig_nose:',use_aliases=True),command= lambda: self.sendEmoji(':pig_nose:'))
        self.e20Button.place(x=250,y=107,height=30,width=30)
        
        self.e21Button = Button(self.labelBottom,text=emoji.emojize(':smoking:',use_aliases=True),command= lambda: self.sendEmoji(':smoking:'))
        self.e21Button.place(x=285,y=107,height=30,width=30)
        
        self.e22Button = Button(self.labelBottom,text=emoji.emojize(':triangular_flag_on_post:',use_aliases=True),command= lambda: self.sendEmoji(':triangular_flag_on_post:'))
        self.e22Button.place(x=320,y=107,height=30,width=30)
        
        self.e23Button = Button(self.labelBottom,text=emoji.emojize(':sos:',use_aliases=True),command= lambda: self.sendEmoji(':sos:'))
        self.e23Button.place(x=355,y=107,height=30,width=30)
        
        self.e24Button = Button(self.labelBottom,text=emoji.emojize(':bulb:',use_aliases=True),command= lambda: self.sendEmoji(':bulb:'))
        self.e24Button.place(x=390,y=107,height=30,width=30)
        
       
        # entry message
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")

        self.entryMsg.place(relwidth = 0.8,
                            height = 32,
                            y = 43,
                            relx = 0.005)
          
        self.entryMsg.focus()
        
        # send button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
          
        self.buttonMsg.place(relx = 0.77995,
                             y = 43,
                             height = 32, 
                             relwidth = 0.22)
          
        self.textCons.config(cursor = "arrow")
        
        # screenshot button
        self.buttonCap = Button(self.Window,
                                text = "Screenshot",
                                font = "Helvetica 10 bold", 
                                bg = "#ABB2B9",
                                command = lambda : self.capButton())
        self.buttonCap.place(x = 0, y = 430)
        
        # location button
        self.buttonLoc = Button(self.Window,
                                text = "Location",
                                font = "Helvetica 10 bold", 
                                bg = "#ABB2B9",
                                command = lambda : self.locButton())
        self.buttonLoc.place(x = 93, y = 430)
        
        # weather button
        self.buttonWea = Button(self.Window,
                                text = "Weather",
                                font = "Helvetica 10 bold", 
                                bg = "#ABB2B9",
                                command = lambda : self.weaButton())
        self.buttonWea.place(x = 173, y = 430)
        
        # translation button
        self.buttonTrans = Button(self.Window,
                                text = "Translation",
                                font = "Helvetica 10 bold", 
                                bg = "#ABB2B9",
                                command = lambda : self.transButton())
        self.buttonTrans.place(x = 250, y = 430)
        
        # memes button
        self.buttonMemes = Button(self.Window,
                                text = "Memes",
                                font = "Helvetica 10 bold", 
                                bg = "#ABB2B9",
                                command = lambda : self.memesButton())
        self.buttonMemes.place(x = 340, y = 430)
        
        # time button
        self.buttonTime = Button(self.Window,
                                text = "Time",
                                font = "Helvetica 10 bold", 
                                bg = "#ABB2B9",
                                command = lambda : self.timeButton())
        self.buttonTime.place(x = 0, y = 407)
        
        # list users button
        self.buttonUser = Button(self.Window,
                                text = "List Users&Groups",
                                font = "Helvetica 10 bold", 
                                bg = "#ABB2B9",
                                command = lambda : self.listUsers())
        self.buttonUser.place(x = 61, y = 407)
        
        # poem button
        self.buttonPoem =Button(self.Window,
                                text = "Poem",
                                font = "Helvetica 10 bold", 
                                bg = "#ABB2B9",
                                command = lambda : self.poemButton())
        self.buttonPoem.place(x = 192, y = 407)
        
        # connect button
        self.buttonCon =Button(self.Window,
                                text = "Connect",
                                font = "Helvetica 10 bold", 
                                bg = "#ABB2B9",
                                command = lambda : self.chatButton())
        self.buttonCon.place(x = 257, y = 407)
        
        # search button
        self.buttonSrh =Button(self.Window,
                                text = "Search",
                                font = "Helvetica 10 bold", 
                                bg = "#ABB2B9",
                                command = lambda : self.searchButton())
        self.buttonSrh.place(x = 335, y = 407)
        
        # search button
        self.buttonLve =Button(self.Window,
                                text = "Leave",
                                font = "Helvetica 10 bold", 
                                bg = "#ABB2B9",
                                command = lambda : self.leaveButton())
        self.buttonLve.place(x = 405, y = 407)
        
        
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
          
        # place the scroll bar 
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
          
        scrollbar.config(command = self.textCons.yview)
          
        self.textCons.config(state = DISABLED)
        
        ### hand game ###
        self.handgameButton = Button(self.labelBottom, text='👊'
                                     ,command= lambda: self.handgame())
        self.handgameButton.place(x=430,y=77,height=30,width=32)
        
        ### dice game ###
        
        self.dicegameButton = Button(self.labelBottom, text='🎲'
                                     ,command= lambda: self.dicegame())
        self.dicegameButton.place(x=430,y=107,height=30,width=32)
        
    '''  
    def dicegame(self):
        self.diceBox=Frame(self.Window,bg='pink')
        self.diceBox.place(width=250,height=150,x=150,y=200)
        self.diceEndButton=Button(self.diceBox,text='QUIT',command=lambda: self.endDice())
        self.diceEndButton.place(x=200,y=0,width=50,height=35)
        
    def endDice(self):
        self.diceBox.destroy()
    '''
    
    def dicegame(self):
        n=random.randint(1, 6)
        
        self.my_msg = 'dice'+str(n)
      
    
    def handgame(self):
        self.gameBox = Frame(self.Window,bg='pink')
        self.gameBox.place(width=250,height=300,x=150,y=100)
        self.startLabel = Label(self.gameBox, text = 'Game start!')
        self.startLabel.place(x = 70, y = 10, width = 100, height = 30)
        self.userLabel = Label(self.gameBox, text = ' User:')
        self.userLabel.place(x = 5, y = 40, width = 50, height = 30)
        self.rockButton = Button(self.gameBox, text='rock',command=self.ButtonRock).place(x=5,y=80)
        self.paperButton = Button(self.gameBox, text='paper',command=self.ButtonPaper).place(x=65,y=80)
        self.scissorsButton = Button(self.gameBox, text='scissors',command=self.ButtonScissors).place(x=130,y=80)
        #self.cleargameButton = Button(self.gameBox, text='clear',command=self.ButtonScissors).place(x=180,y=160)
        
    def ButtonRock(self):
        self.userchoiceLabel = Label(self.gameBox, text='rock').place(x=55, y=40, width = 60, height = 30)
        self.userchoice = 1
        
        self.computerchoice = random.randint(1, 3)
        
        if self.computerchoice == 3:
            self.result = 'Congrats! You win :)'
        elif self.computerchoice == 1:
            self.result = 'Tie. Please try again.'
        else:
            self.result = 'Sorry. You lose :('
        
        self.compLabel = Label(self.gameBox, text = ' Computer:')
        self.compLabel.place(x = 5, y = 120, width = 80, height = 30)
        
        if self.computerchoice == 1:
            self.comp_choice = 'rock'
        elif self.computerchoice == 2:
            self.comp_choice = 'paper'
        else:
            self.comp_choice = 'scissors'
            
        self.compchoiceLabel = Label(self.gameBox, text=self.comp_choice).place(x=85, y=120, width = 60, height = 30)
        
        self.resultText = Label(self.gameBox, text=self.result).place(x=5, y=160, width=150, height = 30)
        
        self.endButton = Button(self.gameBox, text = 'End Game', command = self.endHandgame).place(x=70, y=250)
        
    
    def ButtonPaper(self):
        self.userchoiceLabel = Label(self.gameBox, text='paper').place(x=55, y=40, width = 60, height = 30)
        self.userchoice = 2
        
        self.computerchoice = random.randint(1, 3)
        
        if self.computerchoice == 1:
            self.result = 'Congrats! You win :)'
        elif self.computerchoice == 2:
            self.result = 'Tie. Please try again.'
        else:
            self.result = 'Sorry. You lose :('
        
        self.compLabel = Label(self.gameBox, text = ' Computer:')
        self.compLabel.place(x = 5, y = 120, width = 80, height = 30)
        
        if self.computerchoice == 1:
            self.comp_choice = 'rock'
        elif self.computerchoice == 2:
            self.comp_choice = 'paper'
        else:
            self.comp_choice = 'scissors'
            
        self.compchoiceLabel = Label(self.gameBox, text=self.comp_choice).place(x=85, y=120, width = 60, height = 30)
        
        self.resultText = Label(self.gameBox, text=self.result).place(x=5, y=160, width = 150, height = 30)
        
        self.endButton = Button(self.gameBox, text = 'End Game', command = self.endHandgame).place(x=70, y=250)
        
        
    def ButtonScissors(self):
        self.userchoiceLabel = Label(self.gameBox, text='scissors').place(x=55, y=40, width = 60, height = 30)
        self.userchoice = 3
        
        self.computerchoice = random.randint(1, 3)
        
        if self.computerchoice == 2:
            self.result = 'Congrats! You win :)'
        elif self.computerchoice == 3:
            self.result = 'Tie. Please try again.'
        else:
            self.result = 'Sorry. You lose :('
        
        self.compLabel = Label(self.gameBox, text = ' Computer:')
        self.compLabel.place(x = 5, y = 120, width = 80, height = 30)
        
        if self.computerchoice == 1:
            self.comp_choice = 'rock'
        elif self.computerchoice == 2:
            self.comp_choice = 'paper'
        else:
            self.comp_choice = 'scissors'
            
        self.compchoiceLabel = Label(self.gameBox, text=self.comp_choice).place(x=85, y=120, width = 60, height = 30)
        
        self.resultText = Label(self.gameBox, text=self.result).place(x=5, y=160, width = 150, height = 30)
        
        self.endButton = Button(self.gameBox, text = 'End Game', command = self.endHandgame).place(x=70, y=250)
    
    #def cleargameButton(self):
        #self.resultText = Label(self.gameBox, text='               ').place(x=5, y=160, width = 150, height = 20)
        
    def endHandgame(self):
        self.gameBox.destroy()
    
    # memes function
    def memesButton(self):
        self.memesBox = Frame(self.Window,bg='pink')
        self.memesBox.place(width=200,height=260,x=150,y=140)
        
        self.me1=Button(self.memesBox,text='Memes 1',command=self.Meme_1, image=self.memes1)
        self.me1.place(x=10,y=40)
        
        self.me2=Button(self.memesBox,text='Memes 2',command=self.Meme_2, image=self.memes2)
        self.me2.place(x=110,y=40)
        
        self.me3=Button(self.memesBox,text='Memes 3',command=self.Meme_3, image=self.memes3)
        self.me3.place(x=10,y=150)
        
        self.me4=Button(self.memesBox,text='Memes 4',command=self.Meme_4, image=self.memes4)
        self.me4.place(x=110,y=150)
        
        self.levme=Button(self.memesBox,text='OK',command=self.memesDone)
        self.levme.place(x=0,y=0,width=30,height=30)
    
    def Meme_1(self):
        self.my_msg = 'MEMES 1'
    
    def Meme_2(self):
        self.my_msg = 'MEMES 2'
        
    def Meme_3(self):
        self.my_msg = 'MEMES 3'
        
    def Meme_4(self):
        self.my_msg = 'MEMES 4'
    
    def memesDone(self):
        self.memesBox.destroy()
    
    # translation function
    def transButton(self):
        self.transpage = Toplevel(self.Window)
        self.transpage.title('Translation')
        self.transpage.geometry('800x600')
        
        self.infolabel = Label(self.transpage, text = 'This is a Chinese-English translation tool.')
        self.infolabel.place(x = 50, y = 20)
        
        self.enterlabel = Label(self.transpage,text = 'Please enter the content to be translated to English:')
        self.enterlabel.place(x = 50, y = 40)
        
        self.entryTrans = Entry(self.transpage,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14")
        self.entryTrans.place(x = 50, y = 100, width = 700, height = 200)
        
        
        self.clicktransButton =Button(self.transpage,
                                text = "Click to translate",
                                font = "Helvetica 10 bold", 
                                bg = "#ABB2B9",
                                command = lambda : self.translator(self.entryTrans.get()))
        self.clicktransButton.place(x = 60, y = 320)
        
        self.clearButton =Button(self.transpage,
                                text = "Clear",
                                font = "Helvetica 10 bold", 
                                bg = "#ABB2B9",
                                command = self.clear)
        self.clearButton.place(x = 200, y = 320)
        
        self.lvetransButton =Button(self.transpage,
                                text = "Leave",
                                font = "Helvetica 10 bold", 
                                bg = "#ABB2B9",
                                command = self.lvetrans)
        self.lvetransButton.place(x = 280, y = 320)
        
        self.transpage.mainloop()
    
    def lvetrans(self):
        self.transpage.destroy()
        
    def clear(self):             #清空文本框
        self.entryTrans.delete(0,END)
        self.textTrans.delete(1.0,END)
            
    def is_cn(self,uchar):
        #判断一个unicode是否是汉字
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            return True
        else:
            return False

    def filterchar(self,char):            #过滤字母
        word=filter(str.isalpha, char)
        word=''.join(list(word))
        return word

    def translator(self,content):             #段落翻译
        test_url = 'http://youdao.com'
        try:
            requests.get(test_url,timeout=2)
        except:
            messagebox.showerror('Error')
        if self.is_cn(content):
            sep = '。'
            resep = '.'
        else:
            sep = '.'
            resep = '。'
        contents = content.split('\n')            #段落分割
        strs = ""
        for paragraph in contents:
            if paragraph:
                sentences = paragraph.split(sep)      #句子
                for sentence in sentences:
                    if sentence:
                        res = get_translate_youdao(sentence)     #有道翻译
                        if res == 'wrong!':
                            res = get_translate_google(sentence)   #有道不行就用谷歌翻译
                        strs += res+resep                  
            strs += '\n'
        self.textTrans = Text(self.transpage,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14")
        self.textTrans.place(x = 50, y = 360, width = 700, height = 200)

        self.textTrans.insert(END,strs) #文本框填入翻译结果
    
    # location button
    def locButton(self):
        self.myname = socket.gethostname()
        self.myip = socket.gethostbyname(self.myname)
        #self.myip = '101.231.120.135'
        url = 'http://ip-api.com/json/'   #外国网站
        url = url + format(self.myip)
        response2 = requests.get(url)
        strpp={}                  #定义一个字典strpp   
        strpp=response2.json()    #把英文网站json接口返回值传给字典strpp
        locmsg = ''
        locmsg += "****************************************\n"
        locmsg += "Your IP: %s "%(strpp.get('query')) + '\n'
        locmsg += "Country: %s"%(strpp.get('country')) + '\n'
        locmsg += "City: %s"%(strpp.get('city')) + '\n'
        locmsg += "Longitude: %s"%(strpp.get('lon')) + '\n'
        locmsg += "Latitude: %s"%(strpp.get('lat')) + '\n'
        locmsg += "Data Source: <www.ip-api.com>" + '\n'
        locmsg += "****************************************"
        
        self.locBox = Frame(self.Window,bg='pink')
        self.locBox.place(width=200,height=200,x=200,y=200)
        self.location = Label(self.locBox,text=locmsg,font = "Helvetica 10 bold")
        self.location.place(width = 200,
                            height = 160,x=0,
                            y =40)
        self.recloc=Button(self.locBox,text='OK',command=self.locationDone)
        self.recloc.place(x=0,y=0,width=30,height=30)
        
    def locationDone(self):
        self.locBox.destroy()
    
    # weather function
    def weaButton(self):
        self.weaBox = Frame(self.Window,bg='pink')
        self.weaBox.place(width=200,height=200,x=150,y=200)
        self.cityBox = Entry(self.weaBox,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
        self.cityBox.place(width = 200,
                            height = 35,x=0,
                            y =30)
        self.recwea=Button(self.weaBox,text='Get',command=self.weatherFind)
        self.recwea.place(x=0,y=0,width=35,height=30)
        self.levwea=Button(self.weaBox,text='OK',command=self.weatherDone)
        self.levwea.place(x=35,y=0,width=30,height=30)
        
    def weatherFind(self):
        city_name = self.cityBox.get()
        trans_url = 'http://youdao.com'
        requests.get(trans_url,timeout=2)
        res = get_translate_youdao(city_name)
        url1 = 'http://wthrcdn.etouch.cn/weather_mini?city='+urllib.parse.quote(res)
        weather_data = urllib.request.urlopen(url1).read()
        #读取网页数据
        weather_data = gzip.decompress(weather_data).decode('utf-8')
        #解压网页数据
        weather_dict = json.loads(weather_data)
        #将json数据转换为dict数据
        forecast = weather_dict.get('data').get('forecast')#获取数据块
        self.info = ''
        self.info += forecast[0].get('date') + '\n' #日期
        self.info += forecast[0].get('high') + '\n' #最高温
        self.info += forecast[0].get('low') + '\n' #最低温
        self.info += forecast[0].get('type') #,'天气'
        self.weather = Label(self.weaBox,text=self.info,font = "Helvetica 10 bold")
        self.weather.place(width = 200,
                            height = 120,x=0,
                            y =80)
        
    def weatherDone(self):
        self.weaBox.destroy()    
    
    # time function
    def timeButton(self):
        self.my_msg = 'time'
    
    # list users function
    def listUsers(self):
        self.my_msg = 'who'
    
    # leave function
    def leaveButton(self):
        self.my_msg = 'q'
        self.Window.destroy()
    
    # search function
    def searchButton(self):
        self.logBox = Frame(self.Window,bg='pink')
        self.logBox.place(width=100,height=100,x=300,y=300)
        self.searchBox = Entry(self.logBox,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
        self.searchBox.place(width = 50,
                            height = 35,x=0,
                            y =60)
        self.findChat=Button(self.logBox,text='Find',command=self.searchDone)
        self.findChat.place(x=0,y=0,width=40,height=30)
        self.levsea=Button(self.logBox,text='OK',command=self.directsearchDone)
        self.levsea.place(x=40,y=0,width=30,height=30)
        
    def directsearchDone(self):
        self.logBox.destroy()
        
    def searchDone(self):
        findWord = self.searchBox.get()
        self.my_msg = '? '+ findWord
        self.logBox.destroy()
    
    # chat function
    def chatButton(self):
        self.peerMatch = Frame(self.Window,bg='pink')
        self.peerMatch.place(width=100,height=100,x=250,y=300)
        
        self.peerName = Entry(self.peerMatch,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
        self.peerName.place(width = 90,
                            height = 35,x=0,
                            y =60)
        self.c=Button(self.peerMatch,text='Connect',command=self.connectionDone)
        self.c.place(x=0,y=0,width=65,height=30)
        self.levc=Button(self.peerMatch,text='OK',command=self.directchatDone)
        self.levc.place(x=65,y=0,width=30,height=30)
       
    def directchatDone(self):
        self.peerMatch.destroy()
        
    def connectionDone(self):
        pname = self.peerName.get()
        self.my_msg = 'c' + pname
        self.peerMatch.destroy()
    
    # poem function
    def poemButton(self):
        self.box = Frame(self.Window, bg='pink')
        self.box.place(width=100,height=100,x=200,y=300)
        self.poemBox = Entry(self.box,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
        self.poemBox.place(width = 50,
                            height = 35,x=0,
                            y =60)
        self.b=Button(self.box,text='Find',command=self.nobox)
        self.b.place(x=0,y=0,width=40,height=30)
        self.levp=Button(self.box,text='OK',command=self.directpoemDone)
        self.levp.place(x=40,y=0,width=30,height=30)
    
    def directpoemDone(self):
        self.box.destroy()    
    
    def nobox(self):
        pn = self.poemBox.get()
        if int(pn)>0 and int(pn)<30:
            self.my_msg = 'p' + pn
        self.box.destroy()

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)        

    # screenshot function
    def capButton(self):
        # 最小化主窗口
        self.Window.state('icon')
        sleep(0.2)
        filename = 'screenshot.png'
        # grab()方法默认对全屏幕进行截图
        im = ImageGrab.grab()
        im.save(filename)
        im.close()
        # 截图结束恢复主窗口
        self.Window.state('normal')
    
    # emoji function
    def sendEmoji(self,e):
        ptext=self.entryMsg.get()
        self.entryMsg.delete(0, END)
        newtext=ptext+ emoji.emojize(e,use_aliases=True)       
        self.entryMsg.insert(END,newtext)
        
    

    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            # print(self.msg)
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg = ""
                self.system_msg += self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state = NORMAL)
                
                self.textCons.insert(END, self.system_msg +"\n") 
                
                if '🎲' in self.system_msg:
                    dice_index = self.system_msg[-2]
                    self.textCons.image_create(END, image=self.diceNumbers[dice_index])
                    
                    self.textCons.insert(END,"\n") 
                     
                     #self.textCons.insert(END,"!*!*!*!*!*!*!*!*!*!*!*!*\n") 
                     #self.textCons.image_create(END, image=self.render)
                    
                if 'MEMES' in self.system_msg:
                    memes_index = self.system_msg[-2]
                    self.textCons.image_create(END, image=self.memesdic[memes_index])
                    
                    self.textCons.insert(END,"\n")
                    
                
                
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)

    def run(self):
        self.login()

# create a GUI class object
if __name__ == "__main__": 
    g = GUI()