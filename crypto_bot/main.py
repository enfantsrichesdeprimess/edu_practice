import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from web3 import Web3
import requests
from dotenv import load_dotenv

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv('MONAD_RPC_URL')))

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


class SendTokens(StatesGroup):
    receiver_address = State()
    amount = State()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет, это кошелек для удобной работы с токенами в monad.testnet\n\n"
        "Возможности кошелька:\n"
        "/balance - Показать баланс\n"
        "/transactions - Последние транзакции\n"
        "/send - Отправить токены\n"
    )


@dp.message(Command("balance"))
async def cmd_balance(message: types.Message):
    try:
        balance_wei = w3.eth.get_balance(os.getenv('WALLET_ADDRESS'))
        balance_monad = w3.from_wei(balance_wei, 'ether')
        await message.answer(f"Баланс: {balance_monad} MON")
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")


async def get_monad_transactions(address):
    latest_block = w3.eth.block_number
    transactions = []

    for block_num in range(latest_block - 100, latest_block + 1):
        try:
            block = w3.eth.get_block(block_num, full_transactions=True)
            for tx in block.transactions:
                if tx['to'] == address or tx['from'] == address:
                    transactions.append(tx)
        except:
            continue

    return transactions[:10]


@dp.message(Command("transactions"))
async def cmd_transactions(message: types.Message):
    await message.answer("Ожидайте, анализируем блоки...")
    try:
        address = os.getenv('WALLET_ADDRESS')
        transactions = await get_monad_transactions(address)

        if not transactions:
            await message.answer("Нет последних транзакций(среди 100 последних блоков)")
            return

        result = "Последняя транзакция в Monad(среди 100 последних блоков):\n\n"
        for tx in transactions:
            result += f"Хэш: {tx['hash'].hex()}\n"
            result += f"От: {tx['from']}\n"
            result += f"Кому: {tx['to']}\n"
            result += f"Сумма: {w3.from_wei(tx['value'], 'ether')} MON\n\n"

        await message.answer(result)
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")


@dp.message(Command("send"))
async def cmd_send(message: types.Message, state: FSMContext):
    await message.answer("Введите адрес получателя:")
    await state.set_state(SendTokens.receiver_address)


@dp.message(SendTokens.receiver_address)
async def process_receiver(message: types.Message, state: FSMContext):
    if not w3.is_address(message.text):
        await message.answer("Несуществующий адрес, попробуйте снова:")
        return

    await state.update_data(receiver_address=message.text)
    await message.answer("Введите количество MON для отправки:")
    await state.set_state(SendTokens.amount)


@dp.message(SendTokens.amount)
async def process_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        data = await state.get_data()
        receiver = data['receiver_address']

        nonce = w3.eth.get_transaction_count(os.getenv('WALLET_ADDRESS'))
        tx = {
            'nonce': nonce,
            'to': receiver,
            'value': w3.to_wei(amount, 'ether'),
            'gas': 50000,
            'gasPrice': w3.eth.gas_price
        }

        signed_tx = w3.eth.account.sign_transaction(tx, os.getenv('PRIVATE_KEY'))
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        await message.answer(f"Транзакция отправлена!\nХэш: {tx_hash.hex()}")
        await state.clear()
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")
        await state.clear()


async def check_incoming_transactions():
    last_block = w3.eth.block_number
    while True:
        try:
            current_block = w3.eth.block_number
            if current_block > last_block:
                for block_num in range(last_block + 1, current_block + 1):
                    block = w3.eth.get_block(block_num, full_transactions=True)
                    for tx in block.transactions:
                        if tx['to'] and tx['to'].lower() == os.getenv('WALLET_ADDRESS').lower():
                            amount = w3.from_wei(tx['value'], 'ether')
                            await bot.send_message(
                                os.getenv('ADMIN_CHAT_ID'),
                                f"Новое поступление!\n"
                                f"От: {tx['from']}\n"
                                f"Сумма: {amount} MONAD\n"
                                f"Хэш: {tx['hash'].hex()}"
                            )
                last_block = current_block
        except Exception as e:
            print(f"Ошибка при проверке блоков: {str(e)}")
        await asyncio.sleep(10)


async def main():
    await asyncio.gather(
        dp.start_polling(bot),
        check_incoming_transactions()
    )


if __name__ == "__main__":
    asyncio.run(main())