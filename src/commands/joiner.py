import discord
from discord.ext import commands
from discord import app_commands
import re
import asyncio
import os
from utils.joiner import mass_join
from utils.permissions import check_permission, is_locked_channel

def extract_invite_code(url):
    match = re.search(r'(?:discord\.gg/|discordapp\.com/invite\/)([a-zA-Z0-9-]+)|^([a-zA-Z0-9-]+)$', url)
    return match.group(1) if match and match.group(1) else (match.group(2) if match else None)

class JoinerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='emorce', description='Emorce commands')
    @app_commands.describe(
        action='joiner or start',
        invite='Invite URL or code',
        limit='Max tokens to use',
        delay='Delay ms between joins',
    )
    async def emorce(self, interaction: discord.Interaction, action: str, invite: str, limit: int = None, delay: int = None):
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
        
        if action not in ['joiner', 'start']:
            return await interaction.response.send_message(
                '❌ Use: joiner or start',
                ephemeral=True
            )
        
        invite_code = extract_invite_code(invite.strip())
        if not invite_code:
            return await interaction.response.send_message(
                '❌ Invalid invite URL or code',
                ephemeral=True
            )
        
        tokens = self.bot.token_manager.get_all()
        if not tokens:
            return await interaction.response.send_message(
                '❌ No tokens stored',
                ephemeral=True
            )
        
        if limit:
            tokens = tokens[:limit]
        
        delay_ms = delay if delay else int(__import__('os').getenv('JOIN_DELAY_MS', '800'))
        max_concurrent = int(__import__('os').getenv('MAX_CONCURRENT_JOINS', '5'))
        
        await interaction.response.defer()
        
        embed = discord.Embed(
            title='🔄 Joiner Progress',
            color=0x9B59B6
        )
        embed.add_field(name='Joined', value='0', inline=True)
        embed.add_field(name='Failed', value='0', inline=True)
        embed.add_field(name='Total', value=str(len(tokens)), inline=True)
        embed.add_field(name='Invite', value=f'discord.gg/{invite_code}', inline=False)
        
        msg = await interaction.followup.send(embed=embed)
        
        result = await mass_join(tokens, invite_code, limit=None, delay_ms=delay_ms, max_concurrent=max_concurrent)
        
        final_embed = discord.Embed(
            title='✓ Joiner Complete',
            color=0x2ECC71
        )
        final_embed.add_field(name='Joined', value=str(result['joined']), inline=True)
        final_embed.add_field(name='Failed', value=str(result['failed']), inline=True)
        success_rate = round((result['joined'] / result['total'] * 100)) if result['total'] > 0 else 0
        final_embed.add_field(name='Success Rate', value=f'{success_rate}%', inline=True)
        
        await msg.edit(embed=final_embed)

async def setup(bot):
    await bot.add_cog(JoinerCommands(bot))
