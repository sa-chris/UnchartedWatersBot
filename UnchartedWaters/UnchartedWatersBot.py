# UnchartedWatersBot

import os
from datetime import datetime, date
import re
import discord
from dotenv import load_dotenv  # .env management  # pip install python-dotenv
from discord.ext import commands, tasks  # Discord
import simplejson as json  # pip install simplejson


# UW Margin Calculator
import MarginCalculator

# UW Image Processing
import ImageScraper

# UW Spreadsheet Manager
import SheetManager

# UW Time Keeping
import UnchartedWatersTime

# UW gspread account tracker
ACCOUNT = 'uw-1'

# discord globals
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# global variables
UNCHARTEDWATERS = {}
UNCHARTEDWATERSCHANNELS = [] # managed by LoadServers()
UNCHARTEDWATERSMODE = False  # Will update to True, enabling image processing, when needed
UWTIMETRACKER = ''
ITEMLIST = ['Agate', 'Alcohol', 'Bananas', 'Carpets', 'Cloth', 'Diamonds', 'Dye', 'Firearms', 'Fish', 'Gold',
             'Leather', 'Meat', 'Medicine', 'Paper', 'Peanuts', 'Pearls', 'Porcelain', 'Tea leaves', 'Tin', 'Tobacco']

# global discord user ids, enter as int
MASTER = 123456789 # update with bot owners userid




# Initializes bot
async def InitializeUW():
    global UNCHARTEDWATERSMODE, UWTIMETRACKER
    for guild in UNCHARTEDWATERS:
        if UNCHARTEDWATERS[guild]["Enabled"] == "True":
            UNCHARTEDWATERSMODE = True
    if UNCHARTEDWATERSMODE:
        currentTime = datetime.now()
        UWTIMETRACKER = await UnchartedWatersTime.InitializeUWTimeTracker(currentTime)
        print(f'Initialized with {UWTIMETRACKER}')

@bot.event
async def on_resumed():
    print('Session Resumed')

# Performs time checks every 30 seconds
@tasks.loop(seconds = 30)
async def masterTasks():
    currentTime = datetime.now()
    await checkUnchartedWaters(currentTime)

# Determines if current time is within UW window
async def checkUnchartedWaters(curTime):
    global UWTIMETRACKER
    if UNCHARTEDWATERSMODE:
        # send time to external script
        UWTIMETRACKER = await UnchartedWatersTime.TimeCheck(curTime, bot, UNCHARTEDWATERS, UWTIMETRACKER)
    else:
        pass

# Determines if image is posted, sends image to ImageScraper() to begin OCR
# Will add a green check mark or a red X reaction to the image posted depending on if it was successfully read
@bot.event
async def on_message(message):
    if await UnchartedWatersCheck(message.guild.id, message.channel.id):
        for attachment in message.attachments:
            imagetypes = ["png", "jpeg", "jpg"]
            if any(attachment.filename.lower().endswith(image) for image in imagetypes):
                success, port, portPrices = await ImageScraper.MasterProcess(attachment)
                if success:
                    try:
                        global ACCOUNT
                        sheetName = UNCHARTEDWATERS[str(message.guild.id)]["SheetName"]
                        ACCOUNT = await SheetManager.MasterProcess(sheetName, port, portPrices, ACCOUNT)
                        await message.add_reaction('\N{White Heavy Check Mark}')
                        if message.channel.id == 1014760906699309107 or message.channel.id == 975780762546753627:
                            await message.channel.send(port)
                    except Exception as err:
                        print(f"Error: Exception {err} during SheetManager.MasterProcess, Port = {port}")
                        await message.add_reaction('\N{Cross Mark}')
                else:
                    await message.add_reaction('\N{Cross Mark}')
                itemIndex = 0
                for price in portPrices:
                    try:
                        if '*' in price:
                            price = price[4:]
                    except:
                        pass
                    if price == 'X':
                        itemIndex = itemIndex + 1
                        continue
                    elif int(price) >= 111 or int(price) <= 80:
                        item = ITEMLIST[itemIndex]
                        await message.channel.send(f"Pricing Error: Price is invalid, please double check and correct the price of **{item}** at **{port}**. Incorrect price = **{price}**")
                    else:
                        pass
                    itemIndex = itemIndex + 1
    await bot.process_commands(message)  ## to process if any commands are sent

