# import
import gspread
import gspread_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from operator import itemgetter  # used to sort list of list by specific index
import math


# gspread info #
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds_uw_1.json", scope)
client = gspread.authorize(creds)


##item index##
agate, alcohol, bananas, carpets, cloth = 0, 1, 2, 3, 4
diamonds, dye, firearms, fish, gold = 5, 6, 7, 8, 9
leather, meat, medicine, paper, peanuts = 10, 11, 12, 13, 14
pearls, porcelain, tealeaves, tin, tobacco = 15, 16, 17, 18, 19

##port list##
PORTS = ["Buenos Aires", "Rio de Janeiro", "Cayenne", "Panama City", "Santo Domingo", "Jamaica", "Nassau", "Boston",
         "Cape Town", "Luanda", "St Georges", "Las Palmas", "Tunis", "Alexandria", "Mozambique", "Stockholm",
         "Copenhagen", "Hamburg", "Amsterdam", "London", "Nantes", "Lisbon", "Seville", "Marseille", "Venice", "Athens",
         "Istanbul", "Hangzhou", "Quanzhou", "Edo", "Manila", "Kolkata", "Calicut", "Basrah", "Aden", "Ceylon",
         "Brunei", "Malacca", "Pinjarra", "Darwin"]

## Item List ##
ITEMLIST = [
    'Agate', 'Alcohol', 'Bananas', 'Carpets', 'Cloth',
    'Diamonds', 'Dye', 'Firearms', 'Fish', 'Gold',
    'Leather', 'Meat', 'Medicine', 'Paper', 'Peanuts',
    'Pearls', 'Porcelain', 'Tea Leaves', 'Tin', 'Tobacco'
]

## Reference Port Dictionary for dataframes ##
MASTERPORTKEY = {
    "Buenos Aires": [],
    "Rio de Janeiro": [],
    "Cayenne": [],
    "Panama City": [],
    "Santo Domingo": [],
    "Jamaica": [],
    "Nassau": [],
    "Boston": [],
    "Cape Town": [],
    "Luanda": [],
    "St Georges": [],
    "Las Palmas": [],
    "Tunis": [],
    "Alexandria": [],
    "Mozambique": [],
    "Stockholm": [],
    "Copenhagen": [],
    "Hamburg": [],
    "Amsterdam": [],
    "London": [],
    "Nantes": [],
    "Lisbon": [],
    "Seville": [],
    "Marseille": [],
    "Venice": [],
    "Athens": [],
    "Istanbul": [],
    "Hangzhou": [],
    "Quanzhou": [],
    "Edo": [],
    "Manila": [],
    "Kolkata": [],
    "Calicut": [],
    "Basrah": [],
    "Aden": [],
    "Ceylon": [],
    "Brunei": [],
    "Malacca": [],
    "Pinjarra": [],
    "Darwin": []
}

## Data Frames ##
PORTDATAFRAMES = []
ACTIVESHEET = []

##
PORTPROFITDATA = []  # holds all port profit data


def PopulateDataFrame(sheetname):
    global ACTIVESHEET
    sheet = client.open(sheetname)
    worksheet = sheet.get_worksheet(0)  # opens the first sheet
    ACTIVESHEET = gspread_dataframe.get_as_dataframe(worksheet)
    cols = [1, 2, 11, 12, 20, 21, 34, 35]  # remove the blank column spacers
    ACTIVESHEET = ACTIVESHEET.drop(ACTIVESHEET.columns[cols], axis=1)
    ACTIVESHEET = ACTIVESHEET.fillna('X')  # replaces NaN from blank cells with 'X'


def CreatePortDataFrames(port):
    # prices = ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"]
    prices = ["X"]
    port_dict = {
        "Buenos Aires": [prices], "Rio de Janeiro": [prices], "Cayenne": [prices], "Panama City": [prices],
        "Santo Domingo": [prices],
        "Jamaica": [prices], "Nassau": [prices], "Boston": [prices], "Cape Town": [prices], "Luanda": [prices],
        "St Georges": [prices], "Las Palmas": [prices], "Tunis": [prices], "Alexandria": [prices],
        "Mozambique": [prices],
        "Stockholm": [prices], "Copenhagen": [prices], "Hamburg": [prices], "Amsterdam": [prices], "London": [prices],
        "Nantes": [prices], "Lisbon": [prices], "Seville": [prices], "Marseille": [prices], "Venice": [prices],
        "Athens": [prices], "Istanbul": [prices], "Hangzhou": [prices], "Quanzhou": [prices], "Edo": [prices],
        "Manila": [prices], "Kolkata": [prices], "Calicut": [prices], "Basrah": [prices], "Aden": [prices],
        "Ceylon": [prices], "Brunei": [prices], "Malacca": [prices], "Pinjarra": [prices], "Darwin": [prices]
    }
    port_dict.pop(port)
    frame = pd.DataFrame(port_dict,
                         index=["Agate", "Alcohol", "Bananas", "Carpets", "Cloth", "Diamonds", "Dye", "Firearms",
                                "Fish", "Gold", "Leather", "Meat", "Medicine", "Paper", "Peanuts", "Pearls",
                                "Porcelain", "Tea Leaves", "Tin", "Tobacco"])
    return frame


