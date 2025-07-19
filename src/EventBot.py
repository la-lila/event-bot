import discord

class MyClient(discord.Client):
  async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))

  # ON EVENT CREATION
  async def on_scheduled_event_create(self, event):
    print(f'Event created: {event.name} in guild: {event.guild.name}!')
    guild = event.guild
    print(f'Guild: {guild.name}!')

    event_name = event.name
    creator = guild.get_member(event.creator_id)
    print(f'Creator id: {creator}!')

    # Create roles
    leader_role = await guild.create_role(name=_leader_role_name(event_name))
    team_role = await guild.create_role(name=_team_role_name(event_name))

    # Create category with restricted visibility for @everyone
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),  # Deny read access for @everyone
        team_role: discord.PermissionOverwrite(send_messages=False, read_messages=True),  # Allow read access for the team role
        leader_role: discord.PermissionOverwrite(read_messages=True, manage_channels=True, manage_messages=True)  # Allow manage permissions for the leader role
    }
    category = await guild.create_category(name=_category_name(event_name), overwrites=overwrites)
    channel = await guild.create_text_channel(name=_channel_name(event_name), category=category)

    # Assign leader role to the user who created the event
    await creator.add_roles(leader_role)
    print(f'Role "{leader_role.name}" assigned to {creator.name} for event "{event_name}".')

    # Change location to channel link
    link = channel.jump_url
    print(f'Channel url: "{link}".')
    await event.edit(location=link)





  # ON EVENT DELETE
  async def on_scheduled_event_delete(self, event):
    guild = event.guild
    event_name = event.name

    # Trouver/supprimer le rôle de Leader
    leader_role_name = _leader_role_name(event_name)
    leader_role = discord.utils.get(guild.roles, name=leader_role_name)

    if leader_role:
        await leader_role.delete()
        print(f'Role "{leader_role_name}" deleted successfully.')
    else:
        print(f'Role "{leader_role_name}" not found.')

    # Trouver/supprimer le rôle de Team
    team_role_name = _team_role_name(event_name)
    team_role = discord.utils.get(guild.roles, name=team_role_name)

    if team_role:
        await team_role.delete()
        print(f'Role "{team_role_name}" deleted successfully.')
    else:
        print(f'Role "{team_role_name}" not found.')

    # Supprimer la catégorie et le channel
    category_name = _category_name(event_name)
    category = discord.utils.get(guild.categories, name=category_name)
    if category:
        for channel in category.channels:
            await channel.delete()
            print(f'Channel "{channel.name}" deleted successfully.')
        await category.delete()
        print(f'Category "{category_name}" deleted successfully.')
    else:
        print(f'Category "{category_name}" not found.')




  # ON EVENT USER ADD
  async def on_scheduled_event_user_add(self, event, user):
    guild = event.guild
    event_name = event.name

    # Vérifiez si le rôle pour l'événement existe déjà
    team_role_name = _team_role_name(event_name)
    team_role = discord.utils.get(guild.roles, name=team_role_name)

    # Si le rôle n'existe pas, créez-le
    if not team_role:
        team_role = await guild.create_role(name=team_role_name)

    # Ajoutez le rôle à l'utilisateur
    member = guild.get_member(user.id)
    if member:
        await member.add_roles(team_role)
        print(f'Role "{team_role.name}" assigned to {member.name} for event "{event_name}".')
    else:
        print(f'Member with ID {user.id} not found in the guild.')



  # ON EVENT USER REMOVE
  async def on_scheduled_event_user_remove(self, event, user):
    guild = event.guild
    event_name = event.name

    # Vérifiez si le rôle pour l'événement existe déjà
    team_role_name = _team_role_name(event_name)
    team_role = discord.utils.get(guild.roles, name=team_role_name)

    if team_role:
      # Retirer le rôle à l'utilisateur
      member = guild.get_member(user.id)
      if member:
          await member.remove_roles(team_role)
          print(f'Role "{team_role.name}" removed from {member.name} for event "{event_name}".')
      else:
          print(f'Member with ID {user.id} not found in the guild.')



def _leader_role_name(event_name):
  return f"Jour J : {event_name}"
def _team_role_name(event_name):
  return f"Staff : {event_name}"
def _category_name(event_name):
  return f"{event_name.title()}"
def _channel_name(event_name):
  return f"discussions-{event_name}"







intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_scheduled_events = True
intents.members = True

client = MyClient(intents=intents)
client.run('MTM0OTQwNDIxODE0MTcwNDI1NQ.GoJO9G.5RcXyMau3td7NJi0BTxzfHcWMblwU4vmmgdWyk')