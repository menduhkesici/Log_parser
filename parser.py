import re
import sys

class Player:
	name = ""
	lumber = 0
	brick = 0
	grain = 0
	wool = 0
	ore = 0
	steal = 0
	stolen = 0
	def __init__(self, name_):
		self.name = name_
	def total(self):
		return self.lumber + self.brick + self.grain + self.wool + self.ore + self.steal - self.stolen

def replace_substr(name):
	if name.startswith('Guest'):
		name = name.replace('Guest', '', 1)
	if name.startswith('bot'):
		name = name.replace('bot', '', 1)
	if name.startswith('User'):
		name = name.replace('User', '', 1)
	if name.startswith('icon_crown'):
		name = name.replace('icon_crown', '', 1)
	return name

DESK = Player('DESK')
DESK.lumber = 19
DESK.brick = 19
DESK.wool = 19
DESK.grain = 19
DESK.ore = 19

development_card_count = 25
knights_card_count = 14
victory_card_count = 5
road_card_count = 2
plenty_card_count = 2
monopoly_card_count = 2

PlayerList = []

name_len = 0
with open('player_name.txt') as f:
	for line in f:
		YOUR_NAME = replace_substr(line.split(' ', 1)[0])
		if (len(YOUR_NAME) > 0):
			name_len = max(name_len, len(YOUR_NAME))
			break
	else:
		sys.exit('Error: Insert your user name in player_name.txt')

pattern_placed_settlement = re.compile("^[^\s]+ placed a settlem*", re.IGNORECASE) # player_name placed a settlement
pattern_placed_road = re.compile("^[^\s]+ placed a ro*", re.IGNORECASE) # player_name placed a road
pattern_starting = re.compile("^[^\s]+ received starting resources*", re.IGNORECASE) # player_name received starting resources: orelumberwool
pattern_got = re.compile("^[^\s]+ got*", re.IGNORECASE) # player_name got: grainwool
pattern_build_road = re.compile("^[^\s]+ built a road*", re.IGNORECASE) # player_name built a road
pattern_build_settlement = re.compile("^[^\s]+ built a settlement*", re.IGNORECASE) # player_name built a settlement: +1 VP
pattern_build_city = re.compile("^[^\s]+ built a city*", re.IGNORECASE) # player_name built a city: +1 VP
pattern_bought_dev = re.compile("^[^\s]+ bought development*", re.IGNORECASE) # player_name bought development card
pattern_steal = re.compile("^[^\s]+ stole card from*", re.IGNORECASE) # player_name_1 stole card from: player_name_2
pattern_steal_you = re.compile("UserYou stole*", re.IGNORECASE) # UserYou stole: wool from: player_name_2
pattern_steal_from_you = re.compile("^[^\s]+ stole:", re.IGNORECASE) # player_name stole: ore from you
pattern_steal_monopoly = re.compile("^[^\s]+ stole *", re.IGNORECASE) # player_name stole 10: ore
pattern_trade = re.compile("^[^\s]+ traded*", re.IGNORECASE) # player_name_1 traded: lumberlumberfor: woolgrain with: player_name_2
pattern_bank_trade = re.compile("^[^\s]+ gave bank*", re.IGNORECASE) # player_name gave bank: graingrain and took lumber
pattern_bank_res = re.compile("^[^\s]+ took from bank*", re.IGNORECASE)# player_name took from bank: lumber lumber
pattern_discard = re.compile("^[^\s]+ discarded*", re.IGNORECASE) # player_name discarded: lumberwoolwoolwoolgrain
pattern_road_building = re.compile("^[^\s]+ used Road Building*", re.IGNORECASE) # player_name used Road Building card road building
pattern_knights = re.compile("^[^\s]+ used Knight*", re.IGNORECASE) # player_name used Knight card knight
pattern_plenty = re.compile("^[^\s]+ used Year of Plenty*", re.IGNORECASE) # player_name used Year of Plenty card year of plenty

