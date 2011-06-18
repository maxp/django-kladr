# -*- coding: utf-8 -*-

'''
    mxlab.com: kladr.models
'''

import logging; log = logging.getLogger(__name__)

from django.db import models, connection


_LEVEL_POS = [0, 2, 5, 8, 11, 15]

class Socr(models.Model):
    socr    = models.CharField( max_length=10, primary_key=True )   # duplicated values allowed!
    name    = models.CharField( max_length=29 )
    level   = models.CharField( max_length=5 )
    tcode   = models.CharField( max_length=3 )
    
    class Meta:
        managed = False
        
    def save(self):
        '''disabled'''
        return False
#---

class Kladr(models.Model):
    code    = models.CharField( max_length=13, primary_key=True )   # SS RRR GGG PPP AA
    level   = models.IntegerField()                 # 1..4
    name    = models.CharField( max_length=40 )
    socr    = models.CharField( max_length=10 )
    stat    = models.CharField( max_length=1 )
    indx    = models.CharField( max_length=6 )

    class Meta:
        managed = False
        
    def save(self):
        '''disabled'''
        return False
#---

class Street(models.Model):
    code    = models.CharField( max_length=17, primary_key=True )   # SS RRR GGG PPP UUUU AA
    # level == 5
    name    = models.CharField( max_length=40 )
    socr    = models.CharField( max_length=10 )
    indx    = models.CharField( max_length=6 )

    class Meta:
        managed = False
        
    def save(self):
        '''disabled'''
        return False
#---


def list_level( code, level ):
    
    if level == 5:
        sql, c = "kladr_street where substr(code,1,11)=%(code)s", code[:11]
    elif level == 4:
        sql, c = "kladr_kladr where level=%(level)s and substr(code,1,8)=%(code)s", code[:8]
    elif level == 3:
        sql, c = "kladr_kladr where level=%(level)s and substr(code,1,5)=%(code)s", code[:5]
    elif level == 2:
        sql, c = "kladr_kladr where level=%(level)s and substr(code,1,2)=%(code)s", code[:2]
    elif level == 1:
        sql, c = "kladr_kladr where level=%(level)s", ''
    else:
        return ["","",""]

    curs = connection.cursor()  #@UndefinedVariable
    curs.execute( 
        "select code,name,socr from "+sql+" order by name,code", 
            {'level':level, 'code':c} 
    )
    res = curs.fetchall()
    curs.close()
    return res
#--


def by_code( code, level ):

    if level < 1 or level > 5:
        return None
    
    code = code[: _LEVEL_POS[level] ]
    
    if level == 5:
        code += '0'*(15-len(code))
        sql = "kladr_street where substr(code,1,15)=%(code)s"
    else:
        code += '0'*(11-len(code))
        sql = "kladr_kladr where substr(code,1,11)=%(code)s and level=%(level)s"
    #-
        
    curs = connection.cursor()  #@UndefinedVariable
    curs.execute( "select code,name,socr from "+sql+" order by code limit 1", 
                  { 'code':code,'level':level } ) 
    res = curs.fetchone()
    curs.close()
    return res
#--

def code_level(code):
    for i in (5,4,3,2,1):
        c = code[ _LEVEL_POS[i-1] : _LEVEL_POS[i] ]
        try:
            if c and int(c):
                return i
        except ValueError:
            return 0
    return 0
#--
    
def code_text( code ):
    lvl = code_level( code )
    if not lvl:
        return ""
    
    res = []
    
    if code[0:5] != '38000':
        k = by_code( code, 1 )
        if k:
            res.append( _SOCR_FMT.get( k[2], k[2]+u". %s" ) % k[1] )
             
    for i in range(1,lvl):
        k = by_code( code, i+1 )
        if k:
            res.append( _SOCR_FMT.get( k[2], k[2]+u". %s" ) % k[1] )
             
    return ", ".join( res )
#--
        
