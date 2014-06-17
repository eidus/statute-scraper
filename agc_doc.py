# coding:utf-8  
# Practice of scraping web data with xpath  
# by redice 2010.11.05  
  
import codecs  
import sys    
reload(sys)    
sys.setdefaultencoding('utf-8') 
from lxml import etree
import urllib, urllib2, cookielib
import re
import csv
import io
import gzip

cookie_jar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
urllib2.install_opener(opener)

# acquire cookie

url=raw_input("URL:")
#url='http://statutes.agc.gov.sg/aol/search/display/view.w3p;page=0;query=DocId:025e7646-947b-462c-b557-60aa55dc7b42%20Depth:0%20Status:inforce;rec=0;whole=yes#legis'
#url='http://www.google.com'
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
req = urllib2.Request(url, headers=headers) 

#req = urllib2.Request(url)
rsp = urllib2.urlopen(req).read()
bi = io.BytesIO(rsp)
gf = gzip.GzipFile(fileobj=bi, mode="rb")
text=gf.read()
#print text
tree=etree.HTML(text)
def get_number(str):
    return re.findall('(\d+)',str)[0]
act_number=" ".join(tree.xpath('//div[@id="contents"]//text()'))
act_number=get_number(act_number)
f= open(act_number+'.csv', 'wb') 
writer = csv.writer(f,delimiter='|',quoting=csv.QUOTE_ALL    )
writer.writerow(['act_number','section_number','section_name','section_content'] ) 
for i in tree.xpath('//blockquote[@class="TocParagraph"]//a') :
     url=i.xpath('./@href')[0]
     name=i.xpath('./text()')[0]
     #print name,url
     section_number=get_number(name)
     id=url.split('#')[-1]
     #print id
    
     if id.find('XX') > 0 :   
        section_name=''
        section_content=url
        
     elif id.find('he-') > 0 :
         
     
        section_name=tree.xpath('//a[@name="'+id+'"]/following-sibling::*/text()')[0]
        section_content=etree.tostring(tree.xpath('//div[@id="'+id.replace('he-','')+'"]')[0])
     else:
   
 
        section_name=tree.xpath('//div[@id="'+id+'"]/div[@class="prov1RepText"]//em/text()')
        section_content=''
     section_content=section_content.replace('\n','')
      
     writer.writerow([act_number,section_number,section_name,section_content] )
 
