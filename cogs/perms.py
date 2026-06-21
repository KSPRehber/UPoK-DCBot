"""
cogs/perms.py – Permission helpers that are mimic-safe.

The admin "mimic" system (see bot.py) swaps `interaction.user` to the mimicked
target *before* command/view checks run. If a permission check reads the swapped
`interaction.user`, an admin who mimics a higher-privileged user (e.g. the bot
owner) would borrow that user's authority — a privilege escalation.

`real_user()` unwraps that swap: permission checks MUST gate on the *real*
invoker, so mimic only changes business-logic identity, never the authority a
command is gated on. The real user is stashed by the mimic patch in
`interaction.extras["_mimic_real_user"]`.
"""

import discord

from config import cfg


def real_user(interaction: discord.Interaction):
    """The real invoker, unwrapping any mimic swap. Use this in every permission
    check (never the raw interaction.user, which may be a mimic target)."""
    extras = getattr(interaction, "extras", None) or {}
    return extras.get("_mimic_real_user") or interaction.user


def is_owner_user(interaction: discord.Interaction) -> bool:
    """True if the real invoker is the configured bot owner."""
    return getattr(real_user(interaction), "id", None) == cfg.OWNER_ID


def is_admin_user(interaction: discord.Interaction) -> bool:
    """True if the real invoker is the bot owner or a guild administrator."""
    u = real_user(interaction)
    if getattr(u, "id", None) == cfg.OWNER_ID:
        return True
    return isinstance(u, discord.Member) and u.guild_permissions.administrator


def is_mod_user(interaction: discord.Interaction) -> bool:
    """True if the real invoker is a moderator (MOD_ROLE_ID, kick, or admin)."""
    import settings
    u = real_user(interaction)
    if not isinstance(u, discord.Member):
        return False
    if settings.MOD_ROLE_ID and u.get_role(settings.MOD_ROLE_ID):
        return True
    return u.guild_permissions.kick_members or u.guild_permissions.administrator
