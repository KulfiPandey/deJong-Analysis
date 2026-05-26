from statsbombpy import sb
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import matplotlib.pyplot as plt

pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='white')

# get matches from both seasons
matches_1920 = sb.matches(competition_id=11, season_id=42)
matches_2021 = sb.matches(competition_id=11, season_id=90)

# combine both seasons into one
all_matches = pd.concat([matches_1920, matches_2021])

print(f"Total matches: {len(all_matches)}")

all_dejong_events = []  # empty list to collect events

for match_id in all_matches['match_id']:
    events = sb.events(match_id=match_id)
    dejong = events[events['player'] == 'Frenkie de Jong']
    all_dejong_events.append(dejong)

# combine everything into one big table
dejong_all = pd.concat(all_dejong_events)
print(f"Total De Jong events: {len(dejong_all)}")

print(dejong_all['type'].value_counts())


dejong_touches_all = dejong_all[dejong_all['type'].isin(['Pass', 'Carry', 'Ball Receipt*'])]

dejong_touches_all['x'] = dejong_touches_all['location'].apply(lambda loc: loc[0])
dejong_touches_all['y'] = dejong_touches_all['location'].apply(lambda loc: loc[1])

fig, ax = pitch.draw(figsize=(12, 8))
pitch.kdeplot(dejong_touches_all['x'], dejong_touches_all['y'], ax=ax,
              fill=True, cmap='hot', levels=100, alpha=0.7)
plt.title('Frenkie de Jong - Touch Map 19/20 - 20/21', color='white', fontsize=14)
plt.show()

avg_position = dejong_touches_all.groupby('match_id')[['x', 'y']].mean().reset_index()
print(avg_position.head(10))

fig, ax = pitch.draw(figsize=(12, 8))

pitch.scatter(avg_position['x'], avg_position['y'], 
              ax=ax, s=75, color='yellow', edgecolors='black', alpha=0.75)

plt.title("De Jong - Average Position Per Match (19/20 & 20/21)", color='white', fontsize=14)
plt.show()

# filter only De Jong's passes
dejong_passes_all = dejong_all[dejong_all['type'] == 'Pass']

# for each match, count total passes
total_passes = dejong_passes_all.groupby('match_id').size().reset_index(name='total')

# complete passes = where pass_outcome is null (not marked as incomplete)
complete_passes = dejong_passes_all[dejong_passes_all['pass_outcome'].isna()]
completed = complete_passes.groupby('match_id').size().reset_index(name='completed')

print(total_passes.head())
print(completed.head())

# merge total and completed into one table
pass_stats = total_passes.merge(completed, on='match_id')

# calculate accuracy percentage
pass_stats['accuracy'] = (pass_stats['completed'] / pass_stats['total'] * 100).round(1)

print(pass_stats.head(10))

import matplotlib.pyplot as plt
fig, ax1 = plt.subplots(figsize=(14, 6))

# barca colors
BARCA_BLUE = '#004D98'
BARCA_RED = '#A50044'
BG = '#0a0a0a'

fig.patch.set_facecolor(BG)
ax1.set_facecolor(BG)

# bars for pass volume in barca red
ax2 = ax1.twinx()
ax2.bar(range(len(pass_stats)), pass_stats['total'],
        alpha=0.4, color=BARCA_RED, label='Total Passes')
ax2.set_ylabel('Total Passes', color=BARCA_RED)
ax2.tick_params(colors=BARCA_RED)

# line for accuracy in barca blue
ax1.plot(range(len(pass_stats)), pass_stats['accuracy'],
         color=BARCA_BLUE, linewidth=2.5, label='Pass Accuracy %', zorder=5)
ax1.set_ylabel('Pass Accuracy %', color=BARCA_BLUE)
ax1.set_ylim(70, 100)
ax1.tick_params(colors='white')
ax1.spines[['top','right','left','bottom']].set_edgecolor('#333333')

plt.title("De Jong - Pass Accuracy & Volume Per Match (19/20 & 20/21)",
          color='white', fontsize=14, pad=15)
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(14, 6))

fig.patch.set_facecolor('#0a0a0a')
ax.set_facecolor('#0a0a0a')

ax.plot(range(len(avg_position)), avg_position['x'], 
        color='#004D98', linewidth=2.5)

# add a horizontal line showing the halfway line (x=60 in statsbomb coords)
ax.axhline(y= 60, color='white', linewidth=1, linestyle='--', alpha=0.5, label='Halfway line')

ax.set_ylabel('Average X Position', color='white')
ax.tick_params(colors='white')
plt.title("De Jong - How Deep Did He Play? (19/20 & 20/21)", 
          color='white', fontsize=14)
plt.legend()
plt.tight_layout()
plt.show()

# ball recoveries across all matches
dejong_recoveries_all = dejong_all[dejong_all['type'] == 'Ball Recovery']

dejong_recoveries_all['x'] = dejong_recoveries_all['location'].apply(lambda loc: loc[0])
dejong_recoveries_all['y'] = dejong_recoveries_all['location'].apply(lambda loc: loc[1])

fig, ax = pitch.draw(figsize=(12, 8))
pitch.scatter(dejong_recoveries_all['x'], dejong_recoveries_all['y'],
              ax=ax, s=80, color='red', edgecolors='white', alpha=0.7)
plt.title("De Jong - Ball Recoveries Across 68 La Liga Matches (19/20 & 20/21)",
          color='white', fontsize=14)
plt.show()

print(f"Total ball recoveries: {len(dejong_recoveries_all)}")