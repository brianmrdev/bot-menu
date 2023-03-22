# Examen práctico
## Bot - Menú

Desarrollo de un Bot de Telegram para Registro de Clientes, Listado de Restaurantes y Generación de Órdenes de Comida.

### Stack de tecnologías utilizadas

- [python-telegram-bot](https://python-telegram-bot.org/)

- [Docker](https://www.docker.com/)

### Construir y ejecutar
1.  Clone el repositorio:
    ```bash
    git clone https://github.com/brianmrdev/bot-menu.git
    cd bot-menu/project
    ```
2.  Crea el fichero `.env` (o renombra y modifica `.env.example`) en la raíz del proyecto y establece la variable de entorno para el bot:
    ```bash
    touch .env
    echo TOKEN=<bot-token> >> .env
    ```
3.  Construir imagen de docker:
    ```bash
    docker build -t bot-menu .
    ```
4.  Ejecutar el bot:
    ```bash
    docker run --name bot-menu -d bot-menu:latest
    ```
5.  Verificar si el contenedor está en ejecución:
    ```bash
    docker ps
    ```
6. Si el contenedor está ejecutandose ya puede iniciar el bot en telegram.
