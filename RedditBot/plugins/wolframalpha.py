
from RedditBot import bot, utils
from RedditBot.utils import generate_insult

import xml.etree.ElementTree as ET

import re


url = 'http://www39.wolframalpha.com/input/'

letters_re = re.compile(r'^(?:\w \| )+\w$')


@bot.command('wa')
@bot.command('wolframalpha')
def wa_api(context):
    '''Usage: .wa <query>'''
    if not bot.config['WOLFRAMALPHA_KEY']:
        return 'WolframAlpha support not configured.'
    url = 'http://api.wolframalpha.com/v2/query'
    params = {'format': 'plaintext', 'appid': bot.config['WOLFRAMALPHA_KEY'], 'input': context.args}
    result = utils.make_request(url, params=params, timeout=10)
    if type(result) is str:
        return result
    xml = ET.fromstring(result.text.encode('utf8'))
    success = xml.get('success') == 'true'
    if success:
        pods = xml.findall('.//pod[@primary=\'true\']/subpod/plaintext')

        if len(pods) < 1:
            return 'No primary node returned, you {0}'.format(generate_insult())

        results = pods[-1].text.split('\n')

        def format_result_nicely(result):
            if letters_re.match(result):
                return result.replace(' | ', '')
            return result

        results = [format_result_nicely(r) for r in results]
        return ', '.join(results)
    else:
        return 'Failed, you %s.' % utils.generate_insult()
