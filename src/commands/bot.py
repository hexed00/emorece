import discord
from discord.ext import commands
from discord import app_commands
import os
from utils.permissions import check_permission, is_locked_channel

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='bot', description='Bot customization')
    @app_commands.describe(
        action='image, banner, or status',
        type='Activity type (for status)',
        text='Activity text (for status)',
        image='Image file (for image or banner)',
    )
    async def customize(self, interaction: discord.Interaction, action: str, type: str = None, text: str = None, image: discord.Attachment = None):
        locked_id = os.getenv('LOCKED_CHANNEL_ID', '')
        if locked_id and is_locked_channel(interaction.channel_id):
            return await interaction.response.send_message(
                f'❌ This command only works in <#{locked_id}>',
                ephemeral=True
            )
        
        if not check_permission(interaction.user.id, interaction.guild.owner_id if interaction.guild else None):
            return await interaction.response.send_message(
                '❌ Only bot owners or server owners can use this command.',
                ephemeral=True
            )
        
        action = action.lower().strip()
        
        if action == 'image':
            if not image:
                return await interaction.response.send_message(
                    '❌ Attach an image file',
                    ephemeral=True
                )
            
            try:
                avatar_data = await image.read()
                await self.bot.user.edit(avatar=avatar_data)
                await interaction.response.send_message(
                    '✓ Avatar updated',
                    ephemeral=True
                )
            except Exception as e:
                await interaction.response.send_message(
                    f'❌ {str(e)}',
                    ephemeral=True
                )
        
        elif action == 'banner':
            if not image:
                return await interaction.response.send_message(
                    '❌ Attach an image file',
                    ephemeral=True
                )
            
            try:
                banner_data = await image.read()
                await self.bot.user.edit(banner=banner_data)
                await interaction.response.send_message(
                    '✓ Banner updated',
                    ephemeral=True
                )
            except Exception as e:
                await interaction.response.send_message(
                    f'❌ {str(e)}',
                    ephemeral=True
                )
        
        elif action == 'status':
            if not type or not text:
                return await interaction.response.send_message(
                    '❌ Provide type and text',
                    ephemeral=True
                )
            
            try:
                type_map = {
                    'playing': discord.ActivityType.playing,
                    'watching': discord.ActivityType.watching,
                    'listening': discord.ActivityType.listening,
                    'competing': discord.ActivityType.competing,
                }
                
                activity_type = type_map.get(type.lower(), discord.ActivityType.watching)
                activity = discord.Activity(type=activity_type, name=text)
                await self.bot.change_presence(activity=activity)
                await interaction.response.send_message(
                    f'✓ Status set to "{text}"',
                    ephemeral=True
                )
            except Exception as e:
                await interaction.response.send_message(
                    f'❌ {str(e)}',
                    ephemeral=True
                )
        
        else:
            await interaction.response.send_message(
                '❌ Use: image, banner, or status',
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(BotCommands(bot))
