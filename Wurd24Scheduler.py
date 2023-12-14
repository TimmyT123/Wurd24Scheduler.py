



pathSched = '.\wurd24sched.csv'
pathUsers = '.\wurd24users.csv'

sched = [line for line in open(pathSched)]
users = [line for line in open(pathUsers)]
gamesTemp = []
usersTemp = []
userCopy = []

gameDupTempList = []
gameDupTempList2 = []
game_week_list = []
user_did_not_play = []
user_bye = []


def comp_or_user(games):
    my_list = [elem + "(U)" for elem in games if user in games]
    pass

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
comp_or_user(gameDupTempList)
for magic in gameDupTempList:
    print(magic, end='')
# for userGame in gamesTemp:
#     print(userGame, end='')
    # if game[0] == ',':
    #     for game in usersTemp:
    #         print(game)
          #usersTemp = [line for line in open(pathUsers)]