with open('log.txt') as f:
	for line in f:
		line = line.rstrip('\n')
		if (len(line) == 0):
			continue
		#elif (line == "stop"):
		#	break
		elif (pattern_placed_settlement.match(line) or pattern_placed_road.match(line)):
			player_name = replace_substr(line.split(' ', 1)[0])
			found = False
			for player in PlayerList:
				if player_name == player.name:
					found = True
					break
			if (not found):
				name_len = max(name_len, len(player_name))
				PlayerList.append(Player(player_name))
		elif (pattern_starting.match(line) or pattern_got.match(line)):
			player_name, *middle, res_str = line.split()
			player_name = replace_substr(player_name)
			res_list = list(map(res_str.count, ['lumber', 'brick', 'grain', 'wool', 'ore']))
			found = False
			for player in PlayerList:
				if player_name == player.name:
					player.lumber += res_list[0]
					player.brick += res_list[1]
					player.grain += res_list[2]
					player.wool += res_list[3]
					player.ore += res_list[4]
					DESK.lumber -= res_list[0]
					DESK.brick -= res_list[1]
					DESK.grain -= res_list[2]
					DESK.wool -= res_list[3]
					DESK.ore -= res_list[4]
					found = True
					break
			if (not found):
				print('Name not found:', line)
		elif (pattern_build_road.match(line)):
			player_name = replace_substr(line.split(' ', 1)[0])
			found = False
			for player in PlayerList:
				if player_name == player.name:
					player.lumber -= 1
					player.brick -= 1
					DESK.lumber += 1
					DESK.brick += 1
					found = True
					break
			if (not found):
				print('Name not found:', line)
		elif (pattern_build_settlement.match(line)):
			player_name = replace_substr(line.split(' ', 1)[0])
			found = False
			for player in PlayerList:
				if player_name == player.name:
					player.lumber -= 1
					player.brick -= 1
					player.wool -= 1
					player.grain -= 1
					DESK.lumber += 1
					DESK.brick += 1
					DESK.wool += 1
					DESK.grain += 1
					found = True
					break
			if (not found):
				print('Name not found:', line)
		elif (pattern_build_city.match(line)):
			player_name = replace_substr(line.split(' ', 1)[0])
			found = False
			for player in PlayerList:
				if player_name == player.name:
					player.grain -= 2
					player.ore -= 3
					DESK.grain += 2
					DESK.ore += 3
					found = True
					break
			if (not found):
				print('Name not found:', line)
		elif (pattern_bought_dev.match(line)):
			player_name = replace_substr(line.split(' ', 1)[0])
			development_card_count -= 1
			found = False
			for player in PlayerList:
				if player_name == player.name:
					player.grain -= 1
					player.wool -= 1
					player.ore -= 1
					DESK.grain += 1
					DESK.wool += 1
					DESK.ore += 1
					found = True
					break
			if (not found):
				print('Name not found:', line)
		elif (pattern_steal.match(line)):
			player_name_1, *middle, player_name_2 = line.split()
			player_name_1 = replace_substr(player_name_1)
			player_name_2 = replace_substr(player_name_2)
			found_1 = False
			found_2 = False
			for player in PlayerList:
				if player_name_1 == player.name:
					player.steal += 1
					found_1 = True
				elif player_name_2 == player.name:
					player.stolen += 1
					found_2 = True
			if (not found_1):
				print('Name_1 not found:', line)
			if (not found_2):
				print('Name_2 not found:', line)
		elif (pattern_steal_you.match(line)):
			words = line.split()
			player_name_1 = YOUR_NAME
			player_name_2 = replace_substr(words[4])
			resources_stolen = list(map(words[2].count, ['lumber', 'brick', 'grain', 'wool', 'ore']))
			found_1 = False
			found_2 = False
			for player in PlayerList:
				if player_name_1 == player.name:
					player.lumber += resources_stolen[0]
					player.brick += resources_stolen[1]
					player.grain += resources_stolen[2]
					player.wool += resources_stolen[3]
					player.ore += resources_stolen[4]
					found_1 = True
				elif player_name_2 == player.name:
					player.lumber -= resources_stolen[0]
					player.brick -= resources_stolen[1]
					player.grain -= resources_stolen[2]
					player.wool -= resources_stolen[3]
					player.ore -= resources_stolen[4]
					found_2 = True
			if (not found_1):
				print('Name_1 not found:', line)
			if (not found_2):
				print('Name_2 not found:', line)
		elif (pattern_steal_from_you.match(line)):
			words = line.split()
			player_name_1 = replace_substr(words[0])
			player_name_2 = YOUR_NAME
			resources_stolen = list(map(words[2].count, ['lumber', 'brick', 'grain', 'wool', 'ore']))
			found_1 = False
			found_2 = False
			for player in PlayerList:
				if player_name_1 == player.name:
					player.lumber += resources_stolen[0]
					player.brick += resources_stolen[1]
					player.grain += resources_stolen[2]
					player.wool += resources_stolen[3]
					player.ore += resources_stolen[4]
					found_1 = True
				elif player_name_2 == player.name:
					player.lumber -= resources_stolen[0]
					player.brick -= resources_stolen[1]
					player.grain -= resources_stolen[2]
					player.wool -= resources_stolen[3]
					player.ore -= resources_stolen[4]
					found_2 = True
			if (not found_1):
				print('Name_1 not found:', line)
			if (not found_2):
				print('Name_2 not found:', line)
		elif (pattern_steal_monopoly.match(line)):
			player_name = replace_substr(line.split(' ', 1)[0])
			res_str = line.split()[3]
			monopoly_card_count -= 1
			found = False
			if (res_str == 'lumber'):
				for player in PlayerList:
					if player_name != player.name:
						player.lumber = 0
				for player in PlayerList:
					if player_name == player.name:
						player.lumber = 19 - DESK.lumber
						found = True
			elif (res_str == 'brick'):
				for player in PlayerList:
					if player_name != player.name:
						player.brick = 0
				for player in PlayerList:
					if player_name == player.name:
						player.brick  = 19 - DESK.brick
						found = True
			elif (res_str == 'wool'):
				for player in PlayerList:
					if player_name != player.name:
						player.wool = 0
				for player in PlayerList:
					if player_name == player.name:
						player.wool = 19 - DESK.wool
						found = True
			elif (res_str == 'grain'):
				for player in PlayerList:
					if player_name != player.name:
						player.grain = 0
				for player in PlayerList:
					if player_name == player.name:
						player.grain = 19 - DESK.grain
						found = True
			elif (res_str == 'ore'):
				for player in PlayerList:
					if player_name != player.name:
						player.ore = 0
				for player in PlayerList:
					if player_name == player.name:
						player.ore = 19 - DESK.ore
						found = True
			else:
				print('Resource not found:', line)
			if (not found):
				print('Name not found:', line)
		elif (pattern_trade.match(line)):
			words = line.split()
			player_name_1 = replace_substr(words[0])
			player_name_2 = replace_substr(words[5])
			resources_given_1 = list(map(words[2].count, ['lumber', 'brick', 'grain', 'wool', 'ore']))
			resources_given_2 = list(map(words[3].count, ['lumber', 'brick', 'grain', 'wool', 'ore']))
			found_1 = False
			found_2 = False
			for player in PlayerList:
				if player_name_1 == player.name:
					player.lumber += resources_given_2[0] - resources_given_1[0]
					player.brick += resources_given_2[1] - resources_given_1[1]
					player.grain += resources_given_2[2] - resources_given_1[2]
					player.wool += resources_given_2[3] - resources_given_1[3]
					player.ore += resources_given_2[4] - resources_given_1[4]
					found_1 = True
				elif player_name_2 == player.name:
					player.lumber += resources_given_1[0] - resources_given_2[0]
					player.brick += resources_given_1[1] - resources_given_2[1]
					player.grain += resources_given_1[2] - resources_given_2[2]
					player.wool += resources_given_1[3] - resources_given_2[3]
					player.ore += resources_given_1[4] - resources_given_2[4]
					found_2 = True
			if (not found_1):
				print('Name_1 not found:', line)
			if (not found_2):
				print('Name_2 not found:', line)
		elif (pattern_bank_trade.match(line)):
			words = line.split()
			player_name = replace_substr(words[0])
			resources_got = list(map(words[6].count, ['lumber', 'brick', 'grain', 'wool', 'ore']))
			resources_given = list(map(words[3].count, ['lumber', 'brick', 'grain', 'wool', 'ore']))
			found = False
			for player in PlayerList:
				if player_name == player.name:
					player.lumber += resources_got[0] - resources_given[0]
					player.brick += resources_got[1] - resources_given[1]
					player.grain += resources_got[2] - resources_given[2]
					player.wool += resources_got[3] - resources_given[3]
					player.ore += resources_got[4] - resources_given[4]
					DESK.lumber -= resources_got[0] - resources_given[0]
					DESK.brick -= resources_got[1] - resources_given[1]
					DESK.grain -= resources_got[2] - resources_given[2]
					DESK.wool -= resources_got[3] - resources_given[3]
					DESK.ore -= resources_got[4] - resources_given[4]
					found = True
			if (not found):
				print('Name not found:', line)
		elif (pattern_bank_res.match(line)):
			words = line.split()
			player_name = replace_substr(words[0])
			resources_got1 = list(map(words[4].count, ['lumber', 'brick', 'grain', 'wool', 'ore']))
			resources_got2 = list(map(words[5].count, ['lumber', 'brick', 'grain', 'wool', 'ore']))
			found = False
			for player in PlayerList:
				if player_name == player.name:
					player.lumber += resources_got1[0] + resources_got2[0]
					player.brick += resources_got1[1] + resources_got2[1]
					player.grain += resources_got1[2] + resources_got2[2]
					player.wool += resources_got1[3] + resources_got2[3]
					player.ore += resources_got1[4] + resources_got2[4]
					DESK.lumber -= resources_got1[0] + resources_got2[0]
					DESK.brick -= resources_got1[1] + resources_got2[1]
					DESK.grain -= resources_got1[2] + resources_got2[2]
					DESK.wool -= resources_got1[3] + resources_got2[3]
					DESK.ore -= resources_got1[4] + resources_got2[4]
					found = True
			if (not found):
				print('Name not found:', line)
		elif (pattern_discard.match(line)):
			player_name, *middle, res_str = line.split()
			player_name = replace_substr(player_name)
			res_list = list(map(res_str.count, ['lumber', 'brick', 'grain', 'wool', 'ore']))
			found = False
			for player in PlayerList:
				if player_name == player.name:
					player.lumber -= res_list[0]
					player.brick -= res_list[1]
					player.grain -= res_list[2]
					player.wool -= res_list[3]
					player.ore -= res_list[4]
					DESK.lumber += res_list[0]
					DESK.brick += res_list[1]
					DESK.grain += res_list[2]
					DESK.wool += res_list[3]
					DESK.ore += res_list[4]
					found = True
					break
			if (not found):
				print('Name not found:', line)
		elif (pattern_road_building.match(line)):
			road_card_count -= 1
		elif (pattern_knights.match(line)):
			knights_card_count -= 1
		elif (pattern_plenty.match(line)):
			plenty_card_count -= 1
		#else:
			#print('undefined:', line)
		for player in PlayerList:
			if (player.lumber < 0):
				player.steal += player.lumber
				player.lumber = 0
			if (player.brick < 0):
				player.steal += player.brick
				player.brick = 0
			if (player.wool < 0):
				player.steal += player.wool
				player.wool = 0
			if (player.grain < 0):
				player.steal += player.grain
				player.grain = 0
			if (player.ore < 0):
				player.steal += player.ore
				player.ore = 0
			if (player.steal < 0):
				player.steal = 0
			if (monopoly_card_count == 2):
				total = player.total()
				if (player.lumber > total):
					excess = player.lumber - total
					player.lumber -= excess
					player.stolen -= excess
				if (player.brick > total):
					excess = player.brick - total
					player.brick -= excess
					player.stolen -= excess
				if (player.wool > total):
					excess = player.wool - total
					player.wool -= excess
					player.stolen -= excess
				if (player.grain > total):
					excess = player.grain - total
					player.grain -= excess
					player.stolen -= excess
				if (player.ore > total):
					excess = player.ore - total
					player.ore -= excess
					player.stolen -= excess
				if (player.stolen < 0):
					player.stolen = 0

