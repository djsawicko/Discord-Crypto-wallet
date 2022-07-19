#Coin config
RPChost = 'http://127.0.0.1:8332/'
RPCuser = 'username'
RPCpass = 'password'

explorer = 'https://explorer.powx.org/tx/'

Cointicker = 'oBTC'

Contact = "@The Red Eye Studio#8319"




#ADVANCED SECTION, you may keep this as is

prefix = '/'

#Imports
from datetime import datetime
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from firebase_admin import credentials, firestore
import requests, decimal, json, discord, os, hashlib, time, pyotp, firebase_admin, qrcode, discord_slash

#FireStore collections, no need to change this
Collection='2FA'
tempCollection='temp_2FA'


#Discord auth token
DiscordToken = open("DiscordToken", "r").read()


# QR code config
qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)

#Bot stuff
bot = commands.Bot(command_prefix=prefix)
embed=discord.Embed()
slash=SlashCommand(bot, sync_commands=True)

#fireStore stuff
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

#Just a header, no need to change this
headers = {
    'content-type': 'text/plain;',
}







@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


# creation of wallet
@slash.slash(description='create your wallet')
async def create(ctx):
        await ctx.defer()
        embed.clear_fields()
        embed.remove_author()
        
        user = ctx.author.id
        WalletName = hashlib.md5(str(user).encode('utf-8')).hexdigest() #turn ID into MD5 (not for security)
        data = '{"jsonrpc": "1.0", "id": "curltest", "method": "createwallet", "params": ["'+str(WalletName) +'"]}' #RPC Data to be sent
        response = requests.post(RPChost, headers=headers, data=data, auth=(RPCuser, RPCpass)) # get a response
        json = response.json() # parse json
        if (str(json["error"])) == "None":
            embed.add_field(name='Congrats!', value="Your wallet is now created!")
            embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
            await ctx.reply(embed=embed)
            embed.clear_fields()
            embed.remove_author()
        else:
            if (json["error"])["code"] == -4:
                embed.add_field(name='Error!', value="Sorry dude, you can only create a wallet per account ;-;")
                embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                await ctx.reply(embed=embed)
                embed.clear_fields()
                embed.remove_author()
            else:
                embed.add_field(name="Error!", value="Undefined error, please send error code: "+ "``" +str(json["error"]) +"``" + "to " +Contact + ", this error code will be added to the database and it will provide a more usefull error message 👍" ) 
                embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                await ctx.reply(embed=embed)
                embed.clear_fields()
                embed.remove_author()
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + str(ctx.author) + " Experienced undefined error: " +str(json["error"]))

        user = "" 
        WalletName = ""
        data = ""
        response = ""
        json = ""
        embed.clear_fields()
        embed.remove_author()


# wallet ballace
@slash.slash(description="shows your balance")
async def balance(ctx):
    await ctx.defer()
    embed.clear_fields()
    embed.remove_author()

    user = ctx.author.id
    WalletName = hashlib.md5(str(user).encode('utf-8')).hexdigest()
    data = '{"jsonrpc": "1.0", "id":"curltest", "method": "getbalance", "params": [] }'
    response = requests.post(RPChost+'wallet/'+str(WalletName), headers=headers, data=data, auth=(RPCuser, RPCpass))
    json = response.json() 
    if (str(json["error"])) == "None":
        embed.add_field(name='Balance is:', value=str((json["result"])) + str(" ") +  str(Cointicker))
        embed.set_author(name=str(ctx.author) + "'s", icon_url=(ctx.author).avatar_url)
        await ctx.reply(embed=embed)
        embed.clear_fields()
        embed.remove_author()
    else:
        if (json["error"])["message"] == "Requested wallet does not exist or is not loaded":
            embed.add_field(name="Error!", value="Oops! wallet does not exist, please run " + prefix +"create")
            embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
            await ctx.reply(embed=embed)
            embed.clear_fields()
            embed.remove_author()
        else:
            embed.add_field(name="Error!", value="Undefined error, please send error code: "+ "``" +str(json["error"]) +"``" + "to " +Contact + ", this error code will be added to the database and it will provide a more usefull error message 👍" ) 
            embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
            await ctx.reply(embed=embed)
            embed.clear_fields()
            embed.remove_author()

    user = ""
    WalletName = ""
    data = ""
    response = ""
    json = ""
    embed.clear_fields()
    embed.remove_author()

