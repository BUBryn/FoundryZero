#!/usr/bin/env python
# coding: utf-8

# In[105]:


import socket
import struct


# In[35]:


def getCommandID_And_Values(command):
    commandID = -1
    idOfTox = -1
    NumRating = -1
    while commandID < 0:    
        if "get recent tox id" in command:
            commandID = 1
            print("retrieving id of most recent tox")
            return commandID, idOfTox, NumRating
        
        elif "get tox" in command:
            commandID = 2
            commandValues = command.split(" ")
            idOfTox = int(commandValues[2])
            print("id of tox retrieved:", idOfTox)
            return commandID, idOfTox, NumRating
        
        elif ("rate tox" in command) and (("like" in command) or ("dislike" in command)):
            commandID = 3
            commandValues = command.split(" ")
            idOfTox = int(commandValues[2])
            rating = commandValues[3]
            if rating == "like":
                NumRating = 1
            else:
                NumRating = 255
            print(rating+" tox of id:"+str(idOfTox))
            return commandID, idOfTox, NumRating
    
        elif command == "fin":
            commandID = 4
            print ("Session Closed, Thank You for using TextTok")
            return commandID, idOfTox, NumRating
        
        else:
            print("\nplease input a valid command:\n")
            commandList = ["'get recent tox id' : Returns the ID of a recent tox that you might like","'get tox [id of tox you want to retrieve]' : Return the tox specified by an ID","'rate tox [id of tox you want to rate] [like/dislike]' : Thumbs up or thumbs down on a specified tox","'fin' : end session"]
            print(*commandList, sep="\n")
            print("\nPlease Enter a Command: (enter fin to close session)")
            command = str(input()).lower()
        


# In[53]:



def convertCommand(commandID, idOfTox, NumRating):
    if commandID == 1:
        convCommand = struct.pack('<B', commandID)
        return convCommand
    elif commandID == 2:
        convCommand = struct.pack('<B', commandID)+struct.pack('<i', idOfTox)
        return convCommand
    elif commandID == 3:
        convCommand = struct.pack('<B', commandID)+struct.pack('<i', idOfTox)+struct.pack('<B', NumRating)
        return convCommand
    
    


# In[104]:


def client_program():
    HOST = "texttok.fzero.io"  # The server's hostname or IP address
    PORT = 4000  # The port used by the server
    commandList = ["'get recent tox id' : Returns the ID of a recent tox that you might like","'get tox [id of tox you want to retrieve]' : Return the tox specified by an ID","'rate tox [id of tox you want to rate] [like/dislike]' : Thumbs up or thumbs down on a specified tox","'fin' : end session"]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connection Successful, Welcome to TextTok")
        print("list of valid commands:")
        print(*commandList, sep="\n")
        commandID = 0
        while commandID != 4:
            print("\nPlease Enter a Command: (enter fin to close session)")
            command = str(input()).lower()
            commandID, idOfTox, NumRating = getCommandID_And_Values(command)
            if commandID == 1:
                expected = 2
            elif commandID == 2:
                expected = 2
            elif commandID == 3:
                expected = 2

            if commandID != 4:
                convCommand = convertCommand(commandID, idOfTox, NumRating)
                s.send(convCommand)
                amount = 0
                data = []
                while amount < expected:
                    dataPart = s.recv(10000)
                    print(dataPart)
                    data.append(dataPart)
                    amount = amount +1
                messageType = interpretServerResponse(data)
        s.close()
        input()


# In[94]:


def interpretServerResponse(data):
    print(len(data))
    BinMessageType = data[0]
    messageType = int((struct.unpack('<B', BinMessageType))[0])
    if messageType == 255:
        return messageType
    else:
        if messageType == 64:
            BinRecentToxID = data[1]
            recentToxID = int((struct.unpack('<l', BinRecentToxID))[0])
            print("the retrieved ID of the recent tox is: ",recentToxID)
        elif messageType == 65:
            BinToxSize = data[1][0:4]
            ToxSize = int((struct.unpack('<L', BinToxSize))[0])
            BinTox = data[1][3:ToxSize]
            Tox = BinTox.decode('utf8')
            print("here is the tox you requested:\n"+Tox)
        elif messageType == 66:
            BinNewToxRating = data[1]
            NewToxRating = int(struct.unpack('<L', BinNewToxRating))[0])
            print("the new rating of the recent tox is: ",NewToxRating)
        return messageType
        
    


# In[106]:


if __name__ == '__main__':
    client_program()


# In[ ]:




