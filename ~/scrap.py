import fastf1
import fastf1.plotting
import matplotlib.pylab as plt
import numpy as np
import pandas as pd
from timple.timedelta import strftimedelta

fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1', misc_mpl_mods=True)

fastf1.Cache.enable_cache('~/Documents/porpo/Cache')

###############################################
# Analysis Funtion
###############################################

session = fastf1.get_session(2022, 'Spanish Grand Prix', 'R')
session.load()

drivers = pd.unique(session.laps['Driver'])    ### list of driver abbs
print(drivers)

all_laps = session.laps
best_lap = all_laps.pick_fastest()


team_colors = list()
for index, lap in all_laps.iterlaps():
    color = fastf1.plotting.team_color(lap['Team'])
    team_colors.append(color)

fig = plt.figure(1, figsize=(16,9), constrained_layout=True)
ax = plt.subplot()


ax.scatter(all_laps['Driver'], all_laps['LapTime'], color=team_colors)

ax.minorticks_on()
ax.tick_params(which='minor', axis='y')
ax.set_xticklabels
ax.grid(visible=True, axis='both', which='major', linewidth=0.8, alpha=.5)
ax.grid(visible=True, axis='both', which='minor', linestyle=':', linewidth=0.5, alpha=.5)

lap_time_string = strftimedelta(best_lap['LapTime'], '%m:%s.%ms')

plt.suptitle(f"{session.event['EventName']} {session.event.year} - Race\n"
             f"Fastest Lap: {lap_time_string} ({best_lap['Driver']})")

plt.show()