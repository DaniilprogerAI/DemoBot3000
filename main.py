import asyncio
import logging
import sys
import yaml

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

with open("comfig.yaml", "r") as f:
    CONFIG = yaml.safe_load(f)

# Bot token can be obtained via https://t.me/BotFather
TOKEN = CONFIG["token"]

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`

    leave_bid = InlineKeyboardButton(text="leave bid", callback_data="leave bid")
    for_project = InlineKeyboardButton(text="for_project", callback_data="for_project")

    inline_kb_list = [[leave_bid], [for_project]]

    inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    await message.answer(f"I help you leave bid and hand over here administration.\nChose action", reply_markup=inline_markup)

@dp.query_handler(F.data == "leave bid")
async def guery_leave_bid(callback=CallbackQuery, state: FSMContext):

    await state.set_state(BidForm.waiting_for_name)

    await message.answer("What is the your first name?", reply_markup=ReplyKeyboardRemove())

@dp.message(BidForm.waiting_for_name)
async def process_bid_name(message: Message, state: FSMContext)
    await state.update_data(name=message.text)

    await state.set_state(BidForm.waiting_for_phone)
    await message.answer("What is the your phone?")
    
@dp.message(BidForm.waiting_for_name)
async def process_bid_phone(message: Message, state: FSMContext)
    await state.update_data(phone=message.text)
    
    await state.set_state(BidForm.wait_for_description)
    
    await message.answer("Briefly describe your request")

@dp.message(BidForm.wait_for_description)
async def  process_bid_description(message: Message, state: FSMContext)
    await state.update_data(description=message.text)
    yes = InlineKeyboardButton(text="Send", callback_data="send")
    no = InlineKeyboardButton(text="Rewrite", callback_data="rewrite")
    y_or_n = [[yes], [no]]

    y_or_n_reply = InlineKeyboardMarkup(inline_keyboard=y_on_n)

    await message.answer("All Right?", reply_markup=y_or_n_reply)

@query_handler(F.data == "rewrite")
async def end_of_for(callback: CallbackQuery)
    callback.message.answer("The end!")

@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
