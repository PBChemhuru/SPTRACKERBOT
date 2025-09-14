import math
import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from utils import calculate_pb, get_hit_dice
from database import init_db, add_character, get_characters_by_user, update_character, delete_character, get_characters, \
increment_all_current_sp, rest_user, spend_sp,get_current_sp,regain_sp

from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv('token')

keep_alive()

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        init_db()

        try:
            synced = await self.tree.sync()
            print(f'Synced {len(synced)} commands')
        except Exception as e:
            print(f'Error Syncing Commands: {e}')


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)


@client.tree.command(name="add", description="Add character to database")
async def add(interaction: discord.Interaction, charactername: str, character_class: str, level: int):
    try:
        pb = calculate_pb(level)
        hit_dice = get_hit_dice(character_class)
        sp = pb + hit_dice
        user_id = str(interaction.user.id)

        add_character(user_id, charactername, level, sp)

        await interaction.response.send_message(
            f"✅ Character '{charactername}' added!\nClass: {character_class.title()}, Level: {level}, SP: {sp}"
        )
    except ValueError as e:
        await interaction.response.send_message(f" Error: {e}")


@client.tree.command(name="update", description="update character to database")
async def update(interaction: discord.Interaction, charactername: str, newcharactername: str, character_class: str,level: int):
    try:
        pb = calculate_pb(level)
        hit_dice = get_hit_dice(character_class)
        sp = pb + hit_dice
        user_id = str(interaction.user.id)

        update_character(user_id, charactername, newcharactername, level, sp)

        await interaction.response.send_message(
            f"✅ Character '{charactername}' Update!\nClass: {character_class.title()}, Level: {level}, SP: {sp}"
        )
    except ValueError as e:
        await interaction.response.send_message(f" Error: {e}")


@client.tree.command(name="characters", description="list your characters")
async def mychars(interaction: discord.Interaction):
    user = str(interaction.user.id)
    characters = get_characters_by_user(user)
    if not characters:
        await interaction.response.send_message("You have no characters saved.")
        return
    print(f'{characters}')
    msg = "**Your Characters:**\n"
    for row in characters:
        if len(row) == 4:
            name, level, current_sp, max_sp = row
            msg += f" {name} — Level {level}, SP: {current_sp}/{max_sp}\n"

    await interaction.response.send_message(msg)


@client.tree.command(name="delete", description="Delete character to database")
async def delete(interaction: discord.Interaction, charactername: str):
    try:
        user = str(interaction.user.id)
        delete_character(user, charactername)

        await interaction.response.send_message(
            f"✅ Character '{charactername}' deleted!"
        )
    except ValueError as e:
        await interaction.response.send_message(f" Error: {e}")


@client.tree.command(name='end-turn', description='Global SP recovery')
async def endturn(interaction: discord.Interaction, amount:int =1):
    try:
        increment_all_current_sp(amount)
        await interaction.response.send_message(f'All characters restored by {amount} SP (up to their max).')
    except Exception as e:
        await  interaction.response.send_message(f"Error: {e}")


@client.tree.command(name='rest', description="Rest")
async def rest_command(interaction: discord.Interaction):
    try:
        user = (interaction.user.id)
        rest_user(user)
        characters = get_characters()
        msg = "**Your Characters:**\n"
        for row in characters:
            if len(row) == 4:
                name, level, current_sp, max_sp = row
                msg += f" {name} — Level {level}, SP: {current_sp}/{max_sp}\n"

        await interaction.response.send_message(f'Rest Complete,{msg}')
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}")


@client.tree.command(name='spendsp', description="Spend Sp")
async def spendsp(interaction: discord.Interaction, sp: int,character:str):
    try:
        user = (interaction.user.id)
        current_sp = get_current_sp(user, character)

        if current_sp is None:
            return await interaction.response.send_message(f"❌ Character '{character}' not found.")

        if current_sp <= 0:
            return await interaction.response.send_message(f"⚠️ '{character}' is already SP exhausted (0 SP).")

        if current_sp - sp < 0:
            return await interaction.response.send_message(
                f"⚠️ '{character}' does not have enough SP to spend {sp}. Current SP: {current_sp}"
            )

        spend_sp(user, character, sp)

        updated_characters = get_characters_by_user(user)
        msg = "**Your Characters:**\n"
        for name, level, current_sp, max_sp in updated_characters:
            msg += f" {name} — Level {level}, SP: {current_sp}/{max_sp}\n"

        await interaction.response.send_message(f"✅ {sp} SP spent for '{character}'.\n\n{msg}")
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}")

@client.tree.command(name='regain_sp', description="Regain Sp")
async def regain_sp(interaction: discord.Interaction, sp: int,character:str):
    try:
        user = (interaction.user.id)
        current_sp = get_current_sp(user, character)

        if current_sp is None:
            return await interaction.response.send_message(f"❌ Character '{character}' not found.")

        if current_sp <= 0:
            return await interaction.response.send_message(f"⚠️ '{character}' is already SP exhausted (0 SP).")

        if current_sp - sp < 0:
            return await interaction.response.send_message(
                f"⚠️ '{character}' does not have enough SP to spend {sp}. Current SP: {current_sp}"
            )

        spend_sp(user, character, sp)

        updated_characters = get_characters_by_user(user)
        msg = "**Your Characters:**\n"
        for name, level, current_sp, max_sp in updated_characters:
            msg += f" {name} — Level {level}, SP: {current_sp}/{max_sp}\n"

        await interaction.response.send_message(f"✅ {sp} SP spent for '{character}'.\n\n{msg}")
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}")

regain_sp

client.run(TOKEN)
