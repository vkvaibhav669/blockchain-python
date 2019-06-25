import pyotp  
import time 
topt = pyotp.TOTP('base32secret3232')
h = topt.now()
#print(h)
import requests
url = "https://www.fast2sms.com/dev/bulk"
#a = raw_input("enter message: ")
#h = type(a)
payload = "sender_id=FSTSMS&message=h&language=english&route=p&numbers=9928905025"
headers = {
'authorization': "J7kqr0uFmezwCfIlDs2N1vb6cHKUWY9aVnxO8GAgyZ3PTR4LXhM5NGYXoiDuKSyVFrEBOdtwQ3URmkp4",
'Content-Type': "application/x-www-form-urlencoded",
'Cache-Control': "no-cache",
}
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)
print(' Proceding to next page \n ')
a = raw_input("Enter OTP recieved via SMS")
A = type(a)
print(topt.verify(A))
time.sleep(30)
print(topt.verify(A))

