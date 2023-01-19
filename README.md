# openai-telegram-bot
This is a Telegram bot that utilizes the OpenAI GPT-3 API to generate responses based on user prompts. The bot can be controlled using the following commands:

/gpt followed by the prompt: This will generate a response using the current model. The user can also specify a different model by including --model [model_name] in the prompt.

/model [model_name]: This changes the current model to the specified model. 
The available models are: 
* text-davinci-003
* text-davinci-002
* text-curie-001
* text-babbage-001

/help: This displays information on how to use the bot and lists the available models.

# Installation
To use this script, you will need to have Python 3.7 or later installed. You can download Python from the official website.

You will also need to install the following Python packages:
```
openai
aiogram
asyncio
```
You can install these packages using pip:
```
pip install openai aiogram json
```

# Usage
1. Clone this repository to your local machine.
2. Create an account on the [OpenAI website](https://beta.openai.com/) and obtain an API key.
3. Create a api_key.py file in the same directory as the script, and add your OpenAI API key to it.
```
key = "YOUR_API_KEY"
```
4. Create a new bot on Telegram and obtain the bot_token.
5. Run the script using the following command:
```
python openaitelegram.py
```
6. Start a conversation with the bot on Telegram and use the command !gpt followed by your message to receive a response from the GPT-3 engine.
7. To exit the script, you can use the command !gpt exit

# Note
You need to run this script on a server so that it can run 24/7, otherwise it will run only when you run the script on your local machine.

# Additional Resources
[Telethon documentation](https://docs.telethon.dev/en/stable/index.html#)

[OpenAI API documentation](https://beta.openai.com/docs/guides/completion/introduction)

[Creating a Telegram bot](https://core.telegram.org/bots)

# Limitations

* This script is using GPT3 model, so the response will be based on the content that model was trained on.

* This script is not hosted on Heroku or other hosting platform.

# License
This script is licensed under the MIT license. Feel free to use and modify it for your own projects

# Contribution
Feel free to contribute to this project by creating a pull request. Any contributions are welcome and appreciated.