def AssignPortDataFrames():
    global PORTDATAFRAMES
    frameBuenos = CreatePortDataFrames('Buenos Aires')
    frameRio = CreatePortDataFrames("Rio de Janeiro")
    frameCayenne = CreatePortDataFrames("Cayenne")
    framePanama = CreatePortDataFrames("Panama City")
    frameSanto = CreatePortDataFrames("Santo Domingo")
    frameJamaica = CreatePortDataFrames("Jamaica")
    frameNassau = CreatePortDataFrames("Nassau")
    frameBoston = CreatePortDataFrames("Boston")
    frameCape = CreatePortDataFrames("Cape Town")
    frameLuanda = CreatePortDataFrames("Luanda")
    frameStGeorges = CreatePortDataFrames("St Georges")
    frameLasPalmas = CreatePortDataFrames("Las Palmas")
    frameTunis = CreatePortDataFrames("Tunis")
    frameAlexandria = CreatePortDataFrames("Alexandria")
    frameMozam = CreatePortDataFrames("Mozambique")
    frameStockholm = CreatePortDataFrames("Stockholm")
    frameCopen = CreatePortDataFrames("Copenhagen")
    frameHamburg = CreatePortDataFrames("Hamburg")
    frameAmsterdam = CreatePortDataFrames("Amsterdam")
    frameLondon = CreatePortDataFrames("London")
    frameNantes = CreatePortDataFrames("Nantes")
    frameLisbon = CreatePortDataFrames("Lisbon")
    frameSeville = CreatePortDataFrames("Seville")
    frameMarseille = CreatePortDataFrames("Marseille")
    frameVenice = CreatePortDataFrames("Venice")
    frameAthens = CreatePortDataFrames("Athens")
    frameIstanbul = CreatePortDataFrames("Istanbul")
    frameHangzhou = CreatePortDataFrames("Hangzhou")
    frameQuanzhou = CreatePortDataFrames("Quanzhou")
    frameEdo = CreatePortDataFrames("Edo")
    frameManila = CreatePortDataFrames("Manila")
    frameKolkata = CreatePortDataFrames("Kolkata")
    frameCalicut = CreatePortDataFrames("Calicut")
    frameBasrah = CreatePortDataFrames("Basrah")
    frameAden = CreatePortDataFrames("Aden")
    frameCeylon = CreatePortDataFrames("Ceylon")
    frameBrunei = CreatePortDataFrames("Brunei")
    frameMalacca = CreatePortDataFrames("Malacca")
    framePinjarra = CreatePortDataFrames("Pinjarra")
    frameDarwin = CreatePortDataFrames("Darwin")
    PORTDATAFRAMES = [
        frameBuenos, frameRio, frameCayenne, framePanama, frameSanto, frameJamaica, frameNassau, frameBoston, frameCape,
        frameLuanda, frameStGeorges, frameLasPalmas, frameTunis, frameAlexandria, frameMozam, frameStockholm,
        frameCopen,
        frameHamburg, frameAmsterdam, frameLondon, frameNantes, frameSeville, frameLisbon, frameMarseille, frameVenice,
        frameAthens, frameIstanbul, frameHangzhou, frameQuanzhou, frameEdo, frameManila, frameCalicut, frameKolkata,
        frameBasrah, frameAden, frameCeylon, frameBrunei, frameMalacca, framePinjarra, frameDarwin]


def removeCurrentPort(str):
    ports = ["Buenos Aires", "Rio de Janeiro", "Cayenne", "Panama City", "Santo Domingo", "Jamaica", "Nassau", "Boston",
             "Cape Town", "Luanda", "St Georges", "Las Palmas", "Tunis", "Alexandria", "Mozambique", "Stockholm",
             "Copenhagen", "Hamburg", "Amsterdam", "London", "Nantes", "Lisbon", "Seville", "Marseille", "Venice",
             "Athens",
             "Istanbul", "Hangzhou", "Quanzhou", "Edo", "Manila", "Kolkata", "Calicut", "Basrah", "Aden", "Ceylon",
             "Brunei", "Malacca", "Pinjarra", "Darwin"]
    ports.remove(str)
    return ports


