from telethon import TelegramClient, events

api_id = '23963854'
api_hash = 'cfbe95064159720206325bf9a4fabea6'
channel_source = 'https://t.me/shitpostingdao'  # ссылка на канал, откуда берем новости


def telegram_parser(send_message_func=None, loop=None):
    session = 'dont_delete_me'
    client = TelegramClient(session, api_id, api_hash, loop=loop)
    client.start()

    @client.on(events.NewMessage(chats=channel_source))
    async def handler(event):
        if send_message_func is None:
            print(event.raw_text, '\n')
            await client.forward_messages(-1001814043353, event.message)

    return client


if __name__ == "__main__":
    print('Процесс запущен')
    client = telegram_parser()
    client.run_until_disconnected()