_SOCR_FMT = {

    u"АО":      u"%s АО",
    u"Аобл":    u"%s Аобл.",
    u"г":       u"г. %s",
    u"край":    u"%s край",
    u"обл":     u"%s обл.",
    u"Респ":    u"Респ. %s",
    u"округ":   u"%s округ",
    u"р-н":     u"%s р-н",
            
# у          | Улус                          | 2     | 202
# тер        | Территория                    | 2     | 203
# кожуун     | Кожуун                        | 2     | 204
# АО         | Автономный округ              | 2     | 205
# г          | Город                         | 3     | 301
# пгт        | Поселок городского типа       | 3     | 302
# рп         | Рабочий поселок               | 3     | 303
# кп         | Курортный поселок             | 3     | 304
# дп         | Дачный поселок                | 3     | 305
# с/с        | Сельсовет                     | 3     | 306
# с/а        | Сельская администрация        | 3     | 307
# с/о        | Сельский округ                | 3     | 309
# волость    | Волость                       | 3     | 310
# п/о        | Почтовое отделение            | 3     | 311
# тер        | Территория                    | 3     | 312
# сумон      | Сумон                         | 3     | 313
# с/п        | Сельское поселение            | 3     | 314
# с/мо       | Сельское муниципальное образо | 3     | 315
# аал        | Аал                           | 4     | 401
# аул        | Аул                           | 4     | 402
# волость    | Волость                       | 4     | 403
# высел      | Выселки(ок)                   | 4     | 404
# г          | Город                         | 4     | 405
# д          | Деревня                       | 4     | 406
# дп         | Дачный поселок                | 4     | 407
# ж/д_будка  | Железнодорожная будка         | 4     | 408
# ж/д_казарм | Железнодорожная казарма       | 4     | 409
# ж/д_оп     | ж/д останов. (обгонный) пункт | 4     | 410
# ж/д_пост   | Железнодорожный пост          | 4     | 411
# ж/д_рзд    | Железнодорожный разъезд       | 4     | 412
# ж/д_ст     | Железнодорожная станция       | 4     | 413
# заимка     | Заимка                        | 4     | 414
# казарма    | Казарма                       | 4     | 415
# кп         | Курортный поселок             | 4     | 416
# м          | Местечко                      | 4     | 417
# мкр        | Микрорайон                    | 4     | 418
# нп         | Населенный пункт              | 4     | 419
# остров     | Остров                        | 4     | 420
# п          | Поселок                       | 4     | 421
# п/р        | Планировочный район           | 4     | 422
# п/ст       | Поселок и(при) станция(и)     | 4     | 423
# пгт        | Поселок городского типа       | 4     | 424
# починок    | Починок                       | 4     | 425
# п/о        | Почтовое отделение            | 4     | 426
# промзона   | Промышленная зона             | 4     | 427
# рзд        | Разъезд                       | 4     | 428
# рп         | Рабочий поселок               | 4     | 429
# с          | Село                          | 4     | 430
# сл         | Слобода                       | 4     | 431
# ст         | Станция                       | 4     | 432
# ст-ца      | Станица                       | 4     | 433
# у          | Улус                          | 4     | 434
# х          | Хутор                         | 4     | 435
# городок    | Городок                       | 4     | 436
# тер        | Территория                    | 4     | 437
# ж/д_платф  | Железнодорожная платформа     | 4     | 438
# кв-л       | Квартал                       | 4     | 439
# арбан      | Арбан                         | 4     | 440
# снт        | Садовое неком-е товарищество  | 4     | 441
# лпх        | Леспромхоз                    | 4     | 442
# погост     | Погост                        | 4     | 443
# кордон     | Кордон                        | 4     | 444
# автодорога | Автодорога                    | 4     | 445
# аллея      | Аллея                         | 5     | 501
# б-р        | Бульвар                       | 5     | 502
# въезд      | Въезд                         | 5     | 503
# дор        | Дорога                        | 5     | 504
# жт         | Животноводческая точка        | 5     | 505
# заезд      | Заезд                         | 5     | 506
# кв-л       | Квартал                       | 5     | 507
# км         | Километр                      | 5     | 508
# кольцо     | Кольцо                        | 5     | 509
# линия      | Линия                         | 5     | 510
# наб        | Набережная                    | 5     | 511
# остров     | Остров                        | 5     | 512
# парк       | Парк                          | 5     | 513
# пер        | Переулок                      | 5     | 514
# переезд    | Переезд                       | 5     | 515
# пл         | Площадь                       | 5     | 516
# пл-ка      | Площадка                      | 5     | 517
# проезд     | Проезд                        | 5     | 518
# пр-кт      | Проспект                      | 5     | 519
# просек     | Просек                        | 5     | 520
# проселок   | Проселок                      | 5     | 521
# проулок    | Проулок                       | 5     | 522
# сад        | Сад                           | 5     | 523
# сквер      | Сквер                         | 5     | 524
# стр        | Строение                      | 5     | 525
# тер        | Территория                    | 5     | 526
# тракт      | Тракт                         | 5     | 527
# туп        | Тупик                         | 5     | 528
# ул         | Улица                         | 5     | 529
# уч-к       | Участок                       | 5     | 530
# ш          | Шоссе                         | 5     | 531
# аал        | Аал                           | 5     | 532
# аул        | Аул                           | 5     | 533
# высел      | Выселки(ок)                   | 5     | 534
# городок    | Городок                       | 5     | 535
# д          | Деревня                       | 5     | 536
# ж/д_будка  | Железнодорожная будка         | 5     | 537
# ж/д_казарм | Железнодорожная казарма       | 5     | 538
# ж/д_оп     | ж/д останов. (обгонный) пункт | 5     | 539
# ж/д_пост   | Железнодорожный пост          | 5     | 540
# ж/д_рзд    | Железнодорожный разъезд       | 5     | 541
# ж/д_ст     | Железнодорожная станция       | 5     | 542
# казарма    | Казарма                       | 5     | 543
# м          | Местечко                      | 5     | 544
# мкр        | Микрорайон                    | 5     | 545
# нп         | Населенный пункт              | 5     | 546
# платф      | Платформа                     | 5     | 547
# п          | Поселок                       | 5     | 548
# п/о        | Почтовое отделение            | 5     | 549
# п/р        | Планировочный район           | 5     | 550
# п/ст       | Поселок и(при) станция(и)     | 5     | 551
# полустанок | Полустанок                    | 5     | 552
# починок    | Починок                       | 5     | 553
# рзд        | Разъезд                       | 5     | 554
# с          | Село                          | 5     | 555
# сл         | Слобода                       | 5     | 556
# ст         | Станция                       | 5     | 557
# х          | Хутор                         | 5     | 558
# ж/д_платф  | Железнодорожная платформа     | 5     | 559
# арбан      | Арбан                         | 5     | 560
# спуск      | Спуск                         | 5     | 561
# канал      | Канал                         | 5     | 562
# гск        | Гаражно-строительный кооперат | 5     | 563
# снт        | Садовое неком-е товарищество  | 5     | 564
# лпх        | Леспромхоз                    | 5     | 565
# проток     | Проток                        | 5     | 566
# коса       | Коса                          | 5     | 567
# вал        | Вал                           | 5     | 568
# ферма      | Ферма                         | 5     | 569
# мост       | Мост                          | 5     | 570
# ряды       | Ряды                          | 5     | 571
             
             
}
        
#.