def CalcProfitMargins(portName, dataFramePos):
    global ACTIVESHEET, PORTDATAFRAMES
    ports = removeCurrentPort(portName)
    homePortPrices = []
    for price in ACTIVESHEET[portName]:
        homePortPrices.append(price)
    frame = PORTDATAFRAMES[dataFramePos]
    portProfits = []  ## Holds the top profits for each port being compared to the home port
    for port in ports:
        awayPortPrices = []
        for price in ACTIVESHEET[port]:
            awayPortPrices.append(price)
        y = 0
        topAway = []
        topHome = []
        for item in ITEMLIST:
            # need to separate each way
            diffHome = CalcBestRoute(homePortPrices[y], awayPortPrices[y])
            try:
                if diffHome > 0:
                    topHome.append([item, diffHome])
            except TypeError:
                pass
            diffAway = CalcBestRoute(awayPortPrices[y], homePortPrices[y])
            try:
                if diffAway > 0:
                    topAway.append([item, diffAway])
            except TypeError:
                pass
            frame.loc[item, port] = diffHome
            frame.loc[item, port] = diffAway
            y = y + 1
        ## start sorting profits ##
        sortedHome = sorted(topHome, key=itemgetter(1), reverse=True)  # reversed=True sorts descending
        sortedAway = sorted(topAway, key=itemgetter(1), reverse=True)
        sixthHome, sixthAway = 'X', 'X'
        try:
            sixthHome, sixthAway = sortedHome[5], sortedAway[5]
        except:
            pass # exits if no sixth item is present
        if len(sortedHome) >= 6:
            del sortedHome[5:]  # will only keep the top 5 values
        if len(sortedAway) >= 6:
            del sortedAway[5:]  # will only keep the top 5 values
        ## end profit sorting ##
        ## start port sums ##
        portSum = 0
        for profit in sortedHome:
            portSum = portSum + profit[1]
        for profit in sortedAway:
            portSum = portSum + profit[1]  # so negative values get added to the sum
        ## end port sum
        portProfits.append([port, portSum, sortedHome, sortedAway, sixthHome, sixthAway])
    topPortProfits = sorted(portProfits, key=itemgetter(1), reverse=True)[0:5]  ## only keeps the top 5 port profits

    return portName, topPortProfits

# Calculates the optimal trade routes
def CalcBestRoute(startPort, endPort):
    diff = ''
    try:
        diff = int(endPort) - int(startPort)
    except TypeError:
        pass
    except ValueError:
        if '*' in str(startPort) and '*' in str(endPort):
            pass
        elif 'X' in str(startPort) and 'X' in str(endPort):
            pass
        elif '*' in str(startPort) or 'X' in str(startPort) or 'X' in str(endPort):
            # starred price at home means it is unavailable for purchase and should be ignored
            # 'X' means value not yet known and will be ignored
            diff = ''
        elif '*' in endPort:
            priceFix = endPort[4:]
            diff = int(priceFix) - int(startPort)
        elif math.isnan(startPort) or math.isnan(endPort):
            pass
        else:
            print('ERROR: unknown error occurred during CalcBestRoute.MarginCalculator')
    return diff

