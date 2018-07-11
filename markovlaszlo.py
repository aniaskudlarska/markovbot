#MARKOV LASZLO
#author: ania
#version: 1.1

import discord
import os
import random

#to do: add a function to write the dictionary to a text file; add a function to read from the file

#GLOBAL VARIABLES ===========================================================
discord_token = 'YOUR_TOKEN_HERE'
client = discord.Client()
message_count = 0
message_random_chance = random.randint(2,10) #is larger to accumulate more data
word_dict = {"_START_" : []} #is initially empty

#STORE_TOKENS
#takes all tokens in a given string and puts them into a dictionary called word_dict
#the dictionary keys are the tokens, and each key's values is a list of words that comes after it
#the values may repeat if they occur multiple times. i'm sure there's a better algorithm for this.
def store_tokens(tokens):
    word_dict["_START_"].append(tokens[0])
    i = 0
    while i < len(tokens):
        if tokens[i] not in word_dict:
            if i == len(tokens)-1: #check if i is at the last element
                word_dict.setdefault(tokens[i], ["_END_"])
            else: #if there are still more tokens
                word_dict.setdefault(tokens[i], [ tokens[i+1] ])
        else: #if the token DOES exist in the dictionary
            if i == len(tokens)-1:
                word_dict[tokens[i]].append("_END_")
            else:
                word_dict[tokens[i]].append(tokens[i+1])
        print("'" + tokens[i] + "' added")
        i += 1;
    #print("\n\ntokens in map:")
    #for k,v in word_dict.items():
    #    print(k + ": " + str(v))

#COMPOSE_MESSAGE
#composes the message by randomly selecting items from the dictionary,
#starting with anything in the _START_ list
#until _END_ appears in a subsequent token's list
def compose_message():
    print("\n=========================================\ncomposing...")
    msg = ""
    start_choice = random.choice(word_dict["_START_"])
    choice = start_choice
    while choice != "_END_":
        msg += (choice + " ")
        choices = word_dict[choice] #choose the next token based on the current token's next token list
        choice = random.choice(choices) #select the token
    print(msg)
    return msg

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    global message_count
    global message_random_chance
    message_count += 1  
    
    print(str(message_count) + " of " + str(message_random_chance))
    message_l = message.content.lower() #set the message contents to lowercase
    tokens = message_l.split() #turn the contents into a list of tokens
    if tokens:
        store_tokens(tokens)
    
    if message_count == message_random_chance:
        print("sending message...")
        await client.send_typing(message.channel)
        message_count = 0
        message_random_chance = random.randint(1,3)
        composed_message = compose_message()
        await client.send_message(message.channel, composed_message)
    
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
client.run(discord_token)
print("shutting down...")
#to do: add a way for the bot to flush its dictionary to a text file
