from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Start bot'),
        types.BotCommand('description', 'Description'),
        types.BotCommand('text', 'Input text'),
        types.BotCommand('translate', 'Translating text'),
        types.BotCommand('test', 'Pass the test')
    ])
