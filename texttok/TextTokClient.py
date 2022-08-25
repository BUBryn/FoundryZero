#!/usr/bin/env python
# coding: utf-8

# In[105]:


import socket#import for network/client/server interface module
import struct#import for coversion module


# In[35]:


def getCommandID_And_Values(command):#function for finding which request the client wants to make
    commandID = -1
    idOfTox = -1
    NumRating = -1
    #all return values are set to a default negative number 
    while commandID < 0: #whileloop to find the command they wish to use   
        if "get recent tox id" in command: # command type 1: get recent tox id
            commandID = 1
            print("retrieving id of most recent tox")
            return commandID, idOfTox, NumRating
        
        elif "get tox" in command: # command type 2: get tox [id]
            commandID = 2
            commandValues = command.split(" ")# splits command into parts
            idOfTox = int(commandValues[2]) #retrieves ID for tox to get
            return commandID, idOfTox, NumRating
        
        elif ("rate tox" in command) and (("like" in command) or ("dislike" in command)): # command type 3: rate tox [id] [like/dislike]
            commandID = 3
            commandValues = command.split(" ")#split command into parts
            idOfTox = int(commandValues[2])#retrieves ID of tox to rate
            rating = commandValues[3]#retrieves client rating of tox
            if rating == "like":#converts rating into number (1 for Like, 255 for dislike)
                NumRating = 1
            else:
                NumRating = 255
            print(rating+" tox of id:"+str(idOfTox))
            return commandID, idOfTox, NumRating
    
        elif command == "fin": # command type 4: end session
            commandID = 4
            print ("Session Closed, Thank You for using TextTok")
            return commandID, idOfTox, NumRating
        
        else: # if command does not fit any of the valid commands, asks for new input
            print("\nplease input a valid command:\n")
            commandList = ["'get recent tox id' : Returns the ID of a recent tox that you might like","'get tox [id of tox you want to retrieve]' : Return the tox specified by an ID","'rate tox [id of tox you want to rate] [like/dislike]' : Thumbs up or thumbs down on a specified tox","'fin' : end session"]
            print(*commandList, sep="\n")
            print("\nPlease Enter a Command: (enter fin to close session)")
            command = str(input()).lower()
        


# In[53]:



def convertCommand(commandID, idOfTox, NumRating):#function for converting command and values into little endian 
    if commandID == 1:#command type 1: get recent tox ID
        convCommand = struct.pack('<B', commandID)
        return convCommand
    elif commandID == 2:#command type 2: get tox [id]
        convCommand = struct.pack('<B', commandID)+struct.pack('<i', idOfTox)
        return convCommand
    elif commandID == 3:#command type 3: rate tox [id] [like/dislike]
        convCommand = struct.pack('<B', commandID)+struct.pack('<i', idOfTox)+struct.pack('<B', NumRating)
        return convCommand#returns converted command to be submitted to server
    
    


# In[104]:


def client_program():
    HOST = "texttok.fzero.io"  # The server's hostname or IP address
    PORT = 4000  # The port used by the server
    commandList = ["'get recent tox id' : Returns the ID of a recent tox that you might like","'get tox [id of tox you want to retrieve]' : Return the tox specified by an ID","'rate tox [id of tox you want to rate] [like/dislike]' : Thumbs up or thumbs down on a specified tox","'fin' : end session"]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:#intialise socket object
        s.connect((HOST, PORT))#connect to server
        print("Connection Successful, Welcome to TextTok")
        print("\nlist of valid commands:")
        print(*commandList, sep="\n")#print list of valid commands
        commandID = 0 #intialise command ID
        while commandID != 4: #while loop to keep connection open until end session command is typed
            print("\nPlease Enter a Command: (enter fin to close session)")
            command = str(input()).lower()#take user command input
            commandID, idOfTox, NumRating = getCommandID_And_Values(command)#get command type and values from input

            if commandID != 4:#check to see if command needs to be sent to server or is end session command
                expected = 2 #defines the number of responses from server expected
                convCommand = convertCommand(commandID, idOfTox, NumRating)#convert command type and values to little endian
                s.send(convCommand)#send request to server
                amount = 0#intialise varible to store number of responses recieved
                data = []#intialise array/list for data from each response part
                while amount < expected:#while responses recieved < reponses expected
                    dataPart = s.recv(10000)#store response from server
                    data.append(dataPart)#append new response to array
                    amount = amount +1 #increment responses recieved
                    if int((struct.unpack('<B', data[0]))[0]) == 255:#check if error code
                        expected = amount# set expected responses to number recieved to prevent hanging    
                messageType = interpretServerResponse(data)#interpert server response
                if messageType == 255:#if error code
                    print("the command: '"+command+"' failed to return a result, please try again")
        s.close()# close connection
        input()


# In[94]:


def interpretServerResponse(data):#function for interpreting response from server
    BinMessageType = data[0]#extract message type from response
    messageType = int((struct.unpack('<B', BinMessageType))[0])#convert message type to interger
    if messageType == 255:# check if server failed to execute command
        return messageType
    else:
        if messageType == 64:# response type 64: Recent Tox ID
            BinRecentToxID = data[1]#extract ID of tox from response
            recentToxID = int((struct.unpack('<l', BinRecentToxID))[0])#convert ID of tox to number
            print("the retrieved ID of the recent tox is: ",recentToxID)#print converted ID and message
        elif messageType == 65:# response type 65: Tox
            BinToxSize = data[1][0:4]#extract size of tox
            ToxSize = int((struct.unpack('<L', BinToxSize))[0])#convert size of tox to number
            print("estimated size of requested tox: ", ToxSize)
            BinTox = data[1][4:]#extract tox
            Tox = BinTox.decode('utf8')#decode tox
            print("real size of requested tox: ",len(Tox) )
            print("here is the tox you requested:\n"+Tox)#print tox and message
        elif messageType == 66:# response type 66:
            BinNewToxRating = data[1]#extract new rating from response
            NewToxRating = int((struct.unpack('<L', BinNewToxRating))[0])#convert new rating
            print("the new rating of the tox is: ",NewToxRating)#print new rating and message
        return messageType
        
    


# In[106]:


if __name__ == '__main__':#program main
    client_program()#run client program


# In[ ]:




