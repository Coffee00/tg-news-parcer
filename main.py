from telethon import TelegramClient, events
import os
import asyncio

api_id = '23963854'
api_hash = 'cfbe95064159720206325bf9a4fabea6'
channels_file = 'channels.txt'  # Файл для хранения ссылок на каналы
target_channel = -1002295023854  # Ссылка на канал, куда отправляем новости
admin_user_id = 671873653  # ID администратора, который может добавлять и удалять каналы


async def load_channels():
    """Загружает каналы из файла."""
    if not os.path.exists(channels_file):
        return []
    with open(channels_file, 'r') as file:
        return [int(line.strip()) for line in file if line.strip()]


async def add_channel(channel_id):
    """Добавляет канал в файл с обработкой ошибок."""
    try:
        channel_id = int(channel_id)
    except ValueError:
        return f"Ошибка: {channel_id} не является действительным идентификатором канала."

    channels = await load_channels()
    if channel_id in channels:
        return f"Канал {channel_id} уже существует в списке."

    with open(channels_file, 'a') as file:
        file.write(f"{channel_id}\n")
    return f"Канал {channel_id} успешно добавлен."


async def remove_channel(channel_id):
    """Удаляет канал из файла с обработкой ошибок."""
    try:
        channel_id = int(channel_id)
    except ValueError:
        return f"Ошибка: {channel_id} не является действительным идентификатором канала."

    channels = await load_channels()
    if channel_id not in channels:
        return f"Канал {channel_id} отсутствует в списке."

    channels.remove(channel_id)
    with open(channels_file, 'w') as file:
        for ch in channels:
            file.write(f"{ch}\n")
    return f"Канал {channel_id} успешно удален."


async def main():
    session = 'dont_delete_me'
    client = TelegramClient(session, api_id, api_hash)

    await client.start()

    channel_source = await load_channels()

    @client.on(events.NewMessage(chats=channel_source))
    async def handler(event):
        await client.forward_messages(target_channel, event.message)

    @client.on(events.NewMessage(from_users=admin_user_id))
    async def admin_handler(event):
        message = event.message.message
        if message.startswith('/add '):
            channel_id = message.split(' ', 1)[1]
            response = await add_channel(channel_id)
            await event.reply(response)
        elif message.startswith('/remove '):
            channel_id = message.split(' ', 1)[1]
            response = await remove_channel(channel_id)
            await event.reply(response)
        elif message == '/list':
            channels = await load_channels()
            response = "Текущие каналы:\n" + "\n".join(map(str, channels))
            await event.reply(response)
        else:
            await event.reply("Неизвестная команда. Доступные команды:\n/add <channel_id>\n/remove <channel_id>\n/list")

    print('Процесс запущен')
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
