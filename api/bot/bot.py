# from aiogram import Bot, Dispatcher, types
import asyncio
import logging
from datetime import datetime
import pandas as pd
from apps.letter.models import Letter
from apps.organization.models import Courier
    
TELEGRAM_BOT_TOKEN = '6648079265:AAFU8luv3XuQukTTHEcFb2n85k-0fAn8h30'

USER_ID = 663153232
CHANNEL_ID = -1001799708855

GROUP_USERNAME = '@triumf_archive'
ARCHIVE_ID = 2
UPLOAD_LETTER_ID = 6
COURIER_NOTIFIED_ID = 4



# async def msg(file_path):
#     bot = Bot(token=TELEGRAM_BOT_TOKEN)
#
#     session = await bot.get_session()
#     await bot.send_message(chat_id=GROUP_USERNAME, message_thread_id=ARCHIVE_ID, text="excel file")
#     await bot.send_document(chat_id=GROUP_USERNAME, message_thread_id=ARCHIVE_ID, document=types.InputFile(file_path))
#     await session.close()
#
# def load_data(excel_file_path):
#     letters = Letter.objects.filter(status='archived')
#
#     # Convert the queryset to a DataFrame
#     letter_data = pd.DataFrame.from_records(letters.values())
#     print(letter_data, ": =======================================\n\n=========================letter_data")
#     letter_data.to_excel(excel_file_path, index=False)
    

