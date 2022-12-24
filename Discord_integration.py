import discord
import openai

# Set the link to the source code
link = "https://github.com/Daxer97/chat_gpt3_discord_integration"

# Set the intents for the Discord client
intents = discord.Intents.all()

# Create the Discord client object
client = discord.Client(intents=intents)

# Print out all the intents for debugging purposes
for Intents in discord.all():
    print(Intents)

# Set the API key for the OpenAI library
openai.api_key = "Open AI API key"

# Define the generate_response function
def generate_response(message):
    # Use the OpenAI Completion API to generate a response
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{message}\n",
        max_tokens=1024,
        temperature=0.6,
    )
    
    # Return the text of the first response choice
    return response.choices[0].text

# Create an event handler for when the Discord client is ready
@client.event
async def on_ready():
    print("Loged in!")

# Create an event handler for when a message is received
@client.event
async def on_message(message):
    # Check if the message was sent in the correct channel
    if message.channel.name == "chat-gpt3":
        # Check if the message was sent by the bot
        if message.author == client.user:
            return
        
        # Check if the message starts with the "/help" command
        if message.content.startswith("/help"):
            await message.channel.send(f"This bot has been written by Daxer, any pool request or issue can be uploaded here:\n\n-Source code: {link}")
        # If the message is not the "/help" command, generate a response
        elif message.content:
            response = generate_response(f" {message.content}")
            await message.channel.send(response)

# Start the Discord client
client.run("Discord bot token")
