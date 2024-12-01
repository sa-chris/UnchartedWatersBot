# bot.py
import re
import requests
from PIL import Image, ImageEnhance, ImageOps, ImageFilter # Image Processing
import pytesseract  # OCR Engine # pip install pytesseract

# https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


PORTERROR = False # global to indicate if an error occurred while deciphering the Port name
PORTNAME = '' # global to store the erroneous port name


# List of all items found at ports
ITEMLIST = [
    'Agate', 'Alcohol', 'Bananas', 'Carpets', 'Cloth',
    'Diamonds', 'Dye', 'Firearms', 'Fish', 'Gold',
    'Leather', 'Meat', 'Medicine', 'Paper', 'Peanuts',
    'Pearls', 'Porcelain', 'Tea Leaves', 'Tin', 'Tobacco'
]


# List of all ports
PORTS = [
    "Buenos Aires", "Rio de Janeiro", "Cayenne", "Panama City", "Santo Domingo",  "Jamaica", "Nassau",
    "Boston", "Cape Town", "Luanda", "St Georges", "Las Palmas", "Tunis", "Alexandria", "Mozambique",
    "Stockholm", "Copenhagen", "Hamburg", "Amsterdam", "London", "Nantes", "Lisbon", "Seville",
    "Marseille", "Venice", "Athens", "Istanbul", "Hangzhou", "Quanzhou", "Edo", "Manila",
    "Kolkata", "Calicut", "Basrah", "Aden", "Ceylon", "Brunei", "Malacca", "Pinjarra", "Darwin"
]

# PORTS in lowercase with spaces removed
PORTSlower = [
    "buenosaires", "riodejaneiro", "cayenne", "panamacity", "santodomingo", "jamaica", "nassau",
    "boston", "capetown", "luanda", "st georges", "laspalmas", "tunis", "alexandria", "mozambique",
    "stockholm", "copenhagen", "hamburg", "amsterdam", "london", "nantes", "lisbon", "seville",
    "marseille", "venice", "athens", "istanbul", "hangzhou", "quanzhou", "edo", "manila",
    "kolkata", "calicut", "basrah", "aden", "ceylon", "brunei", "malacca", "pinjarra", "darwin"
]

# running list of transcription errors for ports
PORTERRORS = {
    "alexanaria":"alexandria",
    "basran":"basrah",
    "brunel": "brunei",
    "brune":"brunei",
    "buenosalres": "buenosaires",
    "buenosaltres": "buenosaires",
    "buenosalt": "buenosaires",
    "hangznou": "hangzhou",
    "riodejanelro":"riodejaneiro",
    "santodoming": "santodomingo",
    "ot. George's":"St Georges",
    "St. George's":"St Georges",
    "otgeorges":"St Georges",
    "stgeorges":"St Georges",
    "stgeorgesewe":"St Georges",
    "stgeorgesia":"St Georges"
}



# This function further crops the port image if it exceeds a certain height as phones with large screens continue to be problematic for the script
async def CheckPortSize(portImg):
    xSize, ySize = portImg.size
    if ySize >= 470: ### Previous values: 740, 535, now 470
        port = portImg.crop((0, 0, xSize, ySize * 0.6))
        return port
    else:
        return portImg


# Main image processing function; creates two cropped images - one of the port name, and one for all of the items & prices
async def ImageProcessing(img):
    image, port = Image.open(requests.get(img, stream=True).raw), Image.open(requests.get(img, stream=True).raw)   # opening from url
    xSize, ySize = image.size
    port = port.crop((0, 0, xSize * 0.55, ySize * 0.33))
    portPixels = port.load() # assess whether image is in RGB or RGBA format
    if len(portPixels[0, 0]) == 3:
        port = await processPort_RGB(port, portPixels, xSize, ySize)
    elif len(portPixels[0, 0]) == 4:
        port = await processPort_RGBA(port, portPixels, xSize, ySize)

    port = port.convert('L')
    port = ImageOps.invert(port)

    image = image.convert('L')
    image = ImageEnhance.Contrast(image)
    image = image.enhance(2.0)  # used to be 2.25, found 2.0 to work better
    pixels = image.load()
    for x in range(xSize):
        for y in range(ySize):
            if pixels[x, y] >= 53 and pixels[x, y] <= 209: # previous <= 221, now 209
                pixels[x, y] = 0
            if pixels[x, y] >= 210: # previous >= 222, now 210
                pixels[x, y] = 255
            elif pixels[x, y] <= 52:
                pixels[x, y] = 0

    leftHalf = image.crop((xSize * 0.15, ySize * 0.27, xSize / 2, ySize * 0.93))
    rightHalf = image.crop((xSize * 0.65, ySize * 0.27, xSize, ySize * 0.93))
    leftHalf = leftHalf.resize((leftHalf.size[0] * 2, leftHalf.size[1] * 2)).filter(ImageFilter.GaussianBlur(radius=1))
    rightHalf = rightHalf.resize((rightHalf.size[0] * 2, rightHalf.size[1] * 2)).filter(ImageFilter.GaussianBlur(radius=1))

    # https://stackoverflow.com/questions/44619077/pytesseract-ocr-multiple-config-options
    # had most success with psm 6 & 12, liked formatting of 12 better than 6
    textLeft = pytesseract.image_to_string(leftHalf, lang='eng', config='--psm 6')
    textRight = pytesseract.image_to_string(rightHalf, lang='eng', config='--psm 6')
    textName = pytesseract.image_to_string(port, lang='eng')#, config='--psm 6')
    textPort = re.sub(r'[^a-zA-Z]', '', textName).lower()
    return textPort, textLeft, textRight, port


