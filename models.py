import re

import requests
from aiogram.types import FSInputFile
from openai import OpenAI

import google.generativeai as genai

import config
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model_gemini_flash = genai.GenerativeModel('gemini-1.5-flash')
model_gemini_pro = genai.GenerativeModel('gemini-1.5-pro')

OPENAI_API_KEY = config.GPT_API_KEY

client = OpenAI(
    api_key=OPENAI_API_KEY
)


async def generate(model_name, prompt, bot, user_id):
    msg = await bot.send_message(user_id, 'Генерируем⏳')
    if model_name == "Gemini Flash":
        print('Generating Gemini Flash...')
        response = model_gemini_flash.generate_content([prompt])
        await bot.send_message(user_id, response.text)
    elif model_name == "Gemini PRO":
        print('Generating Gemini PRO...')
        response = model_gemini_pro.generate_content([prompt])
        await bot.send_message(user_id, response.text)
    elif model_name == "GPT 3.5":
        print('Generating GPT 3.5...')
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user",
                       "content": [
                           {
                               "type": "text",
                               "text": f"{prompt}"
                           }
                       ]
                       }],
            stream=True,
        )

        tx = ''
        n = 0
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                n += 1
                # print(chunk.choices[0].delta.content, end="")
                tx += chunk.choices[0].delta.content
                if n % 25 == 0:
                    await bot.edit_message_text(text=tx, chat_id=user_id,
                                                message_id=msg.message_id)
        try:
            await bot.edit_message_text(text=tx, chat_id=user_id,
                                        message_id=msg.message_id)
        except:
            pass
    elif model_name == "GPT 4o":
        print('Generating GPT 4o...')
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user",
                       "content": [
                           {
                               "type": "text",
                               "text": f"{prompt}"
                           }
                       ]
                       }],
            stream=True,
        )

        tx = ''
        n = 0
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                n += 1
                # print(chunk.choices[0].delta.content, end="")
                tx += chunk.choices[0].delta.content
                if n % 25 == 0:
                    await bot.edit_message_text(text=tx, chat_id=user_id,
                                                message_id=msg.message_id)
        try:
            await bot.edit_message_text(text=tx, chat_id=user_id,
                                        message_id=msg.message_id)
        except:
            pass
    else:
        print('Generating DALL-E 3...')
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        response = requests.get(image_url)

        # Сохраняем изображение в файл
        with open(f"{user_id}.png", "wb") as f:
            f.write(response.content)
        photo = FSInputFile(f"{user_id}.png")
        await bot.send_photo(user_id, photo, caption=f'Генерация по промту:\n{prompt}')
