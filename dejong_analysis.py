from statsbombpy import sb
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt

# get the match
events = sb.events(match_id=3773585)

# filter de jong
dejong = events[events['player'] == 'Frenkie de Jong']

# filter touches
dejong_touches = dejong[dejong['type'].isin(['Pass', 'Carry', 'Ball Receipt*'])]

# extract the x and y coordinates of the touches
dejong_touches['x'] = dejong_touches['location'].apply(lambda x: x[0])
dejong_touches['y'] = dejong_touches['location'].apply(lambda x: x[1])

# create a pitch
pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')
fig, ax = pitch.draw(figsize=(12, 8))

# plot the touches
pitch.scatter(dejong_touches['x'], dejong_touches['y'], ax=ax, s=50, color='blue', edgecolors='black', alpha=0.7)
plt.title("Frenkie de Jong - Touch Map vs Real Madrid (Oct 2020)", color='white', fontsize=14)
plt.show()

# draw a fresh pitch for the heatmap
fig, ax = pitch.draw(figsize=(12, 8))

# draw the heatmap
pitch.kdeplot(dejong_touches['x'], dejong_touches['y'], ax=ax, 
              fill=True, cmap='hot', levels=100, alpha=0.7)

plt.title("Frenkie de Jong - Touch Heatmap vs Real Madrid (Oct 2020)", 
          color='white', fontsize=14)
plt.show()

# filter only passes
dejong_passes = dejong[dejong['type'] == 'Pass']

# extract start and end coordinates
dejong_passes['x'] = dejong_passes['location'].apply(lambda loc: loc[0])
dejong_passes['y'] = dejong_passes['location'].apply(lambda loc: loc[1])
dejong_passes['end_x'] = dejong_passes['pass_end_location'].apply(lambda loc: loc[0])
dejong_passes['end_y'] = dejong_passes['pass_end_location'].apply(lambda loc: loc[1])

# draw pitch
fig, ax = pitch.draw(figsize=(12, 8))

# draw arrows for each pass
pitch.arrows(dejong_passes['x'], dejong_passes['y'],
             dejong_passes['end_x'], dejong_passes['end_y'],
             ax=ax, width=2, headwidth=5, color='red', alpha=0.6)

plt.title("Frenkie de Jong - Pass Map vs Real Madrid (Oct 2020)", 
          color='white', fontsize=14)
plt.show()

# filter ball recoveries
dejong_recoveries = dejong[dejong['type'] == 'Ball Recovery']

# extract coordinates
dejong_recoveries['x'] = dejong_recoveries['location'].apply(lambda loc: loc[0])
dejong_recoveries['y'] = dejong_recoveries['location'].apply(lambda loc: loc[1])

# draw pitch
fig, ax = pitch.draw(figsize=(12, 8))

# scatter the dots
pitch.scatter(dejong_recoveries['x'], dejong_recoveries['y'], 
              ax=ax, s=100, color='red', edgecolors='white', alpha=0.9)

plt.title("Frenkie de Jong - Ball Recoveries vs Real Madrid (Oct 2020)", 
          color='white', fontsize=14)
plt.show()