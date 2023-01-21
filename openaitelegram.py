import openai
import json
import argparse
import asyncio
import os
from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling
from aiogram.types import InputFile
from api_key import key, bot_token

key = openai.api_key
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

previous_prompt = ""
previous_response = ""

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="text-davinci-003",
                        help="GPT-3 model to use. Available options:davinci03, davinci02, curie, babbage, ada")
    return parser.parse_args()

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    chat_id = message.chat.id
    await message.reply(
        "Welcome to the GPT-3 bot! Use the command /gpt followed by your prompt to generate a response. Use the command /help to see the available models.")

@dp.message_handler(commands=['gpt'])
async def handle_gpt(message):
    global previous_prompt, previous_response
    args = get_arguments()
    model = args.model
    prompt = message.text.replace("/gpt ", "")
    if "--model" in prompt:
        model = prompt.split("--model")[-1].strip()

    if prompt.startswith(previous_response):
        prompt = previous_prompt + prompt[len(previous_response):]

    response = openai.Completion.create(engine=model, prompt=prompt, temperature=0, max_tokens=4000,
                                        top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0)
    response_str = json.dumps(response)
    json_response = json.loads(response_str)
    api_response = json_response['choices'][0]['text']

    previous_prompt = prompt
    previous_response = api_response

    await message.reply(api_response)

@dp.message_handler(commands=['model'])
async def handle_model(message):
    model = message.text.split()[1]
    models = {'davinci03': "text-davinci-003", 'davinci02': "text-davinci-002", 'curie': "text-curie-001", 'babbage': "text-babbage-001", 'ada': "text-ada-001"}
    if model not in models:
        await message.reply("Invalid model selected. Please use /help to see available models.")
    else:
        global current_model
        current_model = models[model]
        await message.reply(f"Model changed to {current_model}.")

@dp.message_handler(commands=['help'])
async def handle_help(message):
    await message.reply("Use /model option followed by the desired model when running the script.")
    available_models = "davinci03, davinci02, curie, babbage, ada"
    await message.reply(f"Available models: {available_models}")

executor.start_polling(dp)
