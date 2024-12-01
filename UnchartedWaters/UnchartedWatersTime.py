# UnchartedWatersTime.py
from datetime import datetime
import asyncio
import SheetManager

#https://developers.google.com/sheets/api/quickstart/python
#https://medium.com/analytics-vidhya/how-to-read-and-write-data-to-google-spreadsheet-using-python-ebf54d51a72c

# UW Time Globals
OPENING = datetime.strptime('10:00', '%H:%M')
WARN_OPEN = datetime.strptime('12:50', '%H:%M')
FIRST = datetime.strptime('13:00', '%H:%M')
WARN_FIRST = datetime.strptime('15:50', '%H:%M')
SECOND = datetime.strptime('16:00', '%H:%M')
WARN_SECOND = datetime.strptime('18:50', '%H:%M')
FINAL = datetime.strptime('19:00', '%H:%M')
WARN_FINAL = datetime.strptime('21:50', '%H:%M')
END = datetime.strptime('22:00', '%H:%M')


# Checks current time, creates/deletes sheets at the beginning of new rounds, warns users 10 minutes prior to the start of a new round
async def TimeCheck(curTime, bot, UNCHARTEDWATERS, UWTIMETRACKER):
    curTime = curTime.time()
    if curTime >= OPENING.time() and curTime < WARN_OPEN.time() and UWTIMETRACKER == 0:
        ActiveGuilds = await getEnabledGuilds(UNCHARTEDWATERS)
        updateTimeTracker = 1
        for guild in ActiveGuilds:
            channel = bot.get_channel(guild[1])
            sheetName, sheetLink = guild[2], guild[3]
            CleanedUp = await SheetManager.SheetCleanup(sheetName, "UW-First Round")
            if CleanedUp:
                await channel.send('Uncharted Waters has opened! Please share screenshots of your buy & sell pages!')
                await channel.send(f'A new spreadsheet "UW-First Round" has been created! {sheetLink}')
        return updateTimeTracker
    elif curTime >= WARN_OPEN.time() and curTime < FIRST.time() and UWTIMETRACKER == 1:
        ActiveGuilds = await getEnabledGuilds(UNCHARTEDWATERS)
        updateTimeTracker = 2
        for guild in ActiveGuilds:
            channel = bot.get_channel(guild[1])
            await channel.send('Attention: 10 minutes remain in this round, sell your items before the ports refresh!')
        return updateTimeTracker
    elif curTime >= FIRST.time() and curTime < WARN_FIRST.time() and UWTIMETRACKER == 2:
        ActiveGuilds = await getEnabledGuilds(UNCHARTEDWATERS)
        updateTimeTracker = 3
        for guild in ActiveGuilds:
            channel = bot.get_channel(guild[1])
            sheetName, sheetLink = guild[2], guild[3]
            CleanedUp = await SheetManager.SheetCleanup(sheetName, "UW-Second Round")
            if CleanedUp:
                await channel.send('The ports have refreshed! Please share screenshots of your buy & sell pages!')
                await channel.send(f'A new spreadsheet "UW-Second Round" has been created! {sheetLink}')
        return updateTimeTracker
    elif curTime >= WARN_FIRST.time() and curTime < SECOND.time() and UWTIMETRACKER == 3:
        ActiveGuilds = await getEnabledGuilds(UNCHARTEDWATERS)
        updateTimeTracker = 4
        for guild in ActiveGuilds:
            channel = bot.get_channel(guild[1])
            await channel.send('Attention: 10 minutes remain in this round, sell your items before the ports refresh!')
        return updateTimeTracker
    elif curTime >= SECOND.time() and curTime < WARN_SECOND.time() and UWTIMETRACKER == 4:
        ActiveGuilds = await getEnabledGuilds(UNCHARTEDWATERS)
        updateTimeTracker = 5
        for guild in ActiveGuilds:
            channel = bot.get_channel(guild[1])
            sheetName, sheetLink = guild[2], guild[3]
            CleanedUp = await SheetManager.SheetCleanup(sheetName, "UW-Third Round")
            if CleanedUp:
                await channel.send('The ports have refreshed! Please share screenshots of your buy & sell pages!')
                await channel.send(f'A new spreadsheet "UW-Third Round" has been created! {sheetLink}')
        return updateTimeTracker
    elif curTime >= WARN_SECOND.time() and curTime < FINAL.time() and UWTIMETRACKER == 5:
        ActiveGuilds = await getEnabledGuilds(UNCHARTEDWATERS)
        updateTimeTracker = 6
        for guild in ActiveGuilds:
            channel = bot.get_channel(guild[1])
            await channel.send('Attention: 10 minutes remain in this round, sell your items before the ports refresh!')
        return updateTimeTracker
    elif curTime >= FINAL.time() and curTime < WARN_FINAL.time() and UWTIMETRACKER == 6:
        ActiveGuilds = await getEnabledGuilds(UNCHARTEDWATERS)
        updateTimeTracker = 7
        for guild in ActiveGuilds:
            channel = bot.get_channel(guild[1])
            sheetName, sheetLink = guild[2], guild[3]
            CleanedUp = await SheetManager.SheetCleanup(sheetName, "UW-Final Round")
            if CleanedUp:
                await channel.send('The ports have refreshed for the **FINAL TIME**! Please share screenshots of your buy & sell pages!')
                await channel.send(f'A new spreadsheet "UW-Final Round" has been created! {sheetLink}')
        return updateTimeTracker
    elif curTime >= WARN_FINAL.time() and curTime < END.time() and UWTIMETRACKER == 7:
        ActiveGuilds = await getEnabledGuilds(UNCHARTEDWATERS)
        updateTimeTracker = 8
        for guild in ActiveGuilds:
            channel = bot.get_channel(guild[1])
            await channel.send('Attention: 10 minutes remain in this round, sell your items before the ports refresh!')
        return updateTimeTracker
    elif curTime >= END.time() and UWTIMETRACKER == 8:
        ActiveGuilds = await getEnabledGuilds(UNCHARTEDWATERS)
        updateTimeTracker = 0
        for guild in ActiveGuilds:
            channel = bot.get_channel(guild[1])
            sheetName = guild[2]
            await SheetManager.DeleteSheets(sheetName)
            await channel.send('Uncharted Waters has closed!')
        return updateTimeTracker
    elif curTime < OPENING.time():
       # print('overhere')
        updateTimeTracker = 0
        return updateTimeTracker
    else:

        return UWTIMETRACKER



