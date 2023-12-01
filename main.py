from replit import db
import requests
import time
import threading
import os

from Keep_alive import keep_alive

null = []
true = True

keep_alive()


def different_user_data(user_id, user_name):
  url = os.getenv("Api_key")

  payload = {"encryptedUid": user_id, "tradeType": "PERPETUAL"}

  def filter_data(old, x):
    new = []
    deleted = []
    if old == [] or len(old) == 0:
      new = x
      return new, deleted
    new = [item for item in x if item not in old]
    temp1=[]
    for i in x:
      temp1.append(i['symbol'])
    temp2=[]
    for j in old:
      temp2.append(j['symbol'])
    deleted=[i for i in temp2 if i not in temp1 ]
     
    return new, deleted

  def send_to_telegram(text):
    bot_token = os.getenv("bot_token")
    group_id = os.getenv("group_id")

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
      "chat_id": group_id,
      "text": text,
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
      print("Message sent successfully")
    else:
      print("Failed to send message")

  old = []
  empty = True
  while True:
    response = requests.post(url, json=payload)
    null = []
    true = True
    if response.status_code == 200:
      Data = response.json()
      x = Data['data']['otherPositionRetList']
      print(x)
      if x != None or len(x) != 0:
        empty = True
        for i in x:
          del i['markPrice']
          del i['pnl']
          del i['updateTime']
          del i['updateTimeStamp']
          del i['roe']
        # temp=old
        if old != x:
          new, deleted = filter_data(old, x)

          for i in new:
            if i['amount'] < 0:
              fire = "\U0001F525" * 2
              msg = fire + " Sell Call " + fire + "\n" + " Symbol = " + i[
                'symbol'] + "\n" + "Entry_Price=" + str(
                  i['entryPrice']) + "\n" + " Leverage = " + str(
                    i['leverage']) + "\n" + "By..." + user_name
              send_to_telegram(msg)

            else:
              fire = "\U0001F525" * 2
              msg = fire + " Buy Call " + fire + "\n" + " Symbol  =  " + i[
                'symbol'] + "\n" + "Entry_Price=" + str(
                  i['entryPrice']) + "\n" + " Leverage = " + str(
                    i['leverage']) + "\n" + "By..." + user_name
              send_to_telegram(msg)
          new = []
          if deleted is not []:
            for i in deleted:
              if i['amount'] < 0:
                e = "\U0001F6D1" * 2
                msg = e + " Sell Call **** Closed **** " + e + "\n" + "Symbol=" + i[
                  'symbol'] + "\n" + "By..." + user_name
                send_to_telegram(msg)

              else:
                e = "\U0001F6D1" * 2
                msg = e + "Buy Call **** Closed ****" + e + "\n" + "Symbol=" + i[
                  'symbol'] + "\n" + "By..." + user_name
                send_to_telegram(msg)
            deleted = []

          old = x
      else:
        if empty:
          e = "\U0001F6D1" * 2
          msg = e + "Closed_all_position By ...." + e + user_name
          send_to_telegram(msg)
          empty = False

    else:

      msg = "Stopped Sharing Postion So Close Positions Accordingly"
      send_to_telegram(msg)

    time.sleep(15)


threads = []
user = [['0AA8893770EC615D0C2EF5ECB49D1DC4','Dianor']]
for i in range(len(user)):
  t = threading.Thread(target=different_user_data,
                       args=(user[i][0], user[i][1]))
  threads.append(t)
  t.start()
for i in threads:
  i.join()
keep_alive()
