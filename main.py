# app id: 1170048577385529366
# public key: a03a5e1e7bf8ad23db4aa2e7df64c2806a2f42e9f66a81459313f67f0cd6066b 
import discord 
import os
import openai

file = input("Enter 1, 2, or 3 for loading the chat:\n ")
file = "1"
match(file):
  case "1":
    file = "first.txt"
  case "2":
    file = "second.txt"
  case "3": 
    file = "third.txt"
  case _:
    print("Invalid choice.")
    exit()
    
with open(file, "r") as f:
  chat = f.read() 

openai.api_key = os.getenv("OPENAI_API_KEY")
token = os.getenv("SECRET_KEY")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        global chat
        try:
          chat += f"{message.author}: {message.content}\n"
          print(f'Message from {message.author}: {message.content}')
          if self.user!= message.author:
              if self.user in message.mentions:
                response = openai.Completion.create(
                  model="text-davinci-003",
                  prompt = f"{chat}\ncandyBot: ",
                  temperature=1,
                  max_tokens=256,
                  top_p=1,
                  frequency_penalty=0,
                  presence_penalty=0
                )
                channel = message.channel
                messageToSend = response.choices[0].text
                await channel.send(messageToSend)    
        except Exception as e:
          print(e)
          chat = ""
            
      

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
