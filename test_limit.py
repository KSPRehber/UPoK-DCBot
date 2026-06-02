from discord import app_commands
grp = app_commands.Group(name="test", description="test")
print(hasattr(grp, 'commands'))
print(grp.commands)
