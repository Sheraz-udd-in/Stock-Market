from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# # Create your views here.
import requests

from .models import Stocks, UserInfo, UserStock

webscoket_api_key = 'd1hqgb1r01qsvr2bqhc0d1hqgb1r01qsvr2bqhcg'
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
def index(request):
    user = request.user
    user_stocks = UserStock.objects.filter(
        user=user,
        purchase_quantity__gt=0  # Only include stocks with quantity > 0
    ).select_related('stock')
    context = {
        'user_stocks': user_stocks
    }
    return render(request, 'index.html', context)

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
    context  =  {'data' :  stocks ,  'api_key' : webscoket_api_key }
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
        first_name  =  request.POST.get('first_name')
        last_name  = request.POST.get('last_name')

        address =   request.POST.get('address')
        panCard = request.POST.get('panCard')
        phoneNumber = request.POST.get('phoneNumber')
        profile_pic = request.FILES.get('profile_pic')
        panCard_Image = request.FILES.get('panCard_Image')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')


        user = User(username=username, email=email , first_name = first_name ,  last_name = last_name)
        user.set_password(password)
        user.save()


        user_info = UserInfo(
            user=user,
            pancard_number =panCard,
            address = address ,
            phone_number=phoneNumber,
            user_image=profile_pic,
            pancard_image=panCard_Image,
        )
        user_info.save()

        login(request, user)

        send_mail(subject="Welcome to Investing.com",
                  message=f"Welcome  {user.name} to our platfrom",
                  from_email=None,
                  recipient_list=[user.email], fail_silently=False)

        return redirect('index')

    return render(request, 'register.html')



@login_required
def buy(request , id) :
    stock  = get_object_or_404(Stocks ,  id =  id)
    user =  request.user
    purchase_quantity = int(request.POST.get('quantity'))
    purchase_price =   stock.curr_price

    # UserStock is an exmaple of Composite Keys in DBMS (user , stock) --> candidate key
    userStocks = UserStock.objects.filter(stock  =  stock   ,  user  =  user).first()
    if userStocks :
        userStocks.purchase_price = (userStocks.purchase_quantity*userStocks.purchase_price  +  purchase_price*purchase_quantity) / (purchase_quantity + userStocks.purchase_quantity)
        userStocks.purchase_quantity =  userStocks.purchase_quantity +  purchase_quantity
        userStocks.save()
    else  :
        userStock = UserStock(stock  = stock ,  user = user  ,  purchase_price =  purchase_price ,  purchase_quantity =  purchase_quantity )
        userStock.save()

    send_mail(subject="Buyed successfully", message=f"your purchase of stock {stock.name} is successfull",
              from_email=None,
              recipient_list=[user.email], fail_silently=True)
    return redirect('index')



def  sell(request , id) :
    stock = get_object_or_404(Stocks, id=id)
    user = request.user
    sell_quantity = int(request.POST.get('quantity'))
    userStock  =  UserStock.objects.filter(stock  =  stock ,  user =  user).first()

    if userStock.purchase_quantity <  sell_quantity :
        messages.error(request, "Can't sell more than you own")
        return redirect('market')

    userStock.purchase_quantity -= sell_quantity
    userStock.save()
    send_mail(subject="Sold successfully", message=f"Your Sale of stock {stock.name} is successfull",
              from_email=None,
              recipient_list=[user.email], fail_silently=False)
    return redirect('index')

#1)  Make a view to get all userStock for the perticular user
# 2) make a template to display cards and pass the context from view to template
# email notification  on registration   ,  sell and buy