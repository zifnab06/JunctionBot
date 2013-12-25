from RedditBot import bot, utils
import urllib2

base_url = 'http://itvends.com/vend'

@bot.command('vend')
def search(context):
    """Usage: .vend"""
    data = urllib2.urlopen(base_url)
    for line in data:
        return "\x01ACTION vends {item}\x01".format(item=line)
