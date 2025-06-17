from aiogram import types, Router, F, Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, InlineKeyboardButton, \
    InputMediaPhoto, BotCommand, InputMediaVideo, InputMediaDocument
from aiogram.filters import Command
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.exceptions import TelegramBadRequest
from aiogram.enums import ParseMode

import asyncio

from markdown_it.common.entities import entities
from pyrogram.filters import caption

from AI_TGK.gigachat import giga
from AI_TGK.habr_parser import pars_news, titles_sort, data, parser_article
from AI_TGK.promts import promt_habr_1

rt1 = Router()
ADMIN_LIST = [1696788497]
channel_main = '-1002554633095'
channel_test = '-1002297821651'

media_list = []
edit_media = []
callback_posts = {}
ready_posts = {}

@rt1.message(Command("menu"))
@rt1.message(Command("start"))
async def start(msg: Message):
    global callback_posts, media_list, edit_media, ready_posts
    media_list.clear()
    edit_media.clear()
    callback_posts.clear()
    ready_posts.clear()

    if msg.chat.id in ADMIN_LIST:
        a = await msg.answer("Процесс парсинга начат ⌛")
        promt = pars_news(promt_habr_1)
        await a.edit_text("Осталось совсем чу-чуть 🤏")
        titles = titles_sort(promt)
        for i in range(len(titles)):
            callback_posts[str(i)] = titles[i]

        text = "Выберите заголовок на генерацию\n\n"
        for i in callback_posts:
            text += f"{i}. {callback_posts[i]}\n\n"

        await a.edit_text(text=text)

