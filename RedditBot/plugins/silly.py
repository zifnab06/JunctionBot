from RedditBot import bot
from RedditBot.utils import generate_insult
from random import seed, randint


@bot.command('insult')
@bot.command('i')
def insult(context):
    '''.insult <user>'''
    name = context.args
    return u'{0} is a {1}'.format(context.args, generate_insult())
