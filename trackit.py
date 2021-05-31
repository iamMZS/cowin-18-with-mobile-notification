

import requests
import json
import bs4
from datetime import date
from notify_run import Notify 
import time

def doit(notify):

    today = (date.today()).strftime("%d-%m-%Y")
    districtID = "670"
    baseUrl = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    distId = "?district_id=" + districtID
    dateId = "&date=" + today

    apiUrl = baseUrl + distId + dateId
    headers = {
    'User-Agent': '...',
    'referer': 'https://...'
    }
    print(apiUrl)

    x = requests.get(apiUrl,headers=headers)
    # print(x.status_code)
    response=x.json()
    response = eval(json.dumps(response))
    # print(response['centers'][0])
    CentreAvailable = 0
    for centre in response['centers']:
        for sessions in centre['sessions']:
            if(sessions['min_age_limit']==18 and sessions['available_capacity_dose1']>0 ):
            # if(sessions['available_capacity_dose1']==10 ):
                print(sessions['vaccine'],"date:",sessions['date'] , " available dose1: ",sessions['available_capacity_dose1'])
                print(centre['name'])
                notify.send(centre['name']+" "+sessions['vaccine']+ " " +sessions['date']+ " " + str(sessions['available_capacity_dose1']))
                CentreAvailable +=1
    
    if(CentreAvailable):
        print(str(CentreAvailable) + " centres are available")
        msg = "Below " + str(CentreAvailable) + " centres are available"
        notify.send(msg)
    else:
        print("N0 centres available")
        notify.send("N0 centres available")





if __name__ == '__main__':
    i=0
    notify = Notify(endpoint="https://notify.run/ZeIkzzFO7ul6Wwr3")
    notify.send("from heroku")
    for i in range(0,12):
        print(i)
        doit(notify)
        time.sleep(60*10)



