from lxml import etree
from urllib.request import urlopen
import re

def get_last_match_link(id):
    match_data = etree.HTML(urlopen('http://www.dotabuff.com/players/'+id).read())
    return match_data.xpath('//*[@id="page-content"]/div[3]/div[1]/section[2]/article/table/tbody/tr[1]/td[2]/a/@href')[0]

def get_last_match_enemies(id):
    players = {}
    data = []
    player_pattern = re.compile(r'/players')
    hero_pattern = re.compile(r'/heroes')
    match_data = etree.HTML(urlopen('http://www.dotabuff.com'+get_last_match_link(id)).read())
    for item in match_data.xpath('//*[@id="page-content"]/div[3]/div[2]/section[1]/article/table/tbody//@href'):
        if re.match(hero_pattern, item) and item not in data:
            data.append(item)
    players['radiant'] = [i.split('/')[2] for i in data]
    data = []
    for item in match_data.xpath('//*[@id="page-content"]/div[3]/div[2]/section[2]/article/table//@href'):
        if re.match(player_pattern, item) and item not in data:
            data.append(item)
    players['dire'] = [i.split('/')[2] for i in data]
    if id in players['radiant']:
        match = match_data.xpath('//*[@id="page-content"]/div[3]/div[2]/section[1]/article/table/tbody//@href')
    else:
        match = match_data.xpath('//*[@id="page-content"]/div[3]/div[2]/section[2]/article/table/tbody//@href')
    data = []
    for item in match:
        if re.match(player_pattern, item) and re.match(hero_pattern, match[match.index(item) - 1]):
            data.append((item.split('/')[2], match[match.index(item) - 1]))
    for i in data[::2]:
        data.remove(i)
    return data

def get_player_stats(id):
    player_data = etree.HTML(urlopen('http://www.dotabuff.com/players/'+id).read())
    player_name = player_data.xpath('//*[@id="content-header-primary"]/div[2]/h1/text()')[0]
    player_wins = player_data.xpath('//*[@id="content-header-secondary"]/dl[2]/dd/span/span[1]/text()')[0]
    player_loses = player_data.xpath('//*[@id="content-header-secondary"]/dl[2]/dd/span/span[2]/text()')[0]
    player_abandons = player_data.xpath('//*[@id="content-header-secondary"]/dl[2]/dd/span/span[3]/text()')[0]
    player_win_rate = player_data.xpath('//*[@id="content-header-secondary"]/dl[3]/dd/text()')[0]
    player_total_games = int(player_wins.replace(',', '')) + int(player_loses.replace(',', '')) + int(player_abandons.replace(',', ''))
    return (player_name, player_total_games, player_wins, player_loses, player_win_rate)

def get_last_match_enemies_stats(id):
    players = {}
    for enemy_id in get_last_match_enemies(id):
        data = get_player_stats(enemy_id[0])
        players[data[0]] = (data[1], data[2], data[3], data[4], enemy_id[0], get_hero_image(enemy_id[1]))
    return players

def get_hero_image(hero):
    hero_data = etree.HTML(urlopen('http://www.dotabuff.com'+hero).read())
    return 'http://www.dotabuff.com'+hero_data.xpath('//*[@id="content-header-primary"]/div[1]/div//@src')[0]

#print(get_last_match_enemies_stats('122962230'))
