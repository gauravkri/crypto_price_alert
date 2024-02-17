
from django.contrib.auth.models import User
from .models import Alert
from celery import shared_task
from .serializers import AlertSerializer, UserSerializer
import requests


@shared_task
def getPriceOfCoins(coins ):
    coin = url.encode(coins)
    print(coin)
    params = {
        "ids" : coin,
        "vs_currencies" : "USD",
        "precision" : "0"
    }
    url = "https://api.coingecko.com/api/v3/simple/price"
    req = requests.get(url,params=params)
    print(req.content)
    return req.content




def sendEmail(userid, alert):
    print('user '+ userid + "and  alert "+ alert )



@shared_task
def sendAlert():
    print("called")
    alerts = Alert.objects.all()
    coinsIds =[];
    createdBy = [];

    for alert in  alerts:
        coinsIds.append(alert['coin_id'])
        createdBy.append(alert['createdBy'])
    

    coinsCurrentPrice = getPriceOfCoins(','.join(coinsIds))
    for alert in alerts:
        if coinsCurrentPrice[alerts['coin_id']]['usd'] == alert['alert_price']:
             sendEmail(alert['createdBy'], alert)
        
    


    
    