async def getEnabledGuilds(list):
    activeguilds = []
    for guild in list:
        if list[guild]["Enabled"] == "True":
            channel = int(list[guild]["Channel"])
            sheetname = list[guild]["SheetName"]
            sheetlink = list[guild]["SheetLink"]
            activeguilds.append((guild, channel, sheetname, sheetlink))
        else:
            pass
    return activeguilds

# Initializes bot with current time & current UW round
async def InitializeUWTimeTracker(curTime):
    curTime = curTime.time()
    if curTime >= OPENING.time() and curTime < WARN_OPEN.time():
        UWTIMETRACKER = 0
        return UWTIMETRACKER
    elif curTime >= WARN_OPEN.time() and curTime < FIRST.time():
        UWTIMETRACKER = 1
        return UWTIMETRACKER
    elif curTime >= FIRST.time() and curTime < WARN_FIRST.time():
        UWTIMETRACKER = 2
        return UWTIMETRACKER
    elif curTime >= WARN_FIRST.time() and curTime < SECOND.time():
        UWTIMETRACKER = 3
        return UWTIMETRACKER
    elif curTime >= SECOND.time() and curTime < WARN_SECOND.time():
        UWTIMETRACKER = 4
        return UWTIMETRACKER
    elif curTime >= WARN_SECOND.time() and curTime < FINAL.time():
        UWTIMETRACKER = 5
        return UWTIMETRACKER
    elif curTime >= FINAL.time() and curTime < WARN_FINAL.time():
        UWTIMETRACKER = 6
        return UWTIMETRACKER
    elif curTime >= WARN_FINAL.time() and curTime < END.time():
        UWTIMETRACKER = 7
        return UWTIMETRACKER
    elif curTime >= END.time():
        UWTIMETRACKER = 0
        return UWTIMETRACKER
    elif curTime < OPENING.time():
        UWTIMETRACKER = 0
        return UWTIMETRACKER