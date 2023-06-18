import discord, discord.ext.tasks, aiohttp, tempfile, asyncio, main

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

async def process(url: str) -> bool:
    with tempfile.NamedTemporaryFile() as temp:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                with open(temp.name, 'wb') as fd:
                    async for chunk in resp.content.iter_chunked(16 * 1024):
                        fd.write(chunk)
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, main.is_flashing, temp.name)

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    for embed in message.embeds:
        if embed.type == "gifv" or embed.type == "image": # gif video trolling
            if await process(embed.thumbnail.proxy_url):
                await message.delete()
                await message.channel.send(f"{str(message.author)}: I think one of your images has flashing sequences.")
            else:
                print("not flashing " + embed.thumbnail.proxy_url)
        else:
            print(embed.type)

client.run('token')