# receive funds
@slash.slash(description='get an address')
async def receive(ctx):
    await ctx.defer()
    embed.clear_fields()
    embed.remove_author()

    user = ctx.author.id 
    WalletName = hashlib.md5(str(user).encode('utf-8')).hexdigest()
    data = '{"jsonrpc": "1.0", "id": "curltest", "method": "getnewaddress", "params": []}' 
    response = requests.post(RPChost+'wallet/'+str(WalletName), headers=headers, data=data, auth=(RPCuser, RPCpass)) 
    json = response.json() 
    if (str(json["error"])) == "None":
        embed.add_field(name='New address is:', value=json["result"])
        embed.set_author(name=str(ctx.author) + "'s", icon_url=(ctx.author).avatar_url)
        await ctx.reply(embed=embed)
        embed.clear_fields()
        embed.remove_author()
    else:
        if (json["error"])["message"] == "Requested wallet does not exist or is not loaded":
            embed.add_field(name="Error!", value="Oops! wallet does not exist, please run " + prefix +"create")
            embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
            await ctx.reply(embed=embed)
            embed.clear_fields()
            embed.remove_author()
        else:
            embed.add_field(name="Error!", value="Undefined error, please send error code: "+ "``" +str(json["error"]) +"``" + "to " +Contact + ", this error code will be added to the database and it will provide a more usefull error message 👍" ) 
            embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
            await ctx.reply(embed=embed)
            embed.clear_fields()
            embed.remove_author()
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + str(ctx.author) + " Experienced undefined error: " +str(json["error"]))

    user = ""
    WalletName = ""
    data = ""
    response = ""
    json = ""
    embed.clear_fields()
    embed.remove_author()


# list transactions
@slash.slash(description='list transactions')
async def list_transactions(ctx, tx_asked:int=10):
        await ctx.defer()
        embed.clear_fields()
        embed.remove_author()
       
        ValueError=False
        if(tx_asked==0): await ctx.reply('https://tenor.com/view/house-explosion-explode-boom-kaboom-gif-19506150'); ValueError=True

        if not ValueError==True:
            user = ctx.author.id
            WalletName = hashlib.md5(str(user).encode('utf-8')).hexdigest()
            data = '{"jsonrpc": "1.0", "id": "curltest", "method": "getwalletinfo", "params": []}'
            response = requests.post(RPChost+'wallet/'+str(WalletName), headers=headers, data=data, auth=(RPCuser, RPCpass))
            json = response.json()

            if not json["error"] == None:
                if (json["error"])["message"] == "Requested wallet does not exist or is not loaded":
                    embed.add_field(name="Error!", value="Oops! wallet does not exist, please run " + prefix +"create")
                    embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                    await ctx.reply(embed=embed)
                    embed.clear_fields()
                    embed.remove_author()
                else:
                    embed.add_field(name="Error!", value="Undefined error, please send error code: "+ "``" +str(json["error"]) +"``" + "to " +Contact + ", this error code will be added to the database and it will provide a more usefull error message 👍" ) 
                    embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                    await ctx.reply(embed=embed)
                    embed.clear_fields()
                    embed.remove_author()
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + str(ctx.author) + " Experienced undefined error: " +str(json["error"]))
            else:
                embed.add_field(name="Transactions:", value='\n\u200b')
                lastTX=''
                for i in range (1,tx_asked+1):
                    data = '{"jsonrpc": "1.0", "id": "curltest", "method": "listtransactions", "params": ["*", '+str(i) +']}'
                    response = requests.post(RPChost+'wallet/'+str(WalletName), headers=headers, data=data, auth=(RPCuser, RPCpass))
                    json = response.json() 
                    json = json["result"]

                    if not lastTX==str(json[0]["txid"]):
                        if (json[0]["category"]=='receive'): embed.add_field(name=f"You received " + str(decimal.Decimal(str(json[0]["amount"]))).replace('+', '') + str(" ") + str(Cointicker) + str(" at: ") +str(str(datetime.utcfromtimestamp(int(json[0]["time"])))), value=(f" **From address:** " + str(json[0]["address"]) + str(" [explorer]" + explorer + str(json[0]["txid"]) + str(")")) + "\n **Confirmations:** " +str(json[0]["confirmations"])), inline=False); lastTX=str(json[0]["txid"])
                        if (json[0]["category"]=='send'): embed.add_field(name=f"You sent: " + str(decimal.Decimal(str(json[0]["amount"]))).replace('-', '') + str(" ") + str(Cointicker) + str(" at: ") +str(str(datetime.utcfromtimestamp(int(json[0]["time"])))) , value=(f" **To address:** " + str(json[0]["address"]) + str(" [explorer](" + explorer + str(json[0]["txid"]) + str(")" + "\n **Confirmations:** " +str(json[0]["confirmations"])))), inline=False);        lastTX=str(json[0]["txid"])
                embed.set_author(name=str(ctx.author) + "'s", icon_url=(ctx.author).avatar_url)
                await ctx.reply(embed=embed)
                embed.clear_fields()
                embed.remove_author()
        
        user = ""
        WalletName = ""
        data = ""
        response = ""
        json = ""
        lastTX=""
        embed.clear_fields()
        embed.remove_author()



    