@rt1.message(lambda msg: msg.text in callback_posts.keys())
async def generate_post(msg: Message):
    rows = [[InlineKeyboardButton(text="Сгенерировать", callback_data=f"generate_{msg.text}")]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    try:
        await msg.answer('Вы выбрали\n'
                         f'{callback_posts[msg.text]}\n\n'
                         f'{data[callback_posts[msg.text]]['text']}', reply_markup=markup)
    except Exception as ex:
        print(ex)

@rt1.callback_query(lambda query: query.data in ["generate_" + i for i in callback_posts.keys()])
async def generate_post2(call: CallbackQuery):
    media = []
    msg_del = await call.message.answer("Идет генерация")
    rows = [[InlineKeyboardButton(text="Редактировать медиа", callback_data=f"edit_media_{call.data.replace("generate_", "")}")],
            [InlineKeyboardButton(text="Редактировать текст", callback_data=f"edit_text_{call.data.replace("generate_", "")}")],
            [InlineKeyboardButton(text='Опубликовать', callback_data=f"publish_{call.data.replace("generate_", "")}")]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    try:
        article = parser_article(data[callback_posts[call.data.replace('generate_', '')]]['href'])
        text = (f"{callback_posts[call.data.replace('generate_', '')]}\n\n"
            f"{article['text']}\n\n")

        if len(article["imgs"]) != 0:
            for i in range(len(article['imgs'])):
                if i == 0:
                    media.append(InputMediaPhoto(media=article['imgs'][i], caption=text, parse_mode="html"))
                else:
                    media.append(InputMediaPhoto(media=article['imgs'][i]))

            try:
                await msg_del.delete()

                await call.message.answer_media_group(media)
                await call.message.answer(f'👆\n{article["href"]}', reply_markup=markup, disable_web_page_preview=True)

                ready_posts[call.data.replace("generate_", "")] = {
                    "media": media,
                    "text": text
                }

            except TelegramBadRequest as ex:
                print(ex)
                await call.answer('Слишком длинный пост')

        else:
            await msg_del.delete()
            await call.message.answer(text=text, reply_markup=markup, parse_mode="html")

    except:
        await call.message.answer("Ошибка генерации")

@rt1.callback_query(lambda query: query.data in ["publish_" + i for i in ready_posts.keys()])
async def publish_post(call: CallbackQuery, bot: Bot):
    rows = [[InlineKeyboardButton(text="Основа", callback_data=f"{call.data.replace("publish", "main")}")],
            [InlineKeyboardButton(text="Тестовый", callback_data=f"{call.data.replace("publish", "test")}")]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)

    await call.message.edit_text("Куда публиковать", reply_markup=markup)

@rt1.callback_query(lambda query: query.data in ["test_" + i for i in ready_posts.keys()])
@rt1.callback_query(lambda query: query.data in ["main_" + i for i in ready_posts.keys()])
async def publish_post_2(call: CallbackQuery, bot: Bot):
    if call.data[0:5] == "main_":
        await bot.send_media_group(chat_id=channel_main, media=ready_posts[call.data.replace("main_", "")]['media'])
    else:
        await bot.send_media_group(chat_id=channel_test, media=ready_posts[call.data.replace("test_", "")]['media'])
    await call.answer("Опубликовано")

class Edit_post(StatesGroup):
    edit_text = State()
    edit_media = State()
    answer_media = State()
ready_id = None

@rt1.callback_query(lambda query: query.data in ["edit_media_" + i for i in ready_posts.keys()])
async def edit_post(call: CallbackQuery, state: FSMContext):
    global ready_id, media_list
    media_list = []
    ready_id = call.data.replace("edit_media_", "")

    await call.message.answer("Отправь фото")
    await state.set_state(Edit_post.edit_media)

@rt1.message(Edit_post.edit_media)
async def edit_post_2(msg: Message, state: FSMContext):
    global edit_media, media_list

    kb = [[types.KeyboardButton(text="Сохранить фото и продолжить")]]
    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    try:
        if msg.text == 'Сохранить фото и продолжить':
            await msg.answer(text='Фото сохранены. Отправь любой текст что бы продолжить', reply_markup=types.ReplyKeyboardRemove())
            await state.set_state(Edit_post.answer_media)
        else:
            media_item = None
            media_type = None

            if msg.photo:
                media_item = msg.photo[-1].file_id
                media_type = 'photo'
            elif msg.video:
                media_item = msg.video.file_id
                media_type = 'video'
            elif msg.animation:
                media_item = msg.animation.file_id
                media_type = 'animation'

            caption = ready_posts[ready_id]["media"][0].caption
            entities = ready_posts[ready_id]["media"][0].caption_entities

            media_list.append({
                'type': media_type,
                'file_id': media_item,
                'caption': caption,
                'entities': entities
            })

            await state.update_data(media_list=media_list)

            msg = await msg.answer(
                f"Медиа добавлено: {len(media_list)}\n"
                "Отправьте еще или нажмите кнопку для продолжения",
                reply_markup=markup
            )

    except TypeError:
        await msg.answer(text='Пришлите фото!')

@rt1.message(Edit_post.answer_media)
async def edit_post_3(msg: Message, state: FSMContext):
    global ready_id
    data = await state.get_data()
    ready_posts[ready_id]["media"] = []

    media = []
    for i in range(len(data["media_list"])):
        if i == 0:
            if data["media_list"][i]['type'] == 'photo':
                media_obj = InputMediaPhoto(
                    media=data["media_list"][i]['file_id'],
                    caption=data["media_list"][i]['caption'],
                    caption_entities=data["media_list"][i]['entities']
                )
            elif data["media_list"][i]['type'] == 'video':
                media_obj = InputMediaVideo(
                    media=data["media_list"][i]['file_id'],
                    caption=data["media_list"][i]['caption'],
                    caption_entities=data["media_list"][i]['entities']
                )
            else:
                # Для документов, аудио и других типов
                media_obj = InputMediaDocument(
                    media=data["media_list"][i]['file_id'],
                    caption=data["media_list"][i]['caption'],
                    caption_entities=data["media_list"][i]['entities']
                )
            media.append(media_obj)
        else:
            if data["media_list"][i]['type'] == 'photo':
                media_obj = InputMediaPhoto(
                    media=data["media_list"][i]['file_id']
                )
            elif data["media_list"][i]['type'] == 'video':
                media_obj = InputMediaVideo(
                    media=data["media_list"][i]['file_id']
                )
            else:
                # Для документов, аудио и других типов
                media_obj = InputMediaDocument(
                    media=data["media_list"][i]['file_id']
                )
            media.append(media_obj)
    if media:
        ready_posts[ready_id]["media"] = media

    rows = [
        [InlineKeyboardButton(text="Редактировать медиа", callback_data=f"edit_media_{ready_id}")],
        [InlineKeyboardButton(text="Редактировать текст", callback_data=f"edit_text_{ready_id}")],
        [InlineKeyboardButton(text='Опубликовать', callback_data=f"publish_{ready_id}")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)

    try:
        await msg.answer_media_group(media=media)
        await msg.answer('👆 Обновленный пост', reply_markup=markup)
    except Exception as e:
        await msg.answer(f"Ошибка при отправке: {str(e)}")

    await state.clear()
@rt1.callback_query(lambda query: query.data in ["edit_text_" + i for i in ready_posts.keys()])
async def edit_text(call: CallbackQuery, state: FSMContext):
    global ready_id
    text = f"{ready_posts[call.data.replace("edit_text_", "")]['text']}"

    await call.message.answer(text=ready_posts[call.data.replace("edit_text_", "")]["media"][0].caption,
                              entities=ready_posts[call.data.replace("edit_text_", "")]["media"][0].caption_entities)
    await call.message.answer("Отправь свой отредактированный текст")

    ready_id = call.data.replace("edit_text_", "")
    await state.set_state(Edit_post.edit_text)

@rt1.message(Edit_post.edit_text)
async def edit_text_2(msg: Message, state: FSMContext):
    rows = [[InlineKeyboardButton(text="Редактировать медиа",callback_data=f"edit_media_{ready_id}")],
            [InlineKeyboardButton(text="Редактировать текст",callback_data=f"edit_text_{ready_id}")],
            [InlineKeyboardButton(text='Опубликовать', callback_data=f"publish_{ready_id}")]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)

    edit_text = msg.text
    ready_posts[ready_id]["text"] = edit_text

    ready_posts[ready_id]["media"][0].parse_mode = None
    ready_posts[ready_id]["media"][0].caption = edit_text
    ready_posts[ready_id]["media"][0].caption_entities = msg.entities

    await msg.answer_media_group(media=ready_posts[ready_id]["media"])
    await msg.answer(f'👆 Пост', reply_markup=markup, disable_web_page_preview=True)
    await state.clear()