# Checks to see if discord server is allowed to run bot
async def UnchartedWatersCheck(guild, channel):
    guild, channel = str(guild), str(channel)
    try:
        if UNCHARTEDWATERS[guild]["Enabled"] == "True" and UNCHARTEDWATERS[guild]["Channel"] == channel:
            return True
        else:
            return False
    except KeyError:
        print(f"Key Error {guild} or {channel} not found in SERVERS.json")
        return False

# Load list of servers from SERVERS.json
async def LoadServers():
    global UNCHARTEDWATERS, UNCHARTEDWATERSCHANNELS
    with open("SERVERS.json", 'r') as file:
        modes_data = json.load(file)
        temp = modes_data['Uncharted Waters']
        for server in temp:
            serverID = re.sub(r'[^0-9]', '', server)
            boolean = modes_data['Uncharted Waters'][serverID]["Enabled"]
            channel = modes_data['Uncharted Waters'][serverID]["Channel"]
            UNCHARTEDWATERSCHANNELS.append(int(channel))
            sheetName = modes_data['Uncharted Waters'][serverID]["SheetName"]
            sheetLink = modes_data['Uncharted Waters'][serverID]["SheetLink"]
            UNCHARTEDWATERS.update({f"{serverID}": {"Enabled": f"{boolean}", "Channel": f"{channel}", "SheetName":f"{sheetName}", "SheetLink": f"{sheetLink}"}})
        file.close()
    print('Servers Loaded!')

# allows bot to update list of servers while running if commanded by bot owner
@bot.command(name='updatemodes')
async def UpdateModes(ctx):
    if ctx.author.id == MASTER:
        await LoadServers()
    else:
        ctx.reply("You are not authorized for this.")

# Allows bot to startup if previously disabled
@bot.command(name='uw.start')
async def StartUW(ctx):
    global UNCHARTEDWATERSMODE
    try:
        if ctx.channel.id in UNCHARTEDWATERSCHANNELS:
            with open("Modes/Modes.json", 'r+') as file:
                modes_data = json.load(file)
                toggle = modes_data['Uncharted Waters'][str(ctx.guild.id)]["Enabled"]
                if toggle == 'False': # if waters disabled, will enable
                    modes_data['Uncharted Waters'][str(ctx.guild.id)]["Enabled"] = 'True'
                    await ctx.reply('Uncharted Waters has been enabled!')
                    file.seek(0)
                    json.dump(modes_data, file, indent=8)
                    file.truncate()
                    if not UNCHARTEDWATERSMODE:
                        UNCHARTEDWATERSMODE = True
                        await InitializeUW()
    except KeyError:
        await ctx.reply("Error: This server is not authorized to use this bot.")
        pass



# Performs calculation on spreadsheet to determine the top 5 highest profit margins currently, posts to channel
@bot.command(name='calc')
async def calcMargins(ctx):
    sheetName, guild = UNCHARTEDWATERS[str(ctx.guild.id)]["SheetName"], str(ctx.guild.id)
    try:
        sheetName = UNCHARTEDWATERS[guild]["SheetName"]
    except:
        print('Experienced an unknown error during !calc')
    result = MarginCalculator.MarginCalculator(sheetName)
    await ctx.reply(result[0])
    await ctx.send(result[1])
    await ctx.send(result[2])
    await ctx.send(result[3])
    await ctx.send(result[4])


# Main
@bot.event
async def on_ready():
    await LoadServers()
    await InitializeUW()
    if not masterTasks.is_running():
        masterTasks.start()
        print('Tasks Started!')
    print(f'{bot.user} has connected to Discord!')

if __name__ == '__main__':
    bot.run(TOKEN)