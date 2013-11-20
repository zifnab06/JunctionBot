
from RedditBot import bot, utils

from RedditBot.plugins import mumble

import socket
import re

from requests import codes

account = {
    'true': '{} is a premium Minecaft account',
    'false': '{} is \x02not\x02 a premium Minecraft account'
}

isup_re = re.compile(r'is (\w+) (?:up|down)', re.I)
server_re = re.compile(r'^\s*([A-Za-z0-9_-]+\.[A-Za-z0-9_.-]+)(?::([0-9]{1,5}))?\s*$')

server_list = bot.config['MINECRAFT_SERVER_LIST'];
mumble_server = bot.config['MINECRAFT_MUMBLE_SERVER'];
mumble_port = bot.config['MINECRAFT_MUMBLE_PORT']

def get_info(host, port):
    try:
        #Set up our socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((host, port))

        #Send 0xFE: Server list ping
        s.send('\xfe')
        #Send a payload of 0x01 to trigger a new response if the server supports it
        s.send('\x01')
        #Send an additional byte (bungee requires 3)
        s.send('\xfa')

        #Read as much data as we can (max packet size: 241 bytes)
        d = s.recv(256)
        s.close()

        #Check we've got a 0xFF Disconnect
        assert d[0] == '\xff'

        #Remove the packet ident (0xFF) and the short containing the length of the string
        #Decode UCS-2 string
        d = d[3:].decode('utf-16be')

        #If the response string starts with simolean1, then we're dealing with the new response
        if (d.startswith(u'\xa7' + '1')):
            d = d.split(u'\x00')
            #Return a dict of values
            return {'protocol_version': int(d[1]),
                    'minecraft_version':    d[2],
                    'motd':                 d[3],
                    'players':          int(d[4]),
                    'max_players':      int(d[5])}
        else:
            d = d.split(u'\xa7')
            #Return a dict of values
            return {'motd':         d[0],
                    'players':   int(d[1]),
                    'max_players': int(d[2])}

    except Exception, e:
        print e
        return False


def find_server(name):
    name = name.lower()
    for server in server_list:
        if name == server[0] or name in server[2]:
            return server
    return None


def silly_label(server):
    n = 'PLAYERS_{}'.format(server[0])
    return bot.config.get(n, 'players')


def check_login():
    params = {'user': bot.config['MINECRAFT_USER'],
              'password': bot.config['MINECRAFT_PASSWORD'],
              'version': 9001}

    r = utils.make_request('https://login.minecraft.net', params=params, method='POST')
    if isinstance(r, str):
        return 'Down ({})'.format(r)
    else:
        if r.status_code == codes.ok:
            return 'Up!'
        else:
            return 'Down ({})'.format(r.status_code)


def check_session():
    params = {'user': bot.config['MINECRAFT_USER'],
              'sessionId': 'invalid',
              'serverId': 'invalid'}

    r = utils.make_request('http://session.minecraft.net/game/joinserver.jsp', params=params)
    if isinstance(r, str):
        return 'Down ({})'.format(r)
    else:
        if r.status_code == codes.ok:
            return 'Up!'
        else:
            return 'Down ({})'.format(r.status_code)


@bot.command('login')
@bot.command('session')
@utils.cooldown(bot)
def minecraft_status(context):
    '''Usage: .session'''
    session = check_session()
    login = check_login()

    line = '[Login] {0} [Session] {1}'.format(login, session)
    return line


@bot.command
@utils.cooldown(bot)
def status(context):
    '''Usage: .status'''
    def server_info(host, port):
        info = get_info(host, port)
        if not info:
            return '{} seems to be down'.format(host)

        line = '{motd}: [{players}/{max_players}]'
        if 'minecraft_version' in info and bot.config.get('MINECRAFT_SHOW_SERVER_VER'):
            line = line.replace('{motd}', '{motd} ({minecraft_version})')

        return line.format(**info)

    def mumble_info():
        up = mumble.get_info(mumble_server, mumble_port)
        return 'Mumble: {}'.format('[{users}/{max}]'.format(**up) if up['success'] else 'Down')

    def is_enabled(s):
        return any(name in bot.config['ENABLED_SERVERS'].split(',') for name in s[2])

    servers = [server_info(s[0], s[1]) for s in server_list if is_enabled(s)]
    servers.append(mumble_info())

    return ' | '.join(servers)


@bot.regex(isup_re)
@utils.cooldown(bot)
def is_x_up(context):
    server = find_server(context.line['regex_search'].group(1))
    if not server:
        return

    if server[0] == mumble_server:
        context.args = '{0}:{1}'.format(server[0], server[1])
        info = mumble.mumble(context)
        return info

    info = get_info(server[0], server[1])
    if info:
        return '{0} is online with {players}/{max_players} {1} online.'.format(server[0], silly_label(server), **info)
    else:
        return '{0} seems to be down :(.'.format(server[0])


@bot.command
@utils.cooldown(bot)
def isup(context):
    '''Usage: .isup <MC server address>'''
    server = find_server(context.args)
    if not server:
        match = server_re.match(context.args)
        if not match:
            return
        server = (match.group(1), match.group(2) or 25565, 'players')

    if server[0] == mumble_server:
        context.args = '{0}:{1}'.format(server[0], server[1])
        info = mumble.mumble(context)
        return info

    info = get_info(server[0], server[1])
    if info:
        return '{0} is online with {players}/{max_players} {1} online.'.format(server[0], silly_label(server), **info)
    else:
        return '{0} seems to be down :(.'.format(server[0])


@bot.command('mcaccount')
@bot.command('mcpremium')
def premium(context):
    '''Usage: .mcaccount <username>'''
    arg = context.args.split(' ')[0]
    if len(arg) < 1:
        return premium.__doc__
    params = {'user': arg}
    r = utils.make_request('http://minecraft.net/haspaid.jsp', params=params)

    try:
        return account.get(r.text, 'Unexpected Response').format(arg)
    except AttributeError:
        return r
