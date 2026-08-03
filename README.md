# <p align="center"> <img src="logo.png" width="200"> <br> **BryrekBot** </p>

Bot de Telegram impulsado por Inteligencia Artificial (Llama 3.3 vía Groq), con backend asíncrono, persistencia de datos en PostgreSQL y gestión de estados/caché con Redis.

## Descripcion
**BryrekBot** es un proyecto de asistente conversacional diseñado con arquitectura asíncrona y estructurado bajo buenas prácticas. Integra la API de Telegram con FastAPI a través de Webhooks, permitiendo procesar mensajes de forma rápida. Utiliza PostgreSQL (Neon) para el registro de usuarios, Redis para el manejo de estados de conversación (FSM) y la API de Groq para responder mensajes mediante el modelo Llama 3.3 de forma breve, concisa y directa.

## Funciones
* **FastAPI:** Servidor HTTP asíncrono para recibir peticiones vía Webhook.
* **Aiogram 3:** Framework asíncrono moderno para interactuar con la API de Telegram Bot.
* **Groq (Llama 3.3 70B):** Generación de respuestas inteligentes y resumidas mediante IA.
* **PostgreSQL + SQLAlchemy Async:** Base de datos relacional con ORM asíncrono para almacenar usuarios.
* **Redis:** Manejo de sesiones, estados de la conversación (FSM) y almacenamiento en caché.
* **Patrón Repository & Service:** Código limpio y modular separando la lógica de acceso a datos de la lógica del bot.

## Tecnologias
* **Lenguaje:** Python 3.10+
* **Framework Backend:** FastAPI & Aiogram
* **Base de Datos:** PostgreSQL (Neon) & Redis
* **IA:** Groq API (Llama-3.3-70b-versatile)
* **Editor:** Neovim

---

## Como configurar las Variables de Entorno

Antes de ejecutar el proyecto, debes crear un archivo `.env` basado en el archivo `.env.example`:

```bash
cp .env.example .env
```

Configura las siguientes variables en tu `.env`:

* `TELEGRAM_TOKEN`: Token otorgado por [@BotFather](https://t.me/BotFather).
* `WEBHOOK_URL`: URL pública HTTPS de tu servidor (p. ej., utilizando Ngrok o un VPS).
* `HOST`: Dirección IP donde correrá FastAPI (ej. `0.0.0.0`).
* `PORT`: Puerto de ejecución (ej. `8080`).
* `REDIS_URL`: URL de conexión a tu instancia de Redis (compatible con `rediss://`).
* `DB_URL`: String de conexión PostgreSQL con driver `asyncpg`.
* `GROQ_API_KEY`: Tu API Key obtenida de la consola de Groq.

---

## Como ejecutar

### descargar repositorio:
para descargar este repositorio deberás tener instalado git, puedes instalarlo asi:
* **Android:** ``pkg install git``
* **IOS:** ``apk add git``
* **MacOS:** ``xcode-select --install``
* **Windows:** abre terminal de administrador y ejecuta ``winget install --id Git.Git -e --silent``
* **Linux:** usa el gestor de paquetes de tu distribucion y descarga **git**
* *en el sistema en el que estés ejecuta estos comandos:*
```bash
git clone https://github.com/TuUsuario/BryrekBot.git
cd BryrekBot
```

### crear entorno virtual e instalar dependencias:
para instalar lo necesario ejecuta los siguientes comandos dependiendo tu sistema:

* **Linux / MacOS / Android (Termux):**
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

* **Windows:**
```powershell
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
```

### ejecutar:
para levantar el servidor de FastAPI junto con el bot de Telegram ejecutando Webhooks:

* **Linux / MacOS / Android:**
```bash
source env/bin/activate
python3 main.py
```

* **Windows:**
```powershell
.\env\Scripts\Activate.ps1
python main.py
```

* **NOTA:** Al iniciar, el servidor creará automáticamente las tablas en PostgreSQL si no existen y registrará la `WEBHOOK_URL` en Telegram. Puedes verificar que el servidor está activo ingresando a `http://localhost:8080/`.
