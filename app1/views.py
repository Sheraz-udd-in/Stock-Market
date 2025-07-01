from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# # Create your views here.
import requests

from .models import Stocks


#

# def fun(request) :
#     page  = '''
#     <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Title</title>
# </head>
# <body>
# <h1>Stock Market App</h1>
# <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Blanditiis commodi dignissimos dolor, ducimus enim harum in ipsum iure laboriosam minus, natus odit officiis omnis optio quibusdam quo, sapiente sunt voluptatibus!</p>
# <ul>
#     <li>s1</li>
#     <li>s2</li>
#     <li>s3</li>
# </ul>
# </body>
# </html>
#     '''
#     return  HttpResponse(page)

@login_required
def index(request) :
    return render(request ,  'index.html')



def getData(request) :
    nasdaq_tickers = [
        "AAPL",  # Apple Inc.
        "MSFT",  # Microsoft Corporation
        "GOOGL",  # Alphabet Inc. (Class A)
        "GOOG",  # Alphabet Inc. (Class C)
        "AMZN",  # Amazon.com Inc.
        "META",  # Meta Platforms Inc.
        "NVDA",  # NVIDIA Corporation
        "TSLA",  # Tesla Inc.
        "PEP",  # PepsiCo Inc.
        "INTC",  # Intel Corporation
        "CSCO",  # Cisco Systems Inc.
        "ADBE",  # Adobe Inc.
        "CMCSA",  # Comcast Corporation
        "AVGO",  # Broadcom Inc.
        "COST",  # Costco Wholesale Corporation
        "TMUS",  # T-Mobile US Inc.
        "TXN",  # Texas Instruments Inc.
        "AMGN",  # Amgen Inc.
        "QCOM",  # Qualcomm Incorporated
        "INTU",  # Intuit Inc.
        "PYPL",  # PayPal Holdings Inc.
        "BKNG",  # Booking Holdings Inc.
        "GILD",  # Gilead Sciences Inc.
        "SBUX",  # Starbucks Corporation
        "MU",  # Micron Technology Inc.
        "ADP",  # Automatic Data Processing Inc.
        "MDLZ",  # Mondelez International Inc.
        "ISRG",  # Intuitive Surgical Inc.
        "ADI",  # Analog Devices Inc.
        "MAR",  # Marriott International Inc.
        "LRCX",  # Lam Research Corporation
        "REGN",  # Regeneron Pharmaceuticals Inc.
        "ATVI",  # Activision Blizzard Inc.
        "ILMN",  # Illumina Inc.
        "WDAY",  # Workday Inc.
        "SNPS",  # Synopsys Inc.
        "ASML",  # ASML Holding N.V.
        "EBAY",  # eBay Inc.
        "ROST",  # Ross Stores Inc.
        "CTAS",  # Cintas Corporation
        "BIIB",  # Biogen Inc.
        "MELI",  # MercadoLibre Inc.
        "ORLY",  # O'Reilly Automotive Inc.
        "VRTX",  # Vertex Pharmaceuticals Inc.
        "DLTR",  # Dollar Tree Inc.
        "KHC",  # The Kraft Heinz Company
        "EXC",  # Exelon Corporation
        "FAST",  # Fastenal Company
        "JD",  # JD.com Inc.
        "CRWD"  # CrowdStrike Holdings Inc.
    ]

    headers = {
        'Content-Type': 'application/json'
    }
    token  =  "fced443141e501d554d0b38c4a34bba085172b1e"
    def getStock(ticker):
        url  = f"https://api.tiingo.com/tiingo/daily/{ticker}?token={token}"
        priceurl  =  f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?token={token}"
        requestResponse = requests.get(url, headers=headers )
        Metadata  = requestResponse.json()
        print(Metadata)
        priceData  = requests.get(priceurl , headers=headers)
        print(priceData.json())
        priceData =  priceData.json()[0]['close']

        # insert into SQL
        stock = Stocks(ticker  = Metadata['ticker']  , name  =  Metadata['name'] ,  description =  Metadata['description'] , curr_price  = priceData)
        stock.save()

    nasdaq_tickers =  nasdaq_tickers[11:30]
    for i in nasdaq_tickers :
        getStock(i)


    return HttpResponse("Stock Data Downloaded")


@login_required
def stocks(request) :
    stocks  = Stocks.objects.all()
    context  =  {'data' :  stocks}
    return render(request , 'market.html' ,  context)


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


def logoutView(request) :
    logout(request)
    return redirect('login')