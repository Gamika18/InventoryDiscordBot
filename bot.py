import discord
import responses
from discord.ext import commands
from config import BOT_TOKEN
from logger import setup_logger
from models import userModel
from colorama import init, Fore

init(autoreset=True)

logger = setup_logger()


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_responses(user_message, message)
        if isinstance(response, discord.Embed):
            await message.reply(embed=response)
        else:
            await message.reply(response) if is_private else await message.reply(response)

        logger.info(
            f"Sikeres válasz érkezett a(z) '{user_message}' üzenetre a következőtől: '{message.author}' (ID: '{message.author.id}') a '{message.channel}' csatornán")
        logger.info(f"A bot válasza: '{response}'")
    except discord.errors.HTTPException as http_exception:
        if http_exception.status == 400:
            logger.error(
                f"Érvénytelen bevitel: 400 Bad Request (error code: 50006); Ismeretlen bevitel: '{user_message}'; a következőtől: '{message.author}' (ID: {message.author.id})")
            print(
                f"Nem értelmezhető az input: \n{Fore.RED}{'400 Bad Request (error code: 50006): '}\n{'Ismeretlen bemenet:'}{Fore.RESET}\n{Fore.RED}'{Fore.RESET}{user_message}{Fore.RED}'{Fore.RESET}\n")
        else:
            logger.error(f"Error handling message: {http_exception} from {message.author} (ID: {message.author.id})")
            print(f"Hiba az üzenet kezelése során: {Fore.RED}{http_exception}{Fore.RESET}\n")


def run_discord_bot():
    client = commands.Bot(command_prefix='>', intents=discord.Intents.all())

    @client.event
    async def on_ready():
        logger.info(f'{client.user} csatlakozott a Discordhoz!')
        print(f'{Fore.GREEN}{client.user} csatlakozott a Discordhoz!{Fore.RESET}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        logger.info(f"'{username}' mondja: '{user_message}' (ID: {message.author.id}, {channel})")

        conn = userModel.create_connection()

        try:
            # Ha a felhasználó még nem létezik az adatbázisban, akkor adjuk hozzá
            if not userModel.user_exists(conn, message.author.id):
                userModel.create_user(conn, username, message.author.id, message.channel.id)
                user_data = userModel.fetch_user(conn, message.author.id)
                logger.info(user_data)
                logger.info(f"Lekért felhasználói adatok: {user_data}")
        except Exception as exeption:
            logger.error(f"Hiba az adatbázissal való interakció közben: {exeption}")
        finally:
            conn.close()

        if user_message and user_message[0] == '?':
            user_message = user_message[1:]
            response = responses.handle_responses(user_message, message)
            await message.channel.send(response)
        else:
            await send_message(message, user_message, is_private=False)

    @client.event
    async def on_disconnect():
        logger.warning('A bot lekapcsolódott.')

    @client.event
    async def on_shard_disconnect():
        logger.warning('A bot egy shardja lekapcsolódott.')

    @client.event
    async def on_error(event, *args, **kwargs):
        logger.error(f'Hiba történt az esemény kezelése során: {event}', exc_info=True)

    client.run(BOT_TOKEN)


if __name__ == "__main__":
    run_discord_bot()
