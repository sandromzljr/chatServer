from concurrent.futures import thread
from email import message
from http import client
from pydoc import cli
import socket
from symtable import SymbolTableFactory
import threading
from winreg import CloseKey

#Conexão local host
HOST = '127.0.0.1'

#Porta para conexão
PORT = 55556

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

#Servidores
servers = {}

#Método de transmissão da mensagem
def broadcast(server, message):
  for i in servers[server]:
    #Caso mensagem for str, codificamos a mensagem
    if isinstance(message, str):
      message = message.encode()
    i.send(message)

#Função de enviar mensagem
def sendMessage(name, server, client):
  while True:
    message = client.recv(1024)
    message = ('{}: {} \n'.format(name, message.decode()))
    broadcast(server, message)

#While True para que o servidor fique no ar até ser encerrado
while True:
  #Aceitando conexão
  client, addr = server.accept()

  #Nome do servidor para conexão
  client.send(b'DIGITE NOME DO SERVER')

  #Recebendo nome do servidor e nome do usuário
  serverName = client.recv(1024).decode()
  name = client.recv(1024).decode()

  #Caso não exista, cria um servidor
  if server not in servers.keys():
    servers[server] = []
  servers[server].append(client)

  #Informando o server que a pessoa se conectou
  print('Bem vindo {}! Você está no server {}. INFO {}'.format(name, server, addr))
  
  #Transmitindo que alguém entrou na sala
  broadcast(server, '{}: Entrou na sala! \n'.format(name))

  #Rodando sendMessage em outra thread
  thread = threading.Thread(target=sendMessage, args=(name, server, client))
  thread.start()