while (PlayerList[-1].name != YOUR_NAME):
	PlayerList.insert(0, PlayerList.pop())
PlayerList.insert(0, DESK)

res_len = 6
list_str = []
if (monopoly_card_count < 2):
	list_str.append('RESOURCE COUNTS OF PLAYERS MAY BE WRONG!')
list_str.append('Development card count on desk: ' + str(development_card_count))
list_str.append('Total victory point card count: ' + str(victory_card_count))
list_str.append('Unplayed knights card count: ' + str(knights_card_count))
list_str.append('Unplayed road building card count: ' + str(road_card_count))
list_str.append('Unplayed year of plenty card count: ' + str(plenty_card_count))
list_str.append('Unplayed monopoly card count: ' + str(monopoly_card_count))
for i in range(0, len(PlayerList) * 2):
	list_str.append('')
print('-' * (name_len + (res_len + 3) * 8 + 47))
print('|', 'name'.ljust(name_len), '|', 'lumber'.ljust(res_len), '|', 'brick'.ljust(res_len), '|', 'wool'.ljust(res_len), 
	'|', 'grain'.ljust(res_len), '|', 'ore'.ljust(res_len), '|', 'steal'.ljust(res_len), '|', 'stolen'.ljust(res_len), 
	'|', 'total'.ljust(res_len), '|', list_str[0].ljust(40), '|')
i = 1
for player in PlayerList:
	print('|' + '-' * (name_len + (res_len + 3) * 8 + 2) + '|', list_str[i].ljust(40), '|')
	i += 1
	print('|', player.name.ljust(name_len), '|', str(player.lumber).ljust(res_len), '|', str(player.brick).ljust(res_len), '|', str(player.wool).ljust(res_len), 
		'|', str(player.grain).ljust(res_len), '|', str(player.ore).ljust(res_len), '|', str(player.steal).ljust(res_len).ljust(res_len), '|', 
		str(-player.stolen).ljust(res_len), '|', str(player.total()).ljust(res_len), '|', list_str[i].ljust(40), '|')
	i += 1
print('-' * (name_len + (res_len + 3) * 8 + 47))
