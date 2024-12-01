# Import required modules
import gspread
import gspread_dataframe
import pandas as pd
from time import sleep
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import simplejson as json
import re
import asyncio
from datetime import datetime
import os


# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# pip install gspread
# pip install oauth2client

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Assign credentials ann path of style sheet

#account = 'uw-1'
#creds = ServiceAccountCredentials.from_json_keyfile_name("creds_uw_1.json", scope)
#client = gspread.authorize(creds)
#test = gspread.spreadsheet.Spreadsheet

###############################
#                             #
#     ABOVE IS NECESSARY      #
#                             #
###############################



def fswitchAccounts():
    global creds, account, client
    if account == 'uw-1':
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds_uw_2.json", scope)
        client = gspread.authorize(creds)
        account = 'uw-2'
        print('Successfully switched to account uw-2!')
    elif account == 'uw-2':
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds_uw_3.json", scope)
        client = gspread.authorize(creds)
        account = 'uw-3'
        print('Successfully switched to account uw-3!')
    elif account == 'uw-3':
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds_uw_4.json", scope)
        client = gspread.authorize(creds)
        account = 'uw-4'
        print('Successfully switched to account uw-1!')
    elif account == 'uw-4':
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds_uw_1.json", scope)
        client = gspread.authorize(creds)
        account = 'uw-1'
        print('Successfully switched to account uw-1!')



USERDICT = {} # holds the dictionary list of serverIDs and their sheet name, loaded from JSON

def dupSheet(refresh, guild):
    updateDict()
    sheetName = USERDICT[str(guild)]
    sheet = client.open(sheetName)
    duplicated = False
    try:
        if refresh == 0: # event opening
            sheet.duplicate_sheet(source_sheet_id=sheet.worksheet("Master Copy").id, new_sheet_name='UW-Opening')
            duplicated = True
        elif refresh == 1: # first refresh
            sheet.duplicate_sheet(source_sheet_id=sheet.worksheet("Master Copy").id, new_sheet_name='UW-First Refresh')
            duplicated = True
        elif refresh == 2: # second refresh
            sheet.duplicate_sheet(source_sheet_id=sheet.worksheet("Master Copy").id, new_sheet_name='UW-Second Refresh')
            duplicated = True
        elif refresh == 3: # final refresh
            sheet.duplicate_sheet(source_sheet_id=sheet.worksheet("Master Copy").id, new_sheet_name='UW-Final Refresh')
            duplicated = True
    except:
        pass
    finally:
        return(duplicated)


def delSheet(refresh, guild):
    updateDict()
    sheetName = USERDICT[str(guild)]
    sheet = client.open(sheetName)
    deleted = False
    try:
        if refresh == 0: # event opening
            sheet.del_worksheet(sheet.worksheet("UW-Opening"))
            deleted = True
        elif refresh == 1:  # first refresh
            sheet.del_worksheet(sheet.worksheet("UW-First Refresh"))
            deleted = True
        elif refresh == 2:  # second refresh
            sheet.del_worksheet(sheet.worksheet("UW-Second Refresh"))
            deleted = True
        elif refresh == 3:  # final refresh
            sheet.del_worksheet(sheet.worksheet("UW-Final Refresh"))
            deleted = True
    except:
        pass
    finally:
        return(deleted)

def updateDict():
    global USERDICT
    with open("Modes/Modes.json", 'r') as file:
        modes_data = json.load(file)
        temp = modes_data['Uncharted Waters']
        for server in temp:
            serverID = re.sub(r'[^0-9]', '', server)
            sheetName = modes_data['Uncharted Waters'][serverID]["SheetName"]
            USERDICT.update({f"{serverID}": f"{sheetName}"})
        file.close()


oldPORTDICT = {
    "BuenosAires":4,  # D
    "RiodeJaneiro":5, # E
    "Cayenne":6,      # F
    "PanamaCity":7,
    "SantoDomingo":8,
    "Jamaica":9,
    "Nassau":10,
    "Boston":11,      # K
    ############
    "CapeTown":14,    # N
    "Luanda":15,
    "StGeorges":16,
    "LasPalmas":17,
    "Tunis":18,
    "Alexandria":19,
    "Mozambique":20,  # T
    ############
    "Stockholm":23,   # W
    "Copenhagen":24,
    "Hamburg":25,
    "Amsterdam":26,   # Z
    "London":27,
    "Nantes":28,
    "Lisbon":29,
    "Seville":30,
    "Marseille":31,
    "Venice":32,
    "Athens":33,
    "Istanbul":34,    # AH
    ############
    "Hangzhou":37,    # AK
    "Quanzhou":38,
    "Edo":39,
    "Manila":40,
    "Kolkata":41,
    "Calicut":42,
    "Basrah":43,
    "Aden":44,
    "Ceylon":45,
    "Brunei":46,
    "Malacca":47,
    "Pinjarra":48,
    "Darwin":49      # AW
}


