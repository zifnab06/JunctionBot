from RedditBot import bot, utils
import urllib2
from lxml import etree

@bot.command
def pun(context):
	
    url = "http://www.punoftheday.com/cgi-bin/randompun.pl"
    response = urllib2.urlopen(url)
    htmlparser = etree.HTMLParser();
    tree = etree.parse(response, htmlparser)
    return "{0}: {1}".format(context.line['user'], tree.xpath("//div[@class='dropshadow1']/*[1]/text()")[0])