# Processes port name if image was presented as RGB
async def processPort_RGB(portImg, portPixels, xSize, ySize):
    port = portImg
    ## To determine if a black border is present at the top of the image
    if portPixels[0, 0] == (0, 0, 0):
        for y in range(port.size[1]):
            if portPixels[0,y] == (0, 0, 0):
                pass
            else:
                port = port.crop((0, y, xSize, ySize))
                break

    ## To determine the position of the red hair in the female character
    portRGB = port.load()
    found = False # to control the first observation of >120, >90, >30 RGB
    for y in range(port.size[1]):
        done = False
        for x in range(port.size[0]):
            reds, greens, blues = portRGB[x,y][0], portRGB[x,y][1], portRGB[x,y][2]
            if 110 <= reds <= 130 and 88 <= greens <= 98 and 25 <= blues <= 45 and found == False:
                found = True
                port = port.crop((0, y, port.size[0], port.size[1]))
            if reds >= 80 and blues <= reds / 2 and greens <= reds / 2: #originally 75
                port = port.crop((0, 0,  x * 0.7, y * 0.65))
                done = True
                break
            else:
                pass
        if done:
            break
    port = port.resize((port.size[0] * 5, port.size[1] * 5))

    ## To crush the Blues and Greens in image
    portPixels = port.load()
    for x in range(port.size[0]):
        for y in range(port.size[1]):
            reds, greens, blues = portPixels[x, y][0], portPixels[x, y][1], portPixels[x, y][2]
            if blues <= 165 or greens <= 200:
                portPixels[x, y] = (0, 0, 0)
            else:
                portPixels[x, y] = (255, 255, 255)

    ## To locate the farthest right white pixel to clean up the '?' circle
    updatedPortPixels = port.load()
    farRightWhite = 0
    for x in range(port.size[0]):
        for y in range(port.size[1]):
            if updatedPortPixels[x, y] == (255, 255, 255) and x > farRightWhite:
                farRightWhite = x
            else:
                pass
    port = port.crop((0, 0, farRightWhite * 0.95, port.size[1]))
    port = await CheckPortSize(port)
    return port


# Processes port name if image was presented as RGBA
async def processPort_RGBA(portImg, portPixels, xSize, ySize):
    port = portImg
    ## To determine if a black border is present at the top
    if portPixels[0, 0] == (0, 0, 0, 255):
        for y in range(port.size[1]):
            if portPixels[0, y] == (0, 0, 0, 255):
                pass
            else:
                port = port.crop((0, y, xSize, ySize))
                break

    ## To determine the position of the red hair in the female character
    portRGB = port.load()
    found = False  # to control the first observation of >120, >90, >30 RGB
    for y in range(port.size[1]):
        done = False
        for x in range(port.size[0]):
            reds, greens, blues = portRGB[x, y][0], portRGB[x, y][1], portRGB[x, y][2]
            if 110 <= reds <= 130 and 88 <= greens <= 98 and 25 <= blues <= 45 and found == False:
                found = True
                port = port.crop((0, y, port.size[0], port.size[1]))
            if reds >= 80 and blues <= reds / 2 and greens <= reds / 2:  # originally 75
                port = port.crop((0, 0, x * 0.7, y * 0.65))
                done = True
                break
            else:
                pass
        if done:
            break
    port = port.resize((port.size[0] * 5, port.size[1] * 5))

    ## To crush the Blues and Greens in image
    portPixels = port.load()
    for x in range(port.size[0]):
        for y in range(port.size[1]):
            reds, greens, blues = portPixels[x, y][0], portPixels[x, y][1], portPixels[x, y][2]
            if blues <= 165 or greens <= 200:
                portPixels[x, y] = (0, 0, 0, 255)
            else:
                portPixels[x, y] = (255, 255, 255, 255)

    ## To locate the farthest right white pixel to clean up the '?' circle
    updatedPortPixels = port.load()
    farRightWhite = 0
    for x in range(port.size[0]):
        for y in range(port.size[1]):
            if updatedPortPixels[x, y] == (255, 255, 255, 255) and x > farRightWhite:
                farRightWhite = x
            else:
                pass
    port = port.crop((0, 0, farRightWhite * 0.95, port.size[1]))
    port = await CheckPortSize(port)
    return port


