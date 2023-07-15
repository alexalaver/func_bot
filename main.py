from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
import config as cfg
import logging


logging.basicConfig(level=logging.INFO)


bot = Bot(cfg.token)
dp = Dispatcher(bot)

PRICE = types.LabeledPrice(label="Подписка на месяц", amount=500*100)

@dp.message_handler(commands=['buy'])
async def buy(message: types.Message):
    if cfg.payments_token.split(':') == 'TEST':
        await message.answer("Тестовый платёж")


    await bot.send_invoice(message.chat.id,
                           title="Подписка на бота",
                           description="Активация подписки на бота на 1 месяц!",
                           provider_token=cfg.payments_token,
                           currency='rub',
                           photo_url="https://cdn.xxl.thumbs.canstockphoto.ru/%D0%BE%D0%BF%D0%BB%D0%B0%D1%82%D0%B0-%D0%BA%D0%B0%D1%80%D1%82%D0%B0-%D1%81%D1%82%D0%BE%D0%BA%D0%BE%D0%B2%D0%B0%D1%8F-%D1%84%D0%BE%D1%82%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F_csp5148789.jpg",
                           photo_width=360,
                           photo_height=254,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter='one-month-subscription',
                           payload='test-invoice-payload')

@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id, f"Платёж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошёл успешно!!!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