#=AND($A:AW >90, $A:AW <95, SEARCH("*"))

def OldWrite(guild,portName,portPrices):
    print(portPrices)
    updateDict()
    sheetName = USERDICT[str(guild)]
    sheet = client.open(sheetName)
    worksheet = sheet.get_worksheet(0)
    port = portName
    prices = portPrices
    col = PORTDICT[port]
    for item in prices:
        price = prices[item]
        row = ITEMDICT[item]
        print(guild, port, item, price)
        #while True:
        #    try:
        curVal = worksheet.cell(row, col).value
        if curVal == None or '*' in curVal:
            worksheet.update_cell(row, col, price)
        #        break
        #    except Exception:
        #        print('Rate limit reached, switching accounts')
        #        switchAccounts()
                #print('Rate limit reached, sleeping...')
                #sleep(15)

def Write(guild,portName,portPrices):
    updateDict()
    sheetName = USERDICT[str(guild)]
    sheet = client.open(sheetName)
    worksheet = sheet.get_worksheet(0)
    port = portName
    prices = portPrices
    col = PORTDICT[port]
    for item in prices:
        price = prices[item]
        row = ITEMDICT[item]
        #print(guild, port, item, price)
        #while True:
        #    try:
        curVal = worksheet.cell(row, col).value
        if curVal == None or '*' in curVal:
            worksheet.update_cell(row, col, price)
        #        break
        #    except Exception:
        #        print('Rate limit reached, switching accounts')
        #        switchAccounts()
                #print('Rate limit reached, sleeping...')
                #sleep(15)
##########################

# gspread client account info
creds = ServiceAccountCredentials.from_json_keyfile_name("creds_uw_1.json", scope)
client = gspread.authorize(creds)
account = 'uw-1'

# adjusts port name received from image scraping to reflect name on sheet
PORTTRANSLATION = {
    "buenosaires":"Buenos Aires",
    "riodejaneiro":"Rio de Janeiro",
    "cayenne":"Cayenne",
    "panamacity":"Panama City",
    "santodomingo":"Santo Domingo",
    "jamaica":"Jamaica",
    "nassau":"Nassau",
    "boston":"Boston",
    ############
    "capetown":"Cape Town",
    "luanda":"Luanda",
    "stgeorges":"St Georges",
    "St Georges":"St Georges",
    "laspalmas":"Las Palmas",
    "tunis":"Tunis",
    "alexandria":"Alexandria",
    "mozambique":"Mozambique",
    ############
    "stockholm":"Stockholm",
    "copenhagen":"Copenhagen",
    "hamburg":"Hamburg",
    "amsterdam":"Amsterdam",
    "london":"London",
    "nantes":"Nantes",
    "lisbon":"Lisbon",
    "seville":"Seville",
    "marseille":"Marseille",
    "venice":"Venice",
    "athens":"Athens",
    "istanbul":"Istanbul",
    ############
    "hangzhou":"Hangzhou",
    "quanzhou":"Quanzhou",
    "edo":"Edo",
    "manila":"Manila",
    "kolkata":"Kolkata",
    "calicut":"Calicut",
    "basrah":"Basrah",
    "aden":"Aden",
    "ceylon":"Ceylon",
    "brunei":"Brunei",
    "Brunei":"Brunei",
    "malacca":"Malacca",
    "pinjarra":"Pinjarra",
    "darwin":"Darwin"
}

# Dictonary of ports and their respective column on the sheet
PORTDICT = {
    "Buenos Aires":4,  # D
    "Rio de Janeiro":5, # E
    "Cayenne":6,      # F
    "Panama City":7,
    "Santo Domingo":8,
    "Jamaica":9,
    "Nassau":10,
    "Boston":11,      # K
    ############
    "Cape Town":14,    # N
    "Luanda":15,
    "St Georges":16,
    "Las Palmas":17,
    "Tunis":18,
    "Alexandria":19,
    "Mozambique":20,  # T
    ############
    "Stockholm":23,   # W
    "Copenhagen":24,
    "Hamburg":25,
    "Amsterdam":26,   # Z
    "London":27,
    "Nantes":28,
    "Lisbon":29,
    "Seville":30,
    "Marseille":31,
    "Venice":32,
    "Athens":33,
    "Istanbul":34,    # AH
    ############
    "Hangzhou":37,    # AK
    "Quanzhou":38,
    "Edo":39,
    "Manila":40,
    "Kolkata":41,
    "Calicut":42,
    "Basrah":43,
    "Aden":44,
    "Ceylon":45,
    "Brunei":46,
    "Malacca":47,
    "Pinjarra":48,
    "Darwin":49      # AW
}


