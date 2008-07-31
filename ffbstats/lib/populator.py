teams_list = [["Matt J.", "Ninja Pirates"],
              ["Henry", "Necessary Roughness"],
              ["Charles", "Randy Ratio, The"],
              ["Matt P.", "He Hate Me"],
              ["Ricky", "Boy Looka Here"],
              ["Spencer", "ButtBrothers"],
              ["Mark", "Sailor's Allstars"],
              ["Jamie", "HornDogs"],
              ["Mike", "DrunkenAngryDwarves"],
              ["Jerry", "100yarddash"],
              ["Steve", "Road Warriors"]]

def generate_teams():
    teams = []
    for team in teams_list:
        teams.append(dict(owner=team[0], name=team[1]))
    return teams