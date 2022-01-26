""":cvar
pip3 uninstall telebot
pip3 uninstall PyTelegramBotAPI
pip3 install pyTelegramBotAPI
pip3 install --upgrade pyTelegramBotAPI
"""
try:
    import cv2
    import PIL.Image as Image
    import io
    import base64
    #from byte_array import byte_data

    import telebot
    import config
    import random
    from telebot import util, types
    import Alg
    import DiscretAlg
    import Factorization
    import primeTests
    import time , steganography
    bot = telebot.TeleBot(config.TOKEN)
    #help(bot)
    #print(getStickerSet())
    print("Bot is started")
    imagesPath = ''
    LENGTH = 15
    state = ''
    msg2Hide = ''

    hideInfo = False
    HK = 1

    #zzss = steganography.flatImage()

    def buildMainMenu(buttons):
        global stegoOp
        stegoOp = ''
        mainmn = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        for i,v in buttons.items():
            tmp = types.InlineKeyboardButton(i, callback_data=v)
            mainmn.add(tmp)
        return mainmn

    def buildInternalMenu(buttons):
        itemTmp = []
        for i, v in buttons.items():
            itemTmp.append([types.InlineKeyboardButton(i,callback_data=v)])
        return types.InlineKeyboardMarkup(itemTmp)


    def intt(x):
        z= []
        for i in x:
            z.append(int(i))
        return z


    mainMenu =  buildInternalMenu(
        {"RSA": "1",
         "EL-Gamal": "2",
         "Inv mod": "3",
         "BinPow": "4",
         "Prime": "5",
         "DigitalSignature": "10",
         "Factorization p": "6",
         "Discrete alg(Shanks’ baby-step/giant-step)": "7",
         "Elliptic curve": "8",
         "Steganograph": "9",
         "About":"100"})


    #buildMainMenu
    RSAMenu = buildInternalMenu({"RSA Encryption":"20",
                                 "RSA Decryption":"21",
                                 "RSA Genrate keys":"20.1",
                                 "Main menu":"00"})
    GAMALMenu = buildInternalMenu({"GAMAL Encryption": "30",
                                   "GAMAL Decryption":"31",
                                   "Main menu": "00"})

    primeMenu = buildInternalMenu({"is prime": "40",
                                   "Generate prime": "41",
                                   #"fractional": "52",
                                   "Main menu": "00"})

    primeCheckMenu = buildInternalMenu({"Trial Division Method": "50",#xxxxxxxxxxx
                                        "Chinese Test": "501",#xxxxx
                                        "Fermat Test": "502",
                                        "Miller Test": "51",#xxxxx
                                        "Miller-Rabin": "52",
                                        "Main menu": "00"})

    primeFractionMenu = buildInternalMenu({"Fermat": "60",
                                           "Polard p-1": "61",
                                           "Monte carlo": "62",#xxxxxx
                                           "Main menu": "00"})

    ellipticMenu = buildInternalMenu({"findPoints": "70",
                                        "isGenerator": "71",
                                       "Main menu": "00"})

    DigSignMenu = buildInternalMenu({"RSA_DS": "80",
                                     "El-Gamal_DS": "81",
                                     "Elliptic-curve_DS": "82",#xxxxxxxxx
                                     "Main menu": "00"})
    stegoMenu = buildInternalMenu({"Hide": "110",
        "Extract": "111",
        "Main menu": "00"})
        
    @bot.message_handler(commands=['start'])
    def welcome(message):
        sti = open(imagesPath + 'logo.tgs', 'rb')
        bot.send_sticker(message.chat.id,sti)
        time.sleep(1)
        bot.send_message(message.chat.id,
                         "Hello, {0.first_name}!\nWelcome - <b>{1.first_name}</b>, to help you.\n\n\n****please use space instead of comma****".format(
                             message.from_user, bot.get_me()),
                         parse_mode='html', reply_markup=mainMenu)#mainMenu
        
    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        global state
        #if True:
        try:
            if call.message:
                if call.data == '00':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Select" , reply_markup=mainMenu)
                elif call.data == '1':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Select" , reply_markup=RSAMenu)
                    #bot.send_message(call.message.chat.id, "Select", parse_mode='html', reply_markup=RSAMenu)
                elif call.data == '2':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Select" , reply_markup=GAMALMenu)
                elif call.data == '3':
                    bot.send_message(call.message.chat.id, "Enter x,p (x^-1 mod p)", parse_mode='html', reply_markup=None)
                elif call.data == '4':
                    bot.send_message(call.message.chat.id, "Enter x,y,p (x^y mod p)", parse_mode='html', reply_markup=None)
                elif call.data == '5':
                    bot.send_message(call.message.chat.id, "Select", parse_mode='html', reply_markup=primeMenu)
                elif call.data == '6':
                    bot.send_message(call.message.chat.id, "Select", parse_mode='html', reply_markup=primeFractionMenu)
                elif call.data == '7':
                    bot.send_message(call.message.chat.id, "Enter h,g,p(h = g^x mod p)", parse_mode='html', reply_markup=None)
                elif call.data == '8':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Select" , reply_markup=ellipticMenu)
                elif call.data == '9':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Select" , reply_markup=stegoMenu)
                elif call.data == '10':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "Select" , reply_markup=DigSignMenu)
                elif call.data == '20':
                    bot.send_message(call.message.chat.id, "Enter m,e,p,q or m,e,n or m", parse_mode='html',reply_markup=None)
                elif call.data == '20.1':
                    bot.send_message(call.message.chat.id, "Enter p q e or Any number", parse_mode='html',reply_markup=None)
                elif call.data == '21':
                    bot.send_message(call.message.chat.id, "Enter c,d,n", parse_mode='html',reply_markup=None)
                elif call.data == '30':

                    bot.send_message(call.message.chat.id, "Enter m,p,g,x,k or m", parse_mode='html',reply_markup=None)
                elif call.data == '31':
                    bot.send_message(call.message.chat.id, "Enter a,b,p,g", parse_mode='html', reply_markup=None)
                elif call.data == '40':
                    bot.send_message(call.message.chat.id, "Select", parse_mode='html', reply_markup=primeCheckMenu)
                elif call.data == '41':
                    bot.send_message(call.message.chat.id, "Enter length(bits)", parse_mode='html',reply_markup=None)
                elif call.data == '50':
                    bot.send_message(call.message.chat.id, "Enter x", parse_mode='html',reply_markup=None)
                elif call.data == '50'or call.data == '501':
                    bot.send_message(call.message.chat.id, "Enter p to test", parse_mode='html',reply_markup=None)
                elif  call.data == '502':
                    bot.send_message(call.message.chat.id, "Enter p,b", parse_mode='html',reply_markup=None)                
                elif call.data == '51':
                    bot.send_message(call.message.chat.id, "Under development", parse_mode='html',reply_markup=None)                
                    #bot.send_message(call.message.chat.id, "Enter x, (*)", parse_mode='html',reply_markup=None)
                elif call.data == '52':
                    bot.send_message(call.message.chat.id, "Enter n,k", parse_mode='html',reply_markup=None)
                elif call.data == '60':
                    bot.send_message(call.message.chat.id, "Enter n", parse_mode='html', reply_markup=None)
                elif call.data == '61':
                    bot.send_message(call.message.chat.id, "Enter n(r0 =2)", parse_mode='html',reply_markup=None)
                elif call.data == '62':
                    bot.send_message(call.message.chat.id, "Under development", parse_mode='html',reply_markup=None)                
                    #bot.send_message(call.message.chat.id, "Enter n, m0", parse_mode='html',reply_markup=None)
                elif call.data == '70':
                    bot.send_message(call.message.chat.id, "Enter field, X (11 1 0 -8 -5)", parse_mode='html',reply_markup=None)
                elif call.data == '71':
                    bot.send_message(call.message.chat.id, "Enter x,y,field,X (9 5 11 1 0 -8 -5)", parse_mode='html',reply_markup=None)
                elif call.data == '80':
                    bot.send_message(call.message.chat.id, "Enter s msg |v msg c pub_key", parse_mode='html',reply_markup=None)
                elif call.data == '81':
                    bot.send_message(call.message.chat.id, "Enter s msg| v msg,c,pub_key", parse_mode='html',reply_markup=None)
                elif call.data == '82':
                    bot.send_message(call.message.chat.id, "Under development", parse_mode='html',reply_markup=None)                
                    #bot.send_message(call.message.chat.id, "xxxxxxxxxxxx", parse_mode='html',reply_markup=None)
                elif call.data == '100':
                    bot.send_message(call.message.chat.id, "Mohammed Hammoud\nOla Haydar", parse_mode='html',reply_markup=None)
                elif call.data == '110':
                    bot.send_message(call.message.chat.id, "Enter image and text in caption", parse_mode='html',reply_markup=None)
                elif call.data == '111':
                    bot.send_message(call.message.chat.id, "Enter image and hk in caption", parse_mode='html',reply_markup=None)

                state = call.data
                print(state)
        except Exception as e:
            print(repr(e))

    @bot.message_handler(content_types=['photo'])
    def handle_file(message):
        global state, hideInfo, msg2Hide, HK
        print("*******************1")
        stegoOp = 'hide'
        if False:# stegoOp == '':
            bot.reply_to(message, "*******************1")
        else:
            file_info = bot.get_file(message.photo[-1].file_id)
            tmp = bot.download_file(file_info.file_path)
            #file_name= message.photo[-1].file_id +".png"
            file_name= "tempImg.png"
            src1 = file_name
            with open(src1,'wb') as new_file:
                new_file.write(tmp)
            coverImage = cv2.imread(src1)

            if stegoOp == 'hide':
                msg2Hide, HK = message.caption.split('@')
                HK = int(HK)
                stegoImg,mse,psnr = steganography.hideLSB(msg2Hide,coverImage,0)

                file_name= "stego.png"
                src2 = file_name
                cv2.imwrite(src2, stegoImg)
                stegoImg = cv2.imread(src2)

                RESULTS = 'Cover Image \nmsg: {}\nhideKey: {}\nmse = {}\npsnr = {}'.format(msg2Hide, HK, mse, psnr)
                bot.send_photo(message.chat.id,photo = open(src2,'rb'),caption = RESULTS)

            elif stegoOp == 'extract':
                HK = int(message.caption.text)
                data, h, date = steganography.extractLSB(coverImage,HK)
                RESULTS = 'Hidekey: {}data\nh = {}\ndate = {}'.format(HK, date, h == steganography.calcHash(date) , date)
                bot.reply_to(message, RESULTS)             


    @bot.message_handler(content_types=['text'])
    def lalala(message):
        global state, hideInfo, msg2Hide, HK
        staegoOp = ''
        #if True:
        try:
            print(state)
            if message.chat.type == 'private':
                #I = intt(message.text.split())
                if state == '3':
                    I = intt(message.text.split())
                    x, p = I
                    z = Alg.findModInverse(x, p)
                    if z != "Error":
                        bot.send_message(message.chat.id, str(z), parse_mode='html', reply_markup=None)
                    else:
                        bot.send_message(message.chat.id, "gcd(x,p) !=1", parse_mode='html', reply_markup=None)
                elif state == '4':
                    I = intt(message.text.split())
                    x, y, p = I
                    z = Alg.BPower(x, y, p)
                    bot.send_message(message.chat.id, str(z), parse_mode='html', reply_markup=None)
                elif state == '7':
                    I = intt(message.text.split())
                    h,g,p = I
                    z = DiscretAlg.bsgs(h,g,p)
                    bot.send_message(message.chat.id, "x = {}".format(z), parse_mode='html', reply_markup=None)
                elif state == '9':
                    bot.send_message(call.message.chat.id, "Enter text, HideKey", parse_mode='html', reply_markup=None)
                elif state == '20':
                    I = intt(message.text.split())
                    if len(I) == 1:
                        m = I
                        [(e, n),(d, n)] = Alg.RSA_genrate_keys(LENGTH)
                        z = Alg.RSA_enc(m,e,n)
                    elif  len(I) == 3:
                        m, e, n = I
                        z = Alg.RSA_enc(m,e,n)
                        d = '?'
                    else:
                        m, e, p, q = I
                        n = p * q
                        z = Alg.RSA_enc(m,e,n)
                        d = Alg.findModInverse(e,(p-1)*(q-1))
                    bot.send_message(message.chat.id, "msg = {}\nCipher = {}\ne = {}\nd = {}\nn = {}".format(m,z, e, d, n), parse_mode='html', reply_markup=None)
                elif state == '20.1':
                    I = intt(message.text.split())
                    if len(I) == 1:
                        z = Alg.RSA_genrate_keys(20)
                    else:
                        z = Alg.RSA_genrate_keys(20,(I[0],I[1],I[2]))

                    bot.send_message(message.chat.id, "global{}\nprivate{}".format(z[0],z[1]), parse_mode='html', reply_markup=None)

                elif state == '21':
                    I = intt(message.text.split())
                    c, d, n = I
                    z = Alg.RSA_dec(c,d,n)
                    bot.send_message(message.chat.id, "msg {}".format(z), parse_mode='html', reply_markup=None)
                elif state == '30':
                    I = intt(message.text.split())
                    if len(I) == 1:
                        m = I
                        ((y, g, p),(x, g, p)) = Alg.AlGamal_Genkeys("",LENGTH)
                        (a, b) = Alg.AlGamal_Enc(m, (y, g, p))
                    elif len(I) == 5:
                        m, p, g, x, k = I
                        ((y, g, p),(x, g, p)) = Alg.AlGamal_Genkeys((p,g,x),LENGTH)
                        (a, b) = Alg.AlGamal_Enc(m, (y, g, p), k = k)
                    bot.send_message(message.chat.id, "msg {}\nCipher {} \npublic {}\nprivate {}\n".format(m, (a,b),(y,g,p),(x,g,p)), parse_mode='html', reply_markup=None)
                elif state == '41':
                    n = intt(message.text.split())
                    z = Alg.generate_prime_number(n[0])
                    bot.send_message(message.chat.id, "p = {}".format(z), parse_mode='html', reply_markup=None)
                elif state == '50':
                    n = intt(message.text.split())
                    z = primeTests.trialDevision(n[0])
                    bot.send_message(message.chat.id, "p = {} primility is {} ".format(n[0],z), parse_mode='html', reply_markup=None)
                elif state == '501':
                    n = intt(message.text.split())
                    z = primeTests.chinesTest(n[0])
                    bot.send_message(message.chat.id, "p = {} primility is {} ".format(n[0],z), parse_mode='html', reply_markup=None)
                elif state == '502':
                    p, b = intt(message.text.split())
                    z = primeTests.fermatTest(p, b)
                    bot.send_message(message.chat.id, "p = {}, b = {} primility is {} ".format(p,b,z), parse_mode='html', reply_markup=None)
                elif state == '51':
                    pass
                    #n = intt(message.text.split())
                    #z = primeTests.millerTest(n[0])
                    #bot.send_message(message.chat.id, "p = {} primility is {} ".format(n[0],z), parse_mode='html', reply_markup=None)
                elif state == '52':
                    n, k = intt(message.text.split())
                    z = primeTests.isPrimeMillerRabin(n,k)
                    bot.send_message(message.chat.id, "{} prime \n {}".format(n,z), parse_mode='html', reply_markup=None)
                elif state == '60':
                    n = intt(message.text.split())
                    z = Factorization.factorFermat(n[0])
                    bot.send_message(message.chat.id, "n = {} :\n {}".format(n[0],z), parse_mode='html', reply_markup=None)
                elif state == '61':
                    n = intt(message.text.split())
                    z = Factorization.factoPollard(n[0],2)
                    bot.send_message(message.chat.id, "n = {}\nr0 = {} :\n {}".format(n,r0, z), parse_mode='html', reply_markup=None)
                elif state == '62':
                    pass
                    #z = Factorization.doit(n)
                elif state == '70':
                    I = intt(message.text.split())
                    ALL = I
                    field = ALL[0]
                    X = ALL[1:]
                    (L,points) = Alg.FindPonts(X, field)
                    bot.send_message(message.chat.id, "numberOfPoints = {}\n Points = {}".format(L,points), parse_mode='html', reply_markup=None)
                elif state == '71':
                    I = intt(message.text.split())
                    ALL = I
                    point = ALL[0:2]
                    field = ALL[2]
                    X = ALL[3:]
                    print(point, field, X)
                    (Ggroup, allpoints, ISgenerated, logger) = Alg.isgenerator((point[0],point[1]), X, field)
                    bot.send_message(message.chat.id, "Ggroup {}\nall points = {}\n IS generater = {}\n logger {}".format(Ggroup, allpoints, ISgenerated, logger), parse_mode='html',reply_markup=None)
                elif state == '80':
                    rec = message.text.split()
                    op = rec[0]
                    msg = rec[1]
                    if op == 's':
                        (h1, c, priv_key,pub_key) = Alg.DS_RSA(msg)
                        bot.send_message(message.chat.id,"msg = {}\nh( {} ) = {}\nC = {}\npriv_key(d,n) = {}\npub_key(e,n) = {}".format(msg, h1, c,priv_key,pub_key), parse_mode='html', reply_markup=None)
                    elif op == 'v':
                        c = rec[2]
                        pub_key = (rec[3], rec[4])
                        z = Alg.DS_RSA_verify(msg, c, pub_key)
                        bot.send_message(message.chat.id,"signature is {}".format(z), parse_mode='html', reply_markup=None)
                elif state == '81':
                    rec = message.text.split()
                    op =  rec[0]
                    msg = rec[1]
                    if op == 's':
                        (c, pub_key, priv_key) = Alg.DS_Algamal(msg)
                        bot.send_message(message.chat.id,"msg = {}\nC = {}\npub_key(y, g, p) = {}\npriv_key(x, g, p) = {}".format(msg, c, pub_key,priv_key), parse_mode='html', reply_markup=None)
                    elif op == 'v':
                        c = rec[2]
                        pub_key = (rec[3], rec[4],rec[5])
                        z = Alg.DS_Algamal_verify(msg, c, pub_key)
                        bot.send_message(message.chat.id,"signature is {}".format(z), parse_mode='html', reply_markup=None)
                elif state == '110':
                    bot.send_message(message.chat.id, "Enter image and text in caption", parse_mode='html', reply_markup=None)
                    stegoOp = 'hide'
                elif state == '111':
                    stegoOp = 'extract'
                elif state == '82':
                    pass
                elif state == '82':
                    pass

                else:
                    bot.reply_to(message, 'Sorry what is this!!!')
        except Exception as e:
            bot.reply_to(message, 'Uncorrect input')

    # RUN
    bot.polling(none_stop=True)
except Exception as e:
    bot.polling(none_stop=True)
