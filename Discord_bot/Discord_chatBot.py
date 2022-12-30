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
openai.api_key = "OPEN_AI_TOKEN"


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

#Define the send_response() function
async def send_response(response, channel):
    # Find the start and end of the code block in the response
    start = response.find("```")
    end = response.rfind("```")

    # Check if a code block is present in the response
    if start != -1 and end != -1:
        print("code block found")
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
            # Extract the language key from the message
            language_key = message[3:message.index('\n')]
            print(f"{language_key}")
            # Remove the triple backticks and the language key from the beginning of the message
            message = message[len(language_key) + 3:]

            # Check if the message is more than 2000 characters long
            if len(message) > 1990:
                print("code block longer than 1990")
                # Initialize the list of chunks
                chunks = []

                # Split the message into chunks of 2000 characters or less, preserving the whitespace
                while len(message) > 1990:
                    print("code block greater than 1990 charcaters")
                    chunk = message[:message.rindex('\n', 0, 1990)]
                    chunks.append(chunk)
                    message = message[len(chunk):]

                # Add the remaining message as the last chunk
                chunks.append(message)

                # Add the triple backticks, language key, and whitespace to the beginning of each chunk except the last one
                chunks = [f"```{language_key}\n{chunk}\n```" for chunk in chunks[:-1]]
                for ch in chunks:
                    print(f"{len(ch)}")

                # Add the triple backticks, language key, and whitespace to the beginning of the last chunk
                chunks.append(f"```{language_key}\n{chunks[-1]}")

                # Add the chunks to the list of formatted messages
                formatted_messages.append(chunks)
            else:
                print("code block no longer than 1990")
                # Add the triple backticks, language key, and whitespace to the beginning of the message
                message = f"```{language_key}\n{message}"

                # Add the message to the list of formatted messages
                formatted_messages.append(message)

        else:
            # Wrap the message and add the resulting lines to the list of formatted messages
            formatted_messages.extend(textwrap.wrap(message, width=2000))

    # Send the formatted messages to the Discord channel
    for message in formatted_messages:
        print(f"{len(message)} response")
        await channel.send(message)

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
                f" {message.content}. The entire response need to be written in markdown markup language, containing code while asked and with the right language key on the code block matching the context. Use '**' instead of '#' and '***' instead of '##' while using markdown.")
            #print(len(response))
            if len(response) < 1900:
                print(f"Less than 1900 characters response\n{response}")
                await message.channel.send(response)
            else:
                print(len(response))
                # Send the response to the Discord channel
                await send_response(response, message.channel)

# Start the Discord client
client.run("DISCORD_TOKEN")