# Sorts profit margins of trade routes
def SortProfitMargins():
    firstSum, firstHome, firstAway, firstItems = 0, '', '', []
    secondSum, secondHome, secondAway, secondItems = 0, '', '', []
    thirdSum, thirdHome, thirdAway, thirdItems = 0, '', '', []
    fourthSum, fourthHome, fourthAway, fourthItems = 0, '', '', []
    fifthSum, fifthHome, fifthAway, fifthItems = 0, '', '', []
    for portVar in PORTPROFITDATA:
        portName = portVar[0]
        portData = portVar[1:]
        x = 0
        for port in portData:
            portSum = int(port[x][1])
            # these 4 lines takes the sixth item (not used in sum calcs) and adds it back in as a 'just in case' purchase
            if port[x][4] != 'X':
                port[x][2].append(port[x][4])
            if port[x][5] != 'X':
                port[x][3].append(port[x][5])
            if portSum > firstSum:
                # if not CheckForDuplicates(portName, port[x][0], firstHome, firstAway):
                fifthSum, fifthHome, fifthAway, fifthItems = fourthSum, fourthHome, fourthAway, fourthItems
                fourthSum, fourthHome, fourthAway, fourthItems = thirdSum, thirdHome, thirdAway, thirdItems
                thirdSum, thirdHome, thirdAway, thirdItems = secondSum, secondHome, secondAway, secondItems
                secondSum, secondHome, secondAway, secondItems = firstSum, firstHome, firstAway, firstItems
                firstSum, firstHome, firstAway, firstItems = portSum, portName, port[x][0], port[x][2:]
            elif portSum > secondSum:
                if not CheckForDuplicates(portName, port[x][0], firstHome, firstAway):
                    fifthSum, fifthHome, fifthAway, fifthItems = fourthSum, fourthHome, fourthAway, fourthItems
                    fourthSum, fourthHome, fourthAway, fourthItems = thirdSum, thirdHome, thirdAway, thirdItems
                    thirdSum, thirdHome, thirdAway, thirdItems = secondSum, secondHome, secondAway, secondItems
                    secondSum, secondHome, secondAway, secondItems = portSum, portName, port[x][0], port[x][2:]
            elif portSum > thirdSum:
                if not CheckForDuplicates(portName, port[x][0], secondHome, secondAway):
                    fifthSum, fifthHome, fifthAway, fifthItems = fourthSum, fourthHome, fourthAway, fourthItems
                    fourthSum, fourthHome, fourthAway, fourthItems = thirdSum, thirdHome, thirdAway, thirdItems
                    thirdSum, thirdHome, thirdAway, thirdItems = portSum, portName, port[x][0], port[x][2:]
            elif portSum > fourthSum:
                if not CheckForDuplicates(portName, port[x][0], thirdHome, thirdAway):
                    fifthSum, fifthHome, fifthAway, fifthItems = fourthSum, fourthHome, fourthAway, fourthItems
                    fourthSum, fourthHome, fourthAway, fourthItems = portSum, portName, port[x][0], port[x][2:]
            elif portSum > fifthSum:
                if not CheckForDuplicates(portName, port[x][0], fourthHome, fourthAway):
                    fifthSum, fifthHome, fifthAway, fifthItems = portSum, portName, port[x][0], port[x][2:]
            else:
                pass
        x = x + 1 # updates counter
    result1 = (f"The top five trade routes by profit margin this refresh: \n"
               f"1) `{firstHome} <--> {firstAway} has a trade sum of {firstSum} {sumRanking(firstSum)}.` \n"
               f"__**{firstHome}**__ {GetItemsToBuy(firstItems[0])} \n"
               f"\n__**{firstAway}**__ {GetItemsToBuy(firstItems[1])} \n"
               "\n"
               "\n")
    result2 = (f"2) `{secondHome} <--> {secondAway} has a trade sum of {secondSum} {sumRanking(secondSum)}.` \n"
               f"__**{secondHome}**__ {GetItemsToBuy(secondItems[0])} \n"
               f"\n__**{secondAway}**__ {GetItemsToBuy(secondItems[1])} \n"
               "\n"
               "\n")
    result3 = (f"3) `{thirdHome} <--> {thirdAway} has a trade sum of {thirdSum} {sumRanking(thirdSum)}.` \n"
               f"__**{thirdHome}**__ {GetItemsToBuy(thirdItems[0])}  \n"
               f"\n__**{thirdAway}**__ {GetItemsToBuy(thirdItems[1])}  \n\n")
    result4 = ("\n "
               "\n"
               f"4) `{fourthHome} <--> {fourthAway} has a trade sum of {fourthSum} {sumRanking(fourthSum)}.` \n"
               f"__**{fourthHome}**__ {GetItemsToBuy(fourthItems[0])}  \n"
               f"\n__**{fourthAway}**__ {GetItemsToBuy(fourthItems[1])} \n"
               "\n"
               "\n")
    result5 = (f"5) `{fifthHome} <--> {fifthAway} has a trade sum of {fifthSum} {sumRanking(fifthSum)}.` \n"
               f"__**{fifthHome}**__ {GetItemsToBuy(fifthItems[0])} \n"
               f"\n__**{fifthAway}**__ {GetItemsToBuy(fifthItems[1])} \n")
    return result1, result2, result3, result4, result5

# Gives users an indication whether the route is worth pursuing
def sumRanking(sum):
    if sum >= 150:
        return '[Godly Route]'
    elif sum >= 140 and sum <= 149:
        return '[Excellent Route]'
    elif sum >= 130 and sum <= 139:
        return '[Decent Route]'
    elif sum <= 129:
        return '[Meh Route]'