# Retrieves prices and converts to an int if price is present
async def TextProcessing(textLeft, textRight):
    portPrices = []
    for item in ITEMLIST:
        price = "X" # Assumes price not present initially, assigns "X"
        price = await GrabPriceString(item, price, textLeft)
        price = await GrabPriceString(item, price, textRight)
        try:
            price = int(price) # attempts to turn string into an int
        except:
            pass
        portPrices.append(price)
    return portPrices


# Adjusts the length of the price to correct for common transcription errors experienced
async def PriceAdjustment(price):
    if str(price[0]) == '8' or str(price[0]) == '9':
        return price[0:2] # Prices will only be 2 digits if they begin with an 8 or 9
    else:
        return price[0:3] # Prices will be 3 digits if it doesnt start with an 8 or 9 (100s, 110s)


# Extracts item value from text
async def GrabPriceString(item, price, text):
    price = price
    try:
        if "Profit" in text or "Loss" in text: # to allow users to upload sell pages & extract data from it
            priceString = text.split(item)[1]
            index = await findProfitLoss((priceString))
            priceString = priceString[0:index].split('(')[1]
            price = re.sub(r'[^0-9]', '', priceString)
            price = '****' + await PriceAdjustment(price) # "****" is added to indicate that item can be sold, but cannot be purchased. Also apart of conditional format for spreadsheet
        else: # this processes the "buy" page as Profit/Loss does not appear on these images
            priceString = text.split(item)[1].split('Weight')[0].split('(')[1]
            priceString = priceString[0:4]  ###  2024 EDIT - Was previously 0:3 but sometimes a '{' would appear in pricestring like ({105% so this eliminates that
            price = re.sub(r'[^0-9]', '', priceString)
            price = await PriceAdjustment(price)
    except IndexError:
        pass
    return price


# Finds first instance of "Profit" and "Loss" in pricestring and returns their index to increase accuracy of retrieving price
async def findProfitLoss(pricestring):
    profit = pricestring.find("Profit")
    loss = pricestring.find("Loss")
    if profit < loss and profit != -1:
        return profit
    else:
        return loss


# Verifies name of port, tries to correct for transcription errors
async def CheckPortName(rawPort):
    port = rawPort
    try:
        if port in PORTSlower:
            return True, port
        elif port not in PORTSlower: # this else statement assumes an error occurred during transcrption, tries to correct for it
            ## new may 1 2023 ##
            for ports in PORTSlower:
                if ports in port: # if the port name (from PORTSlower) is present in port, will assign that name to port
                    port = ports
                    return True, port
                elif "stgeorges" in port: # experienced difficulty with this name in particular
                    port = "stgeorges"
                    return True, port
                else:
                    pass
            ## end new ##
            if port in PORTERRORS:
                port = PORTERRORS[port]
                return True, port
            else:
                for portName in PORTSlower:
                    if portName in port:
                        return True, portName
        else:
            return False, port
    except Exception as err:
        print(f'Unknown Error [{err}] occurred in CheckPortName({port})')



# Main process
async def MasterProcess(image):
    rawPort, rawTextLeft, rawTextRight, portError = await ImageProcessing(image)
    portPrices = ""
    try:
        success, port = await CheckPortName(rawPort)
    except TypeError:
        success, port = False, rawPort
        print(rawPort)
        portError.show()
        portError.save(f"{rawPort}.jpg")
        print(f"{rawPort} not found in PortErrorDictionary!")
    if success:
        portPrices = await TextProcessing(rawTextLeft, rawTextRight)
    else:
        print(f"ERROR: Could not find this port - {port}")
    return success, port, portPrices

