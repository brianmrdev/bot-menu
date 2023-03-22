import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
from utils.config import ASK_DIRECTION
from utils.functions import start
from utils.callback_query_handler import ask_direction, restaurant_list_callback, back_restaurant_list_callback, select_menu_callback, add_to_cart, order_menu_callback, cart_menu_callback, cart_list_callback, cart_clear_callback, order_list_callback, order_create_callback, cancel



def main() -> None:
    """Run the bot."""
    
    # Carga las variables de entorno del archivo .env en el entorno actual
    load_dotenv()
    
    app = ApplicationBuilder().token(os.getenv('TOKEN')).build()
    
    # add handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(pattern='restaurant_list', callback=restaurant_list_callback))
    app.add_handler(CallbackQueryHandler(pattern='back_restaurant_list', callback=back_restaurant_list_callback))
    app.add_handler(CallbackQueryHandler(pattern='^filter_menu', callback=select_menu_callback))
    app.add_handler(CallbackQueryHandler(pattern='^add_to_cart', callback=add_to_cart))
    app.add_handler(CallbackQueryHandler(pattern='order_menu', callback=order_menu_callback))
    app.add_handler(CallbackQueryHandler(pattern='cart_menu', callback=cart_menu_callback))
    app.add_handler(CallbackQueryHandler(pattern='cart_list', callback=cart_list_callback))
    app.add_handler(CallbackQueryHandler(pattern='cart_clear', callback=cart_clear_callback))
    app.add_handler(CallbackQueryHandler(pattern='order_list', callback=order_list_callback))
    app.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(pattern='order_create', callback=order_create_callback)],
        states={
            ASK_DIRECTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_direction)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    ))

    
    app.run_polling()
    


if __name__ == '__main__' :  
    main()
    
