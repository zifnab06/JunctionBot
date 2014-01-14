from RedditBot import bot, utils
import urllib2

base_url = 'http://itvends.com/vend'

@bot.regex('^!vend')
@bot.command('vend')
def search(context):
    """Usage: .vend"""
    return "\x01ACTION vends " + vend() + "\x01"
@bot.regex('^!blend')
@bot.command('blend')
def search(context):
    """Usage: .blend"""
    return "\x01ACTION blends " + vend() + "\x01"

def vend():
    data = urllib2.urlopen(base_url)
    for line in data:
        return line
