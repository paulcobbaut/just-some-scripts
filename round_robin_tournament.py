#!/usr/bin/python3
import random

# list of all teams
teams = ["Goblins"
        ,"Merfolk"
        ,"Taptap"
        ,"One"
        ,"Shady"
        ,"Olifanten"
        ,"2 battle"
        ,"Disrespekt"
        ,"Black Arts"
        ,"Unexpted Alliance"
        ,"Taken"
        ,"Boemboem"
        ,"Zombies"
        ,"Slivers"
        ,"kzb"
        ,"ggb"]

# count the number of teams
num_teams = len(teams)

# number of game rounds is one less than number of teams
num_rounds = num_teams - 1

# will contain the schedule
schedule = []

# Expand teams list names with spaces so they are all equal length (16 for now)
longest_name = len(max(teams, key=len))
for teamname in teams:
    expansion = ' ' * ( longest_name - len(teams[teams.index(teamname)] ))
    teams[teams.index(teamname)] = teams[teams.index(teamname)] + expansion

# Generate a round robin schedule for first round
for round in range(num_rounds):
    first_round = []
    for i in range(num_teams // 2):
        home = teams[i]
        away = teams[num_teams - i - 1]
        first_round.append((home, away))
    schedule.append(first_round)
    # Rotate teams
    teams.insert(1, teams.pop())

# Generate a round robin schedule for second round
for round in range(num_rounds):
    second_round = []
    for i in range(num_teams // 2):
        home = teams[i]
        away = teams[num_teams - i - 1]
        second_round.append((away, home))
    schedule.append(second_round)
    # Rotate teams
    teams.insert(1, teams.pop())

# Print both rounds
for i in range(num_rounds * 2):
    print(f'\nSpeeldag {i+1}:')
    for j in range(num_teams // 2):
        print( schedule[i][j][0], '-' , schedule[i][j][1] )

