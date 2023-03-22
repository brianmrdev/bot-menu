from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler, ContextTypes
from utils.buttons import button5, button1, button2, button3, button6, button7, button8, button9, button10, button11
from utils.functions import get_restaurant_list, get_menu_list, get_order_list, send_result
from utils.config import ASK_DIRECTION


async def restaurant_list_callback(update: Update, context: CallbackContext):
    """
    Funcion para manejar la lista de restaurantes
    """
    query = update.callback_query
    await query.answer()
    
    markup_restaurant = get_restaurant_list()
    
    await query.edit_message_text(
        text=str('Listado de Restaurantes'),
        reply_markup = markup_restaurant
    )
    

async def back_restaurant_list_callback(update: Update, context: CallbackContext):
    """
    Funcion para regresar al inicio
    """
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text='Hola {} bienvenido de nuevo!'.format(update.effective_user["first_name"]),
        reply_markup=InlineKeyboardMarkup([
            [button1],
            [button2, button5]
        ])
    )


async def select_menu_callback(update: Update, context: CallbackContext):
    """
    Función para manejar la selección del restaurante por el usuario y mostrar el menu de dicho restaurante
    """
    query = update.callback_query
    id_rest = int(query.data.split(":")[1])
    await query.answer()
    
    markup_menu = get_menu_list(id_rest)
    
    await query.edit_message_text(
        text=str('Seleccione un producto para agregarlo al carrito'),
        reply_markup = markup_menu
    )


async def add_to_cart(update: Update, context: CallbackContext):
    """
    Funcion para agregar los productos al carrito
    """
    query = update.callback_query
    cart = context.chat_data['cart']['product']
    product_id = int(query.data.split(":")[1])
    product_description = str(query.data.split(":")[2])
    product_price = float(query.data.split(":")[3])

    new_product = {"id": product_id, "description": product_description, "price":product_price }
    cart.append(new_product)    

    await query.answer(text=f"✅ Producto agregado al carrito.")


async def order_menu_callback(update: Update, context: CallbackContext):
    """
    Funcion para manejar el menu principal de órdenes
    """
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text='Consultar o generar órdenes',
        reply_markup=InlineKeyboardMarkup([
            [button6, button7],
            [button3]
            
        ])
    )


async def cart_menu_callback(update: Update, context: CallbackContext):
    """
    Función para regresar a la lista de restaurantes
    """
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        text='Consultar o limpiar el carrito',
        reply_markup=InlineKeyboardMarkup([
            [button8, button9],
            [button3]
            
        ])
    )



async def cart_list_callback(update: Update, context: CallbackContext):
    """
    Función para mostrar los productos que tiene el usuario en el carrito
    """
    cart = context.chat_data['cart']['product']
    query = update.callback_query
    await query.answer()
    
    list_product = [(producto["id"], producto["description"], producto["price"]) for producto in cart]
    
    msg = 'Listado de productos en el carrito\n\n'
    
    if len(list_product) == 0:
        msg += 'Su carrito esta vacio'
    else:
        total_price = 0
        for id, desc, price in list_product:
            msg += f"- {desc} - {price} $\n"
            total_price += price
        
        msg += f"\nTotal a pagar {str(total_price)} $"
    
    await query.edit_message_text(
        text=msg,
        reply_markup=InlineKeyboardMarkup([
            [button10]
            
        ])
    )
    

async def cart_clear_callback(update: Update, context: CallbackContext):
    """
    Función para vaciar el carrito del usuario
    """
    cart = context.chat_data['cart']['product']
    query = update.callback_query
    await query.answer()
    cart.clear()
    
    await query.edit_message_text(
        text='Se eliminaron los productos de su carrito',
        reply_markup=InlineKeyboardMarkup([
            [button10]
           
        ])
    )


async def order_list_callback(update: Update, context: CallbackContext):
    """
    Función para mostrar la lista de órdenes
    """
    id_user = context.chat_data['profile']['pk']
    query = update.callback_query
    await query.answer()
    list_order = get_order_list(id_user)
    
    msg = '📝 Listado de Órdenes\n\n'
    
    if list_order['count'] != 0:
        for result in list_order['results']:
            order_id = result['order_id']
            products = result['products']
            msg += "\n*********************"
            msg += f"\nOrder ID: {order_id}\n"
            total_price = 0
            for product in products:
                msg += f"- Product: {product['description']}, Price: {product['price']}\n"
                total_price += product['price']
            
            msg += f"Total {str(total_price)} $\n"
    else:
        msg += '❗ No existen órdenes.'
        
    
    await query.edit_message_text(
        text=msg,
        reply_markup=InlineKeyboardMarkup([
            [button11]
        ])
    )


async def order_create_callback(update: Update, context: CallbackContext):
    """
    Función para solicitar la dirección al usuario
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text='Por favor, ingresa su dirección para completar la órden o envíe /cancel para cancelarlo.'
    )
    return ASK_DIRECTION


async def ask_direction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Función para capturar la dirección enviada por el usuario y crear la orden
    """
    cart = context.chat_data['cart']['product']
    user_direction = update.message.text
    id_user = context.chat_data['profile']['pk']
    list_product = [producto["id"] for producto in cart]
    chat = update.message.chat
    await send_result(user_direction, chat, id_user, list_product, cart)
    return ConversationHandler.END



async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Funcion para cancelar el estado cuando el bot pregunta la dirección al usuario
    """
    await update.message.reply_text(
        "Su órden ha sido cancelada correctamente",
        reply_markup=InlineKeyboardMarkup([
            [button11]
        ])
    )
    return ConversationHandler.END