#Enable 2FA
@slash.slash(description='enable 2fa')
async def enable2fa(ctx):
    await ctx.defer()
    embed.clear_fields()
    embed.remove_author()

    doc_ref = db.collection(Collection).document(str(ctx.author.id))
    doc = doc_ref.get()

    temp_doc_ref = db.collection(tempCollection).document(str(ctx.author.id))
    temp_doc = temp_doc_ref.get()

    if doc.exists:
        embed.add_field(name='...', value="Woah slow down there busta'! You can only enable 2FA once!")
        embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
        await ctx.reply(embed=embed)
        embed.clear_fields()
        embed.remove_author()

    if not doc.exists:
        base32secret = pyotp.random_base32()
        temp_doc_ref.set({
            u'base32Secret': base32secret,
            })
        embed.add_field(name='info ℹ', value='open your favorite authenticator app ready and open the QR code scanning tool, and scan this code. You may run it again if needed, once you scanned it run ``' + prefix + 'verify``' + 'to make the OTP reqiured on the ``' + prefix + "send`` command")
        embed.add_field(name='Warning ⚠', value='once you scanned the QR code and ran ``' + prefix + 'verify`` **please click dismiss message!**')
        embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
        await ctx.reply(embed=embed, hidden=True)
        embed.clear_fields()
        embed.remove_author()
        totp_uri = 'otpauth://totp/' + Cointicker + ' Discord Wallet?secret=' + base32secret
        #QR gen
        qr.add_data(totp_uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save('qrcode.png')
        qr.clear()
        #Send the QR code
        await ctx.reply(file=discord.File('qrcode.png'), hidden=True)
        os.remove("qrcode.png")

   

       
       
# verify 2FA
@slash.slash(description='Verify that you have setup 2FA successfully')
async def verify(ctx, otp_input:int):
    await ctx.defer()
    embed.clear_fields()
    embed.remove_author()

    doc_ref = db.collection(Collection).document(str(ctx.author.id))
    doc = doc_ref.get()

    temp_doc_ref = db.collection(tempCollection).document(str(ctx.author.id))
    temp_doc = temp_doc_ref.get()

    if doc.exists:
        totp = pyotp.TOTP(doc.to_dict()["base32Secret"])
        if int(totp.now())==int(otp_input):
            embed.add_field(name="I'm speachless...", value="Well... the OTP is correct, but you can't re-enable 2FA ¯\_(ツ)_/¯")
            embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
            await ctx.reply(embed=embed)
            embed.clear_fields()
            embed.remove_author()
        else:
            embed.add_field(name='Dude...', value="The OTP is incorrect, and you can't re-enable 2FA ;-;")
            embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
            await ctx.reply(embed=embed)
            embed.clear_fields()
            embed.remove_author()

    if temp_doc.exists and not doc.exists:
        totp = pyotp.TOTP(temp_doc.to_dict()["base32Secret"])
        if int(totp.now())==int(otp_input):

            doc_ref.set({
            u'base32Secret': temp_doc.to_dict()["base32Secret"],
            })
            temp_doc_ref.delete()

            embed.add_field(name="Success!", value="The OTP was correct! You can now use it with the ``" + prefix +"send`` command👍" )
            embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
            await ctx.reply(embed=embed)
            embed.clear_fields()
            embed.remove_author()
        else:
            embed.add_field(name='Dude...', value="The OTP was incorrect... Try again :grimacing:")
            embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
            await ctx.reply(embed=embed)
            embed.clear_fields()
            embed.remove_author()
        
    if not temp_doc.exists and not doc.exists:
        embed.add_field(name='Error!', value="Please run ``" + prefix + "enable2fa`` first!")
        embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
        await ctx.reply(embed=embed)
        embed.clear_fields()
        embed.remove_author()




# send a transaction
@slash.slash(description='Send a Transaction')
async def send(ctx, amount, to_address, otp_input=0):
    await ctx.defer()
    embed.clear_fields()
    embed.remove_author()
    
    doc_ref = db.collection(Collection).document(str(ctx.author.id))
    doc = doc_ref.get()
            

    if doc.exists: 
        totp = pyotp.TOTP(doc.to_dict()['base32Secret'])

        if int(totp.now())==int(otp_input):
            user = ctx.author.id
            WalletName = hashlib.md5(str(user).encode('utf-8')).hexdigest()
            data = '{"jsonrpc": "1.0", "id":"curltest", "method": "sendtoaddress", "params": ["' +str(to_address) +'", '+str(amount) +'] }'
            response = requests.post(RPChost+'wallet/'+str(WalletName), headers=headers, data=data, auth=(RPCuser, RPCpass))
            json = response.json()
            if json["error"] == None:
                embed.add_field(name='Success!', value='You sucsessfully sent '+str(amount) + " " +Cointicker + ' to: ' + str(to_address) + str(" [explorer](" + explorer + str(json["result"]) + str(")") + " TX ID: " + "\n" + str(json["result"])  ))
                embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                await ctx.reply(embed=embed)
                embed.clear_fields()
                embed.remove_author()
            else:
                if (json["error"])["message"] == "Insufficient funds":
                    data = '{"jsonrpc": "1.0", "id":"curltest", "method": "getbalance", "params": [] }'
                    response = requests.post(RPChost+'wallet/'+str(WalletName), headers=headers, data=data, auth=(RPCuser, RPCpass))
                    json = response.json() 
                    embed.add_field(name="Error!", value="Oops! You have insuficient funds, you only have: " + str(json['result']) + " " + Cointicker)
                    embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                    await ctx.reply(embed=embed)
                    embed.clear_fields()
                    embed.remove_author()
                else:
                    if (json["error"])["message"] == "Invalid address":
                        embed.add_field(name="Error!", value="Oops! Invalid address ;-;")
                        embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                        await ctx.reply(embed=embed)
                        embed.clear_fields()
                        embed.remove_author()
                    else:
                        if doc.exists and otp_input==0:
                            embed.add_field(name='Error!',value="Please enter the OTP after the address!")
                            embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                            await ctx.reply(embed=embed)
                            embed.clear_fields()
                            embed.remove_author()
                        else:
                            if (json["error"])["message"] == "Transaction amount too small":
                                embed.add_field(name="Error!", value="Transaction amount too small, please increase it")
                                embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                                await ctx.reply(embed=embed)
                                embed.clear_fields()
                                embed.remove_author()
                            else:
                                if (json["error"])["message"] == "Requested wallet does not exist or is not loaded":
                                    embed.add_field(name="Error!", value="Oops! wallet does not exist, please run " + prefix +"create")
                                    embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                                    await ctx.reply(embed=embed)
                                    embed.clear_fields()
                                    embed.remove_author()
                                else:
                                    embed.add_field(name="Error!", value="Undefined error, please send error code: "+ "``" +str(json["error"]) +"``" + "to " +Contact + ", this error code will be added to the database and it will provide a more usefull error message 👍" ) 
                                    embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                                    await ctx.reply(embed=embed)
                                    embed.clear_fields()
                                    embed.remove_author()
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + str(ctx.author) + " Experienced undefined error: " +str(json["error"]))
        else:
            if doc.exists and otp_input!=0:
                embed.add_field(name='Error!', value="Wrong OTP!")
                embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                await ctx.reply(embed=embed)
                embed.clear_fields()
                embed.remove_author()

            if doc.exists and otp_input==0:
                embed.add_field(name='Error!', value="Please specify the OTP!")
                embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                await ctx.reply(embed=embed)
                embed.clear_fields()
                embed.remove_author()


                    

    if not doc.exists:
        user = ctx.author.id 
        WalletName = hashlib.md5(str(user).encode('utf-8')).hexdigest()
        data = '{"jsonrpc": "1.0", "id":"curltest", "method": "sendtoaddress", "params": ["' +str(to_address) +'", '+str(amount) +'] }'
        response = requests.post(RPChost+'wallet/'+str(WalletName), headers=headers, data=data, auth=(RPCuser, RPCpass))
        json = response.json() 

        if json["error"] == None:
            embed.add_field(name='Success!', value='You sucsessfully sent '+str(amount) + " " +Cointicker + ' to: ' + str(to_address) + str(" [explorer](" + explorer + str(json["result"]) + str(")") + " TX ID: " + "\n" + str(json["result"])  ))
            embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
            await ctx.reply(embed=embed)
            embed.clear_fields()
            embed.remove_author()
        else:
            if (json["error"])["message"] == "Insufficient funds":
                data = '{"jsonrpc": "1.0", "id":"curltest", "method": "getbalance", "params": [] }'
                response = requests.post(RPChost+'wallet/'+str(WalletName), headers=headers, data=data, auth=(RPCuser, RPCpass))
                json = response.json() 
                embed.add_field(name="Error!", value="Oops! You have insuficient funds, you only have: " + str(json['result']) + " " + Cointicker)
                embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                await ctx.reply(embed=embed)
                embed.clear_fields()
                embed.remove_author()
            else:
                if (json["error"])["message"] == "Invalid address":
                    embed.add_field(name="Error!", value="Oops! Invalid address ;-;")
                    embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                    await ctx.reply(embed=embed)
                    embed.clear_fields()
                    embed.remove_author()
                else:
                    if (json["error"])["message"] == "Transaction amount too small":
                        embed.add_field(name="Error!", value="Transaction amount too small, please increase it")
                        embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                        await ctx.reply(embed=embed)
                        embed.clear_fields()
                        embed.remove_author()
                    else:
                        if (json["error"])["message"] == "Requested wallet does not exist or is not loaded":
                            embed.add_field(name="Error!", value="Oops! wallet does not exist, please run " + prefix +"create")
                            embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                            await ctx.reply(embed=embed)
                            embed.clear_fields()
                            embed.remove_author()
                        else:
                            embed.add_field(name="Error!", value="Undefined error, please send error code: "+ "``" +str(json["error"]) +"``" + "to " +Contact + ", this error code will be added to the database and it will provide a more usefull error message 👍" ) 
                            embed.set_author(name=str(ctx.author), icon_url=(ctx.author).avatar_url)
                            await ctx.reply(embed=embed)
                            embed.clear_fields()
                            embed.remove_author()
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + str(ctx.author) + " Experienced undefined error: " +str(json["error"]))
    user = ""
    WalletName = ""
    data = ""
    response = ""
    json = ""
    embed.clear_fields()
    embed.remove_author()
            

                    

        
bot.run(DiscordToken) # inputs your auth token
