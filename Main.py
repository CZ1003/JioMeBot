import telepot, time

bot = telepot.Bot('387099409:AAFmM5sismztGNYvfUo388Bn9QeEhUUcce8')

def handle(msg):
     chat_id = msg['chat']['id']
     command = msg['text']
     print ('Got command: %s' % command)

     if command == '/hello':
        bot.sendMessage(chat_id, "Hello, how are you?")
     elif command == '/Iloveyou':
        bot.sendMessage(chat_id, "AWWW, I love you too!")
        s = bot.exportChatInviteLink(chat_id)
        bot.sendMessage(chat_id, s)
     elif command == 'TestingGit':
         bot.sendMessage(chat_id, "It works..")



bot.message_loop(handle)
while 1:
     time.sleep(10)