import re



pathSched = './wurd24sched.csv'
pathUsers = './wurd24users.csv'
pathNFL_Teams = './NFL_Teams.csv'

sched = [line for line in open(pathSched)]
users = [line for line in open(pathUsers)]
NFL_Teams = [line for line in open(pathNFL_Teams)]

gamesTemp = []
usersTemp = []
userCopy = []

gameDupTempList = []
gameDupTempList2 = []
game_week_list = []
user_did_not_play = []
user_bye = []


def space_between_uu_and_uc_games(games_text):
    first = False
    games_lst = games_text.split('\n')
    pattern = r'\w*\((\w)\) vs \w*\((\w)'
    for i, game in enumerate(games_lst):
        if 'week'.lower() in game.lower():
            first = False
        if len(game) < 10:
            continue

        try:
            m = re.match(pattern, game).groups()
            if m[0] != m[1] and not first:
                games_lst.insert(i, '\n')
                first = True
        except:
            continue

    games_lst = [game + '\n' for game in games_lst]
    games_text = ''.join(games_lst)
    print(games_text)
    quit()
    return games_text


def comp_or_user(games):
    team_txt = ''
    for team in NFL_Teams:
        if team in users:
            team_txt = team_txt + str(team.strip('\n') + '(U)\n')
        else:
            team_txt = team_txt + str(team.strip('\n') + '(C)\n')
        #games.replace(team.strip('\n'), team_txt)
    #test_team = [team.replace(team.strip('\n'), team_txt + '\n') for team in games]
    games_txt = ''.join(games)
    team_lst = team_txt.split()
    for team_r in team_lst:
        games_txt = games_txt.replace(team_r[0:-3], team_r)
    return games_txt

def check_if_user_not_in_current_week_games(weekgames):
    if len(weekgames) < 2:
        return
    for weekgame in weekgames:  # get rid of duplicate games
        if weekgame not in gameDupTempList2:
            gameDupTempList2.append(weekgame)
        else:
            gameDupTempList2.remove(weekgame)
            gameDupTempList2.insert(2, weekgame)
            pass

    userCopy = users.copy()
    for user in users:  # find out if there are bye players in this week
        for i, w in enumerate(gameDupTempList2):
            if user.strip('\n') in w:
                userCopy.remove(user)
                break
    gameDupTempList2.extend(userCopy)
    gameDupTempList[:] = gameDupTempList + gameDupTempList2
    gameDupTempList2.clear()



for game in sched:
    if 'week' in game.lower():
        check_if_user_not_in_current_week_games(gamesTemp)
        gamesTemp.clear()  # clear gamesTemp for the next week
        gamesTemp.append('\n')
        gamesTemp.append(game.replace(',', ''))
        continue

    for user in users:
        user1 = user.strip('\n')
        if user1 in game:
            #game = game.replace(user1, user1 + '(U)')
            gamesTemp.append(game.replace(',', ' vs '))

check_if_user_not_in_current_week_games(gamesTemp)
games_txt = comp_or_user(gameDupTempList)
games_txt = space_between_uu_and_uc_games(games_txt)
print(games_txt)
# for userGame in gamesTemp:
#     print(userGame, end='')
    # if game[0] == ',':
    #     for game in usersTemp:
    #         print(game)
          #usersTemp = [line for line in open(pathUsers)]
