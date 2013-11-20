import sys
sys.path.insert(1, sys.path[0] + "/irctk")

from RedditBot.redditbot import Bot
from RedditBot.config import Config
from copy import deepcopy
from importlib import import_module
# initialize and config the bot
bot = Bot()
bot.config.from_object(Config)

if not bot.h_config:
    bot.h_config = deepcopy(bot.config)

bot.load_config()


# load our plugins
pluginList = bot.config["PLUGINS"];
for plugin in pluginList:
    import_module(plugin, 'RedditBot.plugins')

# Available plugins that aren't loaded by default
# from RedditBot.plugins import eval

if 'RedditBot.plugins.tell' in sys.modules:
    tell.Base.metadata.create_all(tell.engine)
    tell.get_users()
