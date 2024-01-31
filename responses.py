# responses.py

import discord
import random


# handle_responses függvény
def handle_responses(message, ctx) -> str:
    p_message = message.lower()

    if p_message == 'hello':
        return 'Hello!'

    if p_message == 'roll':
        return str(random.randint(1, 6))

    if p_message == 'asd':
        return "`Ez egy segítség amit tudsz változtatni.`"

    if p_message == 'help':
        return help_response(ctx)


def help_response(ctx):
    emlites = ctx.author.mention

    embed = discord.Embed(
        title="Inventory Kommandjai",
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        description=f"Köszönj nekem, {emlites}! :sunglasses:",
    )

    # Interaktok
    embed.add_field(
        name=":lips:  **Interaktok**",
        value="`hello`",
        inline=False
    )

    # Játékok
    embed.add_field(
        name=":video_game:  **Játékok**",
        value="`roll`",
        inline=False
    )

    # Egyebek
    embed.add_field(
        name=":space_invader:  **Egyebek**",
        value="`asd`",
        inline=False
    )

    embed.set_footer(
        text="Ha bármi gond van, csak szólj az Adminnak: \n"
             "[Stoic mindset#0088]"
    )

    return embed
