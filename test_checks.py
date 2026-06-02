import discord
from discord import app_commands
def mod_only():
    async def predicate(interaction: discord.Interaction) -> bool: return True
    return app_commands.check(predicate)

@app_commands.command()
@mod_only()
async def test_cmd(interaction): pass

print(test_cmd.checks)
for check in test_cmd.checks:
    print(check.__qualname__)
