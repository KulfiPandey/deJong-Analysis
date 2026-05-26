from statsbombpy import sb
import pandas as pd

# Pull all available competitions
comps = sb.competitions()
print(comps[comps['competition_name'] == 'La Liga'])
print(comps[comps['competition_name'] == 'La Liga'][['season_id', 'season_name']])

matches = sb.matches(competition_id=11, season_id=90)
print(matches.head())
print(matches[['match_id', 'match_date', 'home_team', 'away_team']].head(10))

events = sb.events(match_id=3773585)
print(events.head())

barca_players = events[events['team'] == 'Barcelona'][['player', 'position']].drop_duplicates()
print(barca_players)

dejong = events[events['player'] == 'Frenkie de Jong']
print(dejong['type'].value_counts())