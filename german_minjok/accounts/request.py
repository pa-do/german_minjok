import hashlib
import hmac
import base64
import requests
import time, json

timestamp = int(time.time() * 1000)
timestamp = str(timestamp)

url = "https://sens.apigw.ntruss.com"
requestUrl = "/sms/v2/services/"
requestUrl2 = "/messages"
serviceId = "ncp:sms:kr:259241969530:german"
access_key = "MnYIs6OrJkEdFJcnsRm1"

uri = requestUrl + serviceId + requestUrl2
apiUrl = url + uri

def make_signaure(uri, access_key):
    secret_key = "h4Wl6coduavPADMRcnkGFIXz3XOl4G4J8gyT9Vmy"
    secret_key = bytes(secret_key, 'UTF-8')
    method = "POST"
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signigKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signigKey

messages = { "to" : "01076338540" }
body = {
    "type" : "SMS",
    "contentType" : "COMM",
    "from" : "01076338540",
    "subject" : "subject",
    "content" : "[게르만 민족]",
    "messages" : [messages]
}
body2 = json.dumps(body)
headers = {
    "Content-Type": "application/json; charset=utf-8",
    "x-ncp-apigw-timestamp": timestamp,
    "x-ncp-iam-access-key": access_key,
    "x-ncp-apigw-signature-v2": make_signaure(uri, access_key)
}

res = requests.post(apiUrl, headers=headers, data=body2)
print(res.json())