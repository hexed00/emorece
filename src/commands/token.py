import discord
from discord.ext import commands
from discord import app_commands
import io
import os
from utils.permissions import check_permission, is_locked_channel

class TokenCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='token', description='Token management')
    @app_commands.describe(
        action='log, count, preview, clear, or output',
        tokens='Paste tokens here (for log)',
        file='Upload .txt file with tokens',
    )
    async def token(self, interaction: discord.Interaction, action: str, tokens: str = None, file: discord.Attachment = None):
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
        
        if action == 'log':
            if not tokens and not file:
                return await interaction.response.send_message(
                    '❌ Provide tokens or attach .txt file',
                    ephemeral=True
                )
            
            if file:
                if not file.filename.endswith('.txt'):
                    return await interaction.response.send_message(
                        '❌ File must be .txt',
                        ephemeral=True
                    )
                
                try:
                    content = await file.read()
                    tokens_list = content.decode('utf-8').split('\n')
                except:
                    return await interaction.response.send_message(
                        '❌ Could not read file',
                        ephemeral=True
                    )
            else:
                tokens_list = tokens.split('\n')
            
            count = self.bot.token_manager.add(tokens_list)
            await interaction.response.send_message(
                f'✓ Added {count} tokens\nTotal: {self.bot.token_manager.get_count()}',
                ephemeral=True
            )
        
        elif action == 'count':
            count = self.bot.token_manager.get_count()
            await interaction.response.send_message(
                f'📊 Token count: **{count}**',
                ephemeral=True
            )
        
        elif action == 'preview':
            preview = self.bot.token_manager.get_preview(10)
            text = '\n'.join(preview) if preview else '_No tokens_'
            await interaction.response.send_message(
                f'**Preview (first 10):**\n```\n{text}\n```',
                ephemeral=True
            )
        
        elif action == 'clear':
            self.bot.token_manager.clear()
            await interaction.response.send_message(
                '✓ All tokens cleared',
                ephemeral=True
            )
        
        elif action == 'output':
            data = self.bot.token_manager.export()
            file = discord.File(io.BytesIO(data), filename='tokens.txt')
            await interaction.response.send_message(
                'Here are your tokens:',
                file=file,
                ephemeral=True
            )
        
        else:
            await interaction.response.send_message(
                '❌ Use: log, count, preview, clear, or output',
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(TokenCommands(bot))
