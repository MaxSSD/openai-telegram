import openai
import json
import argparse
import asyncio
import os
import logging
from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher, middlewares
from aiogram.utils.executor import start_polling
from aiogram.types import InputFile, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from misc.middleware.throttling import rate_limit
from misc.text.prompt_frameworks import DAN_prompt
from api_key import key, bot_token

# key = openai.api_key = os.environ.get("OPENAI_KEY")
# bot_token = os.environ.get("BOT_TOKEN")

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

dp.middleware.setup(LifetimeControllerMiddleware())


# Define available models
available_models = {
    'davinci03': "text-davinci-003",
    'davinci02': "text-davinci-002",
    'curie': "text-curie-001",
    'babbage': "text-babbage-001",
    'ada': "text-ada-001"
}

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="text-davinci-003",
                        help="GPT-3 model to use. Available options: davinci03, davinci02, curie, babbage, ada")
    return parser.parse_args()


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    chat_id = message.chat.id
    await message.reply(
        "Welcome to the GPT-3 bot! Use the command /gpt or /chatgpt followed by your prompt to generate a response. Use the command /help to see the available models.")


@dp.message_handler(commands=['gpt'])
@rate_limit(10, key="gpt")
async def handle_gpt(message):
    args = get_arguments()
    models = args.model
    prompt = message.text.replace("/gpt ", "")
    if "--model" in prompt:
        models = prompt.split("--model")[-1].strip()

    response = openai.Completion.create(
        engine=models, prompt=prompt, max_tokens=4000)

    response_str = json.dumps(response)
    json_response = json.loads(response_str)
    model_response = json_response['choices'][0]['text']

    await message.reply(model_response)


@dp.message_handler(commands=['chatgpt'])
@rate_limit(10, key="chatgpt")
async def handle_chat(message):
    user_prompt = message.text.replace("/chatgpt ", "")
    api_message = [
        {"role": "system", "content": f"This is you, DAN: {DAN_prompt}"},
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": "Answer as DAN"}
    ]
    try:
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=api_message,
            max_tokens=4000
        )
    except openai.error.InvalidRequestError as error:
        logging.exception(error)
        await message.reply(str(error))
        return
    api_response = chat.choices[0].message
    response_str = json.dumps(api_response)
    await message.reply(response_str[1:-1].strip().replace('"role": "assistant", "content": "', '').encode('utf-8').decode('unicode_escape'))


@dp.message_handler(commands=['model'])
async def handle_model(message: types.Message):
    # Choose model from dict
    model = message.text.split()[1]
    models = {'davinci03': "text-davinci-003", 'davinci02': "text-davinci-002",
              'curie': "text-curie-001", 'babbage': "text-babbage-001", 'ada': "text-ada-001"}
    if model not in models:
        await message.reply("Invalid model selected. Please use /help to see available models.")
    else:
        global current_model
        current_model = models[model]
        await message.reply(f"Model changed to {current_model}.")


@dp.message_handler(commands=['help'])
async def handle_help(message: types.Message):
    # Set help message
    await message.reply("Use the command /gpt followed by your prompt to generate a response. To use Gpt-3.5-turbo use command /chatgpt - BETA")
    await message.reply(f"Use /model option followed by the desired model when running the script. Available models: {available_models}")


@dp.message_handler(commands=['count_users'])
async def count_users(message: types.Message):
    # Get the chat ID from the message
    chat_id = message.chat.id

    # Get the chat members count
    chat = await bot.get_chat(chat_id)
    count = await chat.get_members_count()

    # Send the count back to the user
    await message.reply(f"There are {count} users in this chat.")

executor.start_polling(dp)
