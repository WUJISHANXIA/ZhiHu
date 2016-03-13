# -*- coding: utf-8 -*-
import re,urllib2,cookielib,urllib,sys
import MySQLdb,HTMLParser,chardet
class ZhiHu:
    def __init__(self):
        self.loginurl="https://www.zhihu.com/people/cao-wen-ming-78/followees"
        self.zhihu='/Users/wujishanxia/Documents/aha'
        self.header = {
            'Accept': '*/*',
            #'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Host': 'www.zhihu.com',
            'Referer': 'https://www.zhihu.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36',
        }
        self.data={
            '_xsrf':'78065429b0cd0bce6db2ccdac5d78545',
            'password':'luozixing520',
            'email':'1536736414@qq.com',
        }
    def login(self):
        try:
            self.request=urllib2.Request(self.loginurl,data=None,headers=self.header)
            self.cookie=cookielib.MozillaCookieJar(self.zhihu)
            self.cookie.load(self.zhihu,ignore_expires=True,ignore_discard=True)
            self.httphander=urllib2.HTTPCookieProcessor(self.cookie)
            self.opener=urllib2.build_opener(self.httphander)
            self.myopen=self.opener.open(self.request)

        self.postdata=urllib.urlencode(self.data)
        #print self.postdata
        #self.postdata=urllib.urlencode(self.data)
        #self.request=urllib2.Request(self.loginurl,self.postdata,self.header)
        self.request=urllib2.Request(self.loginurl,data=None,headers=self.header)
        self.cookie=cookielib.MozillaCookieJar(self.zhihu)
        self.cookie.load(self.zhihu,ignore_expires=True,ignore_discard=True)
        self.httphander=urllib2.HTTPCookieProcessor(self.cookie)
        self.opener=urllib2.build_opener(self.httphander)
        self.myopen=self.opener.open(self.request)
        #self.cookie.save(ignore_discard=True,ignore_expires=True)
class Parser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.followeesBegin=False
        self.followeesDetail=False
        self.followeesName=False
        self.followeesinfo=[]
        self.div_cnt=0
        self.a_cnt=0
    def handle_starttag(self, tag, attrs):
        HTMLParser.HTMLParser.handle_starttag(self,tag,attrs)
        attrs=dict(attrs)
        if tag=='div' and attrs.has_key('class') and attrs['class']=='zm-profile-card zm-profile-section-item zg-clear no-hovercard':
            self.followeesBegin=True
            #print 'zm-profile-card zm-profile-section-item zg-clear no-hovercard----begin'
        if tag=='div' and self.followeesBegin==True:
            self.div_cnt=self.div_cnt+1
            #print 'fine div and div_cnt='+str(self.div_cnt)
        #div  begin
        if tag=='a' and self.followeesBegin==True and attrs['class']=='zg-link':
            self.followeesName=True
        if tag=='a' and self.followeesName==True:
            self.tmp={}
            self.tmp['followeName']=attrs['title']
            self.tmp['href']=attrs['href']
            #self.followeesinfo.append(tmp)
            #print 'followeName ='+tmp['followeName']
            #print 'href ='+tmp['href']
        #a  followeesName
        if tag=='a' and self.followeesBegin==True and  attrs.has_key('target'):
            self.followeesDetail=True
    def handle_data(self, data):
        a_list=['followers','asks','answers','likes']
        if self.followeesDetail==True:
            #print 'data ='+data
            number=re.match(r'\d+',data)
            if number:
                #print number.group(0)
                pass
            else:
                #print "no find"
                pass
            self.tmp[a_list[self.a_cnt]]=number.group(0)
            self.a_cnt=self.a_cnt+1
            if self.a_cnt==4:
                self.followeesinfo.append(self.tmp)
                self.a_cnt=0
    def handle_endtag(self, tag):
        HTMLParser.HTMLParser.handle_endtag(self,tag)
        if tag=='div' and self.followeesBegin==True:
            self.div_cnt=self.div_cnt-1
            #print 'find /div and div_cnt'+str(self.div_cnt)
        if tag=='div' and self.followeesBegin==True and self.div_cnt==0:
            self.followeesBegin=False
            #print 'zm-profile-card zm-profile-section-item zg-clear no-hovercard----end'
        #div end
        if tag=='a' and self.followeesName==True:
            self.followeesName=False
        #a followeesName end
        #if tag=='a' and self.followeesDetail==True and self.a_cnt!=0:
            #self.a_cnt=self.a_cnt-1
        if tag=='a' and self.followeesDetail==True:
            self.followeesDetail=False
class MySQL:
    def __init__(self):
        pass
    def connectDatebase(self):
        try:
            self.conn=MySQLdb.connect(host='localhost',user='root',passwd='072401',charset='utf8')
            #conn.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
followINfoParser=Parser()
zhihu=Netease()
#print zhihu.myopen.read()
followINfoParser.feed(zhihu.myopen.read())
sql=MySQL()
sql.connectDatebase()
cur=sql.conn.cursor()
sql.conn.select_db('kaka')
for i in followINfoParser.followeesinfo:
    SQL="insert into wuji(user_name,user_ref,followers,asks,answers,likes) values ('%s','%s','%s','%s','%s','%s')" % (i['followeName'],i['href'],i['followers'],i['asks'],i['answers'],i['likes'])
    print SQL
    cur.execute(SQL)
sql.conn.commit()
cur.close()
sql.conn.close()
#cur.execute("insert into wuji ('user_name','user_href','followers','asks','answer','autumnswind','submission_data') values (%s,%s,%s,%s,%s,%s)",list(followINfoParser.followeesinfo[0]))
#for item in followINfoParser.followeesinfo:
   # print 'followeName = '+item['followeName']
   # print 'href ='+item['href']
   # print 'followers ='+item['followers']
   # print 'asks ='+item['asks']
   # print 'answers ='+item['answers']
   # print 'like ='+item['likes']