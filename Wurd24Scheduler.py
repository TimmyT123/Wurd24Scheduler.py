import re
import datetime


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

    for i, game in enumerate(games_lst):
        if 'week'.lower() in game.lower():
            first = False

        if '(' not in game:  # this makes sure game has a user or cpu in it
            continue

        try:
            pattern2 = r'^\w*\(U\)$'
            m2 = re.match(pattern2, game)
            if m2:
                games_lst[i] += ' - BYE'  # Add BYE to single teams

            pattern = r'\w*\((\w)\) vs \w*\((\w)'
            m = re.match(pattern, game).groups()
            if m[0] != m[1] and not first:
                games_lst.insert(i, '\n')
                first = True
        except:
            continue

    # ADD @everybody to the front of each week
    space = 0
    games_lst_copy = games_lst.copy()
    for i, word in enumerate(games_lst_copy):
        if 'week'.lower() in word.lower():
            space += 1
            games_lst.insert(i+space-1, '@everybody')

    games_lst = [game + '\n' for game in games_lst]  # put return in at the end of games

    games_text = ''.join(games_lst) # make into a string

    new_games_text = ''
    num = 0
    for char in games_text:
        if char == '\n':  # get rid of triple \n
            num += 1
            if num == 3:
                num = 0
                continue
            new_games_text += char
        else:
            num = 0
            new_games_text += char

    return new_games_text


def comp_or_user(games):
    team_txt = ''
    for team in NFL_Teams:
        if team in users:
            team_txt = team_txt + str(team.strip('\n') + '(U)\n')
        else:
            team_txt = team_txt + str(team.strip('\n') + '(C)\n')

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
            gamesTemp.append(game.replace(',', ' vs '))

check_if_user_not_in_current_week_games(gamesTemp)
games_txt = comp_or_user(gameDupTempList)
games_txt = space_between_uu_and_uc_games(games_txt)
print(games_txt)

weekDaysMapping = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

today = datetime.datetime.today().weekday()
today += 2  # The advance will be in 2 days
if today > 6:
    today -= 7

print(f"""
Next Advance is {weekDaysMapping[today]} @ 6PM (AZ time) or until games are completed.
*User-CPU games get 1 day.  
*User-User games get 2 days (if necessary).""")

