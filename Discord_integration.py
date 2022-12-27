import discord
import openai
import textwrap

# Set the link to the source code
link = "https://github.com/Daxer97/chat_gpt3_discord_integration"

# Set the intents for the Discord client
intents = discord.Intents.all()

# Create the Discord client object
client = discord.Client(intents=intents)

# Print out all the intents for debugging purposes
for Intents in discord.Intents.all():
    print(Intents)

# Set the API key for the OpenAI library
openai.api_key = "OPEN_AI_KEY"


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
    print(client.user.name)
    print(client.user.id)
    print('------')

# Create an event handler for when a message is received
@client.event
async def on_message(message):
    # Check if the message was sent in the correct channel
    if message.channel.name == "chat-gpt3":
        # Check if the message was sent by the bot
        if message.author == client.user:
            return

        # Check if the message starts with the "/help" command
        if message.content.startswith("!help"):
            await message.channel.send(
                f"This bot has been written by Daxer, any pool request or issue can be uploaded here:\n\n-Source code: {link}")
        # If the message is not the "/help" command, generate and send a response
        elif message.content.startswith("!clear"):
            await message.channel.purge()
        elif message.content:
            # Generate the response
            response = generate_response(
                f" {message.content}. If a piece of code is provided within the response include a code block formatting using the right lamnguage key for code block in discord")
            print(response)
            # Define the send_response function
            async def send_response(response, channel):
                # Find the start and end of the code block in the response
                start = response.find("```")
                end = response.rfind("```")

                # Check if a code block is present in the response
                if start != -1 and end != -1:
                    # Split the response around the start and end of the code block
                    messages = response[:start].split("\n") + [response[start:end + 3]] + response[end + 3:].split("\n")
                else:
                    # Split the response into separate messages
                    messages = response.split("\n")

                # Initialize an empty list to store the formatted messages
                formatted_messages = []

                # Iterate through the messages
                for message in messages:
                    # Check if the message is a code block
                    if message.startswith("```") and message.endswith("```"):
                        # Add the code block to the list of formatted messages
                        formatted_messages.append(message)
                    else:
                        # Wrap the message and add the resulting lines to the list of formatted messages
                        formatted_messages.extend(textwrap.wrap(message, width=2000))

                # Send the formatted messages to the Discord channel
                for message in formatted_messages:
                    await channel.send(message)

            # Send the response to the Discord channel
            await send_response(response, message.channel)


# Start the Discord client
client.run("DISCORD_TOKEN")