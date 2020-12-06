import random
import requests
import json
import paytmchecksum


MID= 'CLSGvC85119487671685'
KEY = '#F9e%toAivZgqt1d'
def check_payment_status(orderId , amount):
    paytmParams = dict()
    paytmParams["body"] = {
    "requestType" : "NATIVE",
    "mid"         : MID,
    "orderId"     : orderId,
    "paymentMode" : "BALANCE",
    }
    paytmParams["head"] = {
        "txnToken"    : "f0bed899539742309eebd8XXXX7edcf61588842333227"
        }
    post_data = json.dumps(paytmParams)
    url = "https://securegw-stage.paytm.in/theia/api/v1/processTransaction"
    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    print(response)        
    return response
    

# def check_payment_status(orderId , amount):
#     paytmParams = dict()
#     paytmParams["body"] = {
#     "mid" : MID,
#     "txnAmount" : amount,
#     "orderId" : orderId,
#     }
#     checksum = paytmchecksum.generateSignature(json.dumps(paytmParams["body"]), KEY)
#     paytmParams["head"] = {
#     "signature"	: checksum
#     }
#     post_data = json.dumps(paytmParams)

#     url = "https://securegw-stage.paytm.in/v3/order/status"
#     response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
#     return response