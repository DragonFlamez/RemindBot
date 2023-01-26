import discord
import asyncio
import token

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

reminders = {}

@client.event
async def on_message(message):
    if message.content.startswith('!remind'):
        # Split message into command and reminder
        _, reminder = message.content.split(' ', 1)

        # Get user who sent message
        user = message.author

        # Get current time and reminder time
        now = message.created_at
        reminder_time = now + datetime.timedelta(minutes=5)

        # Add reminder to dictionary with user ID as key
        reminders[user.id] = reminder_time

        # Send confirmation message
        await message.channel.send(f'Reminder set for {reminder_time}')

async def check_reminders():
    await client.wait_until_ready()
    while not client.is_closed():
        now = datetime.datetime.now()
        for user_id, reminder_time in reminders.items():
            if now >= reminder_time:
                user = client.get_user(user_id)
                await user.send(f'Reminder: {reminders[user_id]}')
                del reminders[user_id]
        await asyncio.sleep(60)

client.loop.create_task(check_reminders())
client.run(token.TOKEN)
