from telegram import InlineKeyboardButton

button1 = InlineKeyboardButton(text='🍽 Restaurantes', callback_data='restaurant_list')
button2 = InlineKeyboardButton(text='📝 Órdenes', callback_data='order_menu')
button3 = InlineKeyboardButton(text='⬅️ Regresar', callback_data='back_restaurant_list')
button4 = InlineKeyboardButton(text='⬅️ Regresar', callback_data='restaurant_list')
button5 = InlineKeyboardButton(text='🛒 Carrito', callback_data='cart_menu')
button6 = InlineKeyboardButton(text='📝 Consultar Órdenes', callback_data='order_list')
button7 = InlineKeyboardButton(text='💵 Generar Órden', callback_data='order_create')
button8 = InlineKeyboardButton(text='🛒 Ver carrito', callback_data='cart_list')
button9 = InlineKeyboardButton(text='❌ Vaciar carrito', callback_data='cart_clear')
button10 = InlineKeyboardButton(text='⬅️ Regresar', callback_data='cart_menu')
button11 = InlineKeyboardButton(text='⬅️ Regresar', callback_data='order_menu')