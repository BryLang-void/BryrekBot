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
* **Lenguaje:** Python
* **Framework Backend:** FastAPI & Aiogram
* **Base de Datos:** PostgreSQL (Neon) & Redis
* **IA:** Groq API (Llama-3.3-70b-versatile)
* **Editor:** Neovim
* **Sistema:** Void Linux

---

## Como configurar las Variables de Entorno

Antes de ejecutar el proyecto, debes crear un archivo `.env` basado en el archivo `.env.example`:

```bash
cp .env.example .env
