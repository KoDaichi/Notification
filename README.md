# CLI -> LINE (Massaging API)  
## Remote-setting
1. Login LINE Developers
2. Create Provider (Ex: Daichi\_Private\_Provider)
3. Create "Massaging API" channel
4. Create LINE Official Account (Ex: Deech\_official)  
   This is the channel you recieve a message.

## Local-setting
5. Create private and public key
6. Set public key in created channel
7. Create channel access token  
   (Ref: https://qiita.com/knaot0/items/8427918564400968bd2b )  
8. Test main.py


* Ref: https://developers.line.biz/ja/docs/messaging-api/generate-json-web-token/#generate-a-key-pair-for-the-assertion-signing-key


# LINE -> CLI -> LINE (Webhook & Massaging API)
## Setting
1. Set up a server (Run run\_command.py)  
2. Forwarding  
   `$ ngrok http <your_local_port_number>` ; on the another terminal
   Before using ngrok, you need to create your account and get authtoken.  
   It is set as  
   `$ ngrok config add-authtoken <authtoken>`
3. Set displayed URL into the LINE Developers Webhook URL  
   Ex) https://unconfidently-unfraught-giana.ngrok-free.dev/callback 
