from RedditBot import bot, utils
import urllib2

base_url = 'http://itvends.com/vend'

@bot.command('vend')
def search(context):
    """Usage: .vend"""
    data = urllib2.urlopen(base_url)
    for line in data:
        return "It Vends {item}".format(item=line)