# Ensures sailing routes are not duplicates of each other
# Example: Boston --> Nassau; Nassau --> Boston are
def CheckForDuplicates(newHome, newAway, previousHome, previousAway):
    home, away = False, False
    if newHome == previousHome or newHome == previousAway:
        home = True
    if newAway == previousHome or newAway == previousAway:
        away = True
    if away and home:
        return True
    else:
        return False

# Returns up to the first 6 items and their price depending on how many items have a positive profit margin
def GetItemsToBuy(items):
    sixth, sixthItem = False, ''
    if len(items) == 6:
        sixth = True
        sixthItem = items[5]
        items = items[0:5]
    buyString = ''
    x = 1
    for item in items:
        buyString = buyString + f'\n      {str(x)})  **{item[0]}**   (+{item[1]}) '
        x = x + 1
    if sixth:
        buyString = buyString + f'\n      *{str(x)})  **{sixthItem[0]}**   (+{sixthItem[1]})     (Buy if necessary)*'
    return buyString


def GetProfitMargins():
    global PORTPROFITDATA
    portBuenos = CalcProfitMargins('Buenos Aires', 0)
    portRio = CalcProfitMargins('Rio de Janeiro', 1)
    portCayenne = CalcProfitMargins('Cayenne', 2)
    portPanama = CalcProfitMargins('Panama City', 3)
    portSanto = CalcProfitMargins('Santo Domingo', 4)
    portJamaica = CalcProfitMargins('Jamaica', 5)
    portNassau = CalcProfitMargins('Nassau', 6)
    portBoston = CalcProfitMargins('Boston', 7)
    ##
    portCape = CalcProfitMargins('Cape Town', 8)
    portLuanda = CalcProfitMargins('Luanda', 9)
    portStGeorges = CalcProfitMargins('St Georges', 10)
    portLasPalmas = CalcProfitMargins('Las Palmas', 11)
    portTunis = CalcProfitMargins('Tunis', 12)
    portAlexandria = CalcProfitMargins('Alexandria', 13)
    portMozambique = CalcProfitMargins('Mozambique', 14)
    ##
    portStockholm = CalcProfitMargins('Stockholm', 15)
    portCopen = CalcProfitMargins('Copenhagen', 16)
    portHamburg = CalcProfitMargins('Hamburg', 17)
    portAmsterdam = CalcProfitMargins('Amsterdam', 18)
    portLondon = CalcProfitMargins('London', 19)
    portNantes = CalcProfitMargins('Nantes', 20)
    portLisbon = CalcProfitMargins('Lisbon', 21)
    portSeville = CalcProfitMargins('Seville', 22)
    portMarseille = CalcProfitMargins('Marseille', 23)
    portVenice = CalcProfitMargins('Venice', 24)
    portAthens = CalcProfitMargins('Athens', 25)
    portIstanbul = CalcProfitMargins('Istanbul', 26)
    ##
    portHang = CalcProfitMargins('Hangzhou', 27)
    portQuan = CalcProfitMargins('Quanzhou', 28)
    portEdo = CalcProfitMargins('Edo', 29)
    portManila = CalcProfitMargins('Manila', 30)
    portKolkata = CalcProfitMargins('Kolkata', 31)
    portCalicut = CalcProfitMargins('Calicut', 32)
    portBasrah = CalcProfitMargins('Basrah', 33)
    portAden = CalcProfitMargins('Aden', 34)
    portCeylon = CalcProfitMargins('Ceylon', 35)
    portBrunei = CalcProfitMargins('Brunei', 36)
    portMalacca = CalcProfitMargins('Malacca', 37)
    portPinjarra = CalcProfitMargins('Pinjarra', 38)
    portDarwin = CalcProfitMargins('Darwin', 39)

    PORTPROFITDATA = [portBuenos, portRio, portCayenne, portPanama, portSanto, portJamaica, portNassau, portBoston,
                      portCape, portLuanda, portStGeorges, portLasPalmas, portTunis, portAlexandria, portMozambique,
                      portStockholm, portCopen, portHamburg, portAmsterdam, portLondon, portNantes, portLisbon,
                      portSeville,
                      portMarseille, portVenice, portAthens, portIstanbul, portHang, portQuan, portEdo, portManila,
                      portKolkata, portCalicut, portBasrah, portAden, portCeylon, portBrunei, portMalacca, portPinjarra,
                      portDarwin]




# Master process
def MarginCalculator(sheetname):
    PopulateDataFrame(sheetname)
    AssignPortDataFrames()
    GetProfitMargins()
    result = SortProfitMargins()
    return result