# Dictionary of items and their respective row on the sheet
ITEMDICT = {
    0: 2,  # Agate
    1: 3,  # Alcohol
    2: 4,  # Bananas
    3: 5,  # Carpets
    4: 6,  # Cloth
    5: 7,  # Diamonds
    6: 8,  # Dye
    7: 9,  # Firearms
    8: 10,  # Fish
    9: 11,  # Gold
    10: 12,  # Leather
    11: 13,  # Meat
    12: 14,  # Medicine
    13: 15,  # Paper
    14: 16,  # Peanuts
    15: 17,  # Pearls
    16: 18,  # Porcelain
    17: 19,  # Tea Leaves
    18: 20,  # Tin
    19: 21  # Tobacco
}

async def GetWorksheet(sheetName):
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds_uw_1.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheetName)
    return sheet.get_worksheet(0)

async def GetDataFrame(worksheet, port):
    currentSheet = gspread_dataframe.get_as_dataframe(worksheet)
    return currentSheet[port]

async def CompareData(worksheet, port, portdata, prices):
    x = 0
    col = PORTDICT[port]
    for rowValue in portdata:
        if isinstance(rowValue, int):
            # does not continue if value is an int
            pass
        else:
            if '*' in str(rowValue) and '*' in str(prices[x]):
                # if both sheet data and price data are a sell price, continue
                pass
            elif 'X' in str(prices[x]) or '.' in str(rowValue):
                # if price does not exist or sheet data contains a float, ignore
                pass
            else:
                row = ITEMDICT[x]
                await SheetUpdate(worksheet, row, col, prices[x])
                #worksheet.update_cell(row, col, prices[x])
        x = x + 1

# Updates spreadsheet at specified row/col
async def SheetUpdate(worksheet, row, col, price):
    done, error, DoubleError = False, 0, False
    while not done:
        try:
            worksheet.update_cell(row, col, price)
            done = True
        except Exception as err:
            if error >= 10:
                if DoubleError:
                    raise ()
                error = 0
                DoubleError = True
                await asyncio.sleep(15)
            else:
                print(f"Exception {err} during SheetManager.SheetUpdate")
                await switchAccounts()
                error = error + 1

async def SheetCleanup(sheetName, newSheetName):
    sheet = client.open(sheetName)
    worksheet_list = sheet.worksheets()
    if newSheetName in str(worksheet_list):
        return False
    else:
        for worksheet in worksheet_list:
            if worksheet.title != "Master Copy":
                sheet.del_worksheet(sheet.worksheet(worksheet.title))
        sheet.duplicate_sheet(source_sheet_id=sheet.worksheet("Master Copy").id, new_sheet_name=newSheetName)
        return True

# Deletes target sheet
async def DeleteSheets(sheetName):
    sheet = client.open(sheetName)
    worksheet_list = sheet.worksheets()
    for worksheet in worksheet_list:
        if worksheet.title != "Master Copy":
            sheet.del_worksheet(sheet.worksheet(worksheet.title))

# Handles the switching of google service accounts, can adjust to however many accounts the user has
async def switchAccounts(initialize=None):
    global creds, account, client
    if initialize != None:
        account = initialize
    if account == 'uw-1':
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds_uw_2.json", scope)
        client = gspread.authorize(creds)
        account = 'uw-2'
        #print('Successfully switched to account uw-2!')
    elif account == 'uw-2':
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds_uw_3.json", scope)
        client = gspread.authorize(creds)
        account = 'uw-3'
        #print('Successfully switched to account uw-3!')
    elif account == 'uw-3':
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds_uw_4.json", scope)
        client = gspread.authorize(creds)
        account = 'uw-4'
        #print('Successfully switched to account uw-4!')
    elif account == 'uw-4':
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds_uw_1.json", scope)
        client = gspread.authorize(creds)
        account = 'uw-1'
        #print('Successfully switched to account uw-1!')



async def MasterProcess(sheetName, port, portPrices, previousAccount):
    await switchAccounts(initialize=previousAccount)
    port = PORTTRANSLATION[port]
    worksheet = await GetWorksheet(sheetName)
    currentPortData = await GetDataFrame(worksheet, port)
    await CompareData(worksheet, port, currentPortData, portPrices)
    return account


