import os

def check_permission(user_id, guild_owner_id=None):
    owner_ids = [int(id.strip()) for id in os.getenv('OWNER_IDS', '').split(',') if id.strip()]
    return user_id in owner_ids or user_id == guild_owner_id

def is_locked_channel(channel_id):
    locked_id = os.getenv('LOCKED_CHANNEL_ID', '')
    if not locked_id:
        return False
    return str(channel_id) != str(locked_id)
