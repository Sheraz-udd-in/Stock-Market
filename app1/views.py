import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import *


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
    token  =  "65296f95ff2c90506f05875435311a8227a560db"
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


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')


        panCard = request.POST.get('panCard')
        phoneNumber = request.POST.get('phoneNumber')
        profile_pic = request.FILES.get('profile_pic')
        panCard_Image = request.FILES.get('panCard_Image')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')


        user = User(username=username, email=email)
        user.set_password(password)
        user.save()


        user_info = UserInfo(
            user=user,
            panCard=panCard,
            phoneNumber=phoneNumber,
            profile_pic=profile_pic,
            panCard_Image=panCard_Image
        )
        user_info.save()

        login(request, user)
        return redirect('index')

    return render(request, 'register.html')
from django.views.decorators.http import require_http_methods
@login_required
@require_http_methods(["POST"])
def buy(request, id):
    user = request.user
    stock = get_object_or_404(Stocks, id=id)

    try:
        purchase_quantity = int(request.POST.get('quantity'))
        if purchase_quantity <= 0:
            messages.error(request, "Quantity must be positive.")
            return redirect('stocks')

        user_stock, created = UserStock.objects.get_or_create(
            user=user,
            stock=stock,
            defaults={
                'buyQuantity': purchase_quantity,
                'buyPrice': stock.curr_price
            }
        )

        if not created:
            total_quantity = user_stock.buyQuantity + purchase_quantity
            user_stock.buyPrice = (
                (user_stock.buyPrice * user_stock.buyQuantity) +
                (stock.curr_price * purchase_quantity)
            ) / total_quantity
            user_stock.buyQuantity = total_quantity
            user_stock.save()

        send_mail(
            subject="Buy Confirmation",
            message=f"You bought {purchase_quantity} shares of {stock.name}.",
            from_email=None,
            recipient_list=[user.email],
            fail_silently=True
        )

        messages.success(request, f"Successfully bought {purchase_quantity} shares of {stock.name}.")
        return redirect('index')

    except (ValueError, TypeError):
        messages.error(request, "Invalid quantity.")
        return redirect('stocks')