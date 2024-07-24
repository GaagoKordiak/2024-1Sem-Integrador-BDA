import logging
import csv
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '6547433727:AAEgiYB04L3RdQIV0wxzkxXTZa0wmlwNSQQ'  # substitua com o token do seu bot

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "Olá! Bem-vindo ao AgroScrape!\n\n"
        "Aqui estão os comandos disponíveis:\n"
        "/start - Iniciar o bot\n"
        "/help - Mostrar esta mensagem de ajuda\n"
        "/noticias - Ver as últimas notícias\n"
        "/cotacoes - Ver as cotações agrícolas\n"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = (
        "Aqui estão os comandos disponíveis:\n"
        "/start - Iniciar o bot\n"
        "/help - Mostrar esta mensagem de ajuda\n"
        "/noticias - Ver as últimas notícias\n"
        "/cotacoes - Ver as cotações agrícolas\n"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def read_csv_file(file_path, delimiter):
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=delimiter)
            next(reader)  # pula o cabeçalho
            return [row for row in reader]
    except Exception as e:
        logging.error(f"Erro ao ler o arquivo {file_path}: {e}")
        return []

async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Leitura do arquivo CSV
    with open("../WebScraper/embrapa.csv", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        noticias = [row for row in reader]
    # Enviar cada linha como uma mensagem separada
    for row in noticias:
        noticias_texto = f"{row[0]}: {row[1]}: {row[2]}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=noticias_texto)

async def cotacoes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Leitura do arquivo CSV
    with open("../WebScraper/noticiasagricolas.csv", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        cotacoes = [row for row in reader]

    # Enviar cada linha como uma mensagem separada
    for row in cotacoes:
        if len(row) >= 2:  # Verifica se a linha tem pelo menos dois elementos
            cotacoes_texto = f"{row[0]}: {row[1]}: {row[2]}: {row[3]}: {row[4]}: {row[5]}"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=cotacoes_texto)

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('noticias', noticias))
    application.add_handler(CommandHandler('cotacoes', cotacoes))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == '__main__':
    main()