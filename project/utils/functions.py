import requests
import random
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import Update
from telegram.ext import ContextTypes
from utils.config import API_URL, CONSULT_CLIENT_ENDPOINT, REGISTER_CLIENT_ENDPOINT, RESTAURANTS_ENDPOINT, MENU_ENDPOINT, ORDERS_ENDPOINT, CREATE_ORDER_ENDPOINT
from utils.buttons import button1, button2, button3, button4, button5, button11


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    chat_data = context.chat_data
    reply_markup = InlineKeyboardMarkup([
        [button1],
        [button2, button5],
    ])
    # Verifique si el usuario ya está registrado mediante una API
    response = requests.get(f'{API_URL}{CONSULT_CLIENT_ENDPOINT}{user_id}')
    if response.status_code == 200:            
        profile = response.json()
        if profile['exist'] == True:
            # Si el usuario está registrado, guarde sus datos en chat_data con la key profile
            chat_data['profile'] = profile['client']
            # Ademas creamos el carrito con la key cart
            chat_data['cart'] = {"product": []}
            await update.message.reply_text(f'Hola {chat_data["profile"]["first_name_telegram"]}, bienvenido de nuevo!', reply_markup=reply_markup)
        else:
            # Si el usuario no está registrado, registre al nuevo cliente mediante una API y guarde sus datos en chat_data con la key profile
            data = {'first_name_telegram': update.effective_user.first_name, 'username_telegram': update.effective_user.username, 'chatID': user_id, 'language_code': update.effective_user.language_code}
            response = requests.post(f'{API_URL}{REGISTER_CLIENT_ENDPOINT}', json=data)
            if response.status_code == 201:
                profile = response.json()
                chat_data['profile'] = profile
                await update.message.reply_text(f'Hola {chat_data["profile"]["username_telegram"]}, bienvenido!', reply_markup=reply_markup)
            else:
                await update.message.reply_text(f'❗ Lo siento, no se pudo registrar al usuario en este momento.\n\n Error: {response.status_code}')
    else:
        await update.message.reply_text(f'❗ El servicio no esta disponible en estos momentos. \n\n Error: {response.status_code}')
        

def get_restaurant_list():
    response = requests.get(f'{API_URL}{RESTAURANTS_ENDPOINT}')
    if response.status_code == 200:
        restaurantes = response.json()
        if restaurantes['count'] != 0:
            botones = []
            for restaurante in restaurantes['results']:
                boton = InlineKeyboardButton(text=restaurante['name'], callback_data=f"filter_menu:{restaurante['pk']}")
                botones.append([boton])
            
            botones.append([button3])
                
            markup = InlineKeyboardMarkup(botones)
            
            return markup
        else:
            return '❗ No hay restaurantes disponibles'
    else:
        return f'❗ El servicio no esta disponible en estos momentos. \n\n Error: {response.status_code}'


def get_menu_list(id_rest):
    response = requests.get(f'{API_URL}{MENU_ENDPOINT}{id_rest}')
    if response.status_code == 200:
        categorias = response.json()
        if categorias['count'] != 0:
            botones = []
            for categoria in categorias['results']:
                for product in categoria['products']:
                    boton = InlineKeyboardButton(text=f"{product['description']} - {product['price']} $", callback_data=f"add_to_cart:{product['pk']}:{product['description']}:{product['price']}")
                    botones.append([boton])
            botones.append([button4, button5])
            markup = InlineKeyboardMarkup(botones)
            return markup
        else:
            return '❗ El menu no esta disponible en estos momentos.'
    else:
        return f'❗ El servicio no esta disponible en estos momentos. \n\n Error: {response.status_code}'


def get_order_list(id_user):
    response = requests.get(f'{API_URL}{ORDERS_ENDPOINT}{id_user}')
    if response.status_code == 200:
        return response.json()
    else:
        return f'❗ El servicio no esta disponible en estos momentos.\n\n Error: {response.status_code}'


async def send_result(user_direction, chat, id_user, list_product, cart):
    
    if len(list_product) == 0:
        msg = '❗ No se pudo generar la órden, su carrito está vacio.'
    else:
        random_number = random.randint(1000, 9999)
        data = {'order_id': f"og-{random_number}", 'client':id_user, 'products': list_product, 'direction': user_direction}
        
        response = requests.post(f'{API_URL}{CREATE_ORDER_ENDPOINT}', json=data)
        if response.status_code == 201:
            cart.clear()
            msg = '✅ Órden creada satisfactoriamente.\n\n Puede ver sus órdenes consultando el menú "Consultar Órdenes"'
        else:
            msg = f"❗ Error al crear la orden.\n\n Error: {response.status_code}"
        
    await chat.send_message(
        text=msg,
        reply_markup=InlineKeyboardMarkup([
            [button11]
        ])
    )