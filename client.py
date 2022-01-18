from concurrent.futures import thread
from http import server
from msilib.schema import SelfReg
import socket
import threading
from tkinter import *
import tkinter
from tkinter import simpledialog

class Chat:
  def __init__(self):

      #Conexão local host
      HOST = '127.0.0.1'

      #Porta para conexão
      PORT = 55556

      #Criando conexão
      self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.client.connect((HOST, PORT))

      #Desenhando tela de login
      login = Tk()
      login.withdraw()

      self.window = False
      self.active = True

      #Telas para digitar nome e servidor
      self.name = simpledialog.askstring('Nome', 'Digite seu nome:', parent=login)
      self.server = simpledialog.askstring('Server', 'Digite nome do servidor:', parent=login)

      thread = threading.Thread(target=self.connect)
      thread.start()

      #Chamada da função Janela
      self.windowChat()

  def windowChat(self):
    self.root = Tk()
    
    #Tamanho da tela de chat
    self.root.geometry("800x800")
    
    #Título da janela de chat
    self.root.title('{}'.format(server))

    #Caixa de mensagem
    self.textBox = Text(self.root)
    self.textBox.place(relx=0.05, rely=0.01, width=700, height=600)
    
    #Caixa para enviar mensagem
    self.sendMessage = Entry(self.root)
    self.sendMessage.place(relx=0.05, rely=0.8, width=500, height=20)
    
    #Botão enviar
    self.sendButton = Button(self.root, text='ENVIAR', command=self.sendMsgServer)
    self.sendButton.place(relx=0.7, rely=0.8, width=100, height=20)
    self.root.protocol("WM_DELETE_WINDOW", self.close)

    #Janela em loop para ficar aberta
    self.root.mainloop()

  def sendMsgServer(self):
    message = self.sendMessage.get()
    self.client.send(message.encode()) 
  
  def close(self):
    self.root.destroy()
    self.client.close()

  def connect(self):
    while True:
      receiver = self.client.recv(1024)
      if receiver == b'DIGITE NOME DO SERVER':
        self.client.send(self.server.encode())
        self.client.send(self.name.encode())
      else:
        try:
          self.textBox.insert('end', receiver.decode())
        except:
          pass

chat = Chat()