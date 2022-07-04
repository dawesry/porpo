import datetime
import os
import webbrowser

import fastf1
import matplotlib.pylab as plt
from matplotlib.pylab import scatter
import pandas as pd
import PySimpleGUI as sg
from fastf1 import plotting

fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1', misc_mpl_mods=True)

###############################################
# Directory Functions
###############################################

class CacheDir:

    default = '~/Documents/porpo/Cache'

    def __init__(self, path):
        path = 'path'

    def Set(path):
        CacheExist = os.path.exists(path)
        if not CacheExist:
            os.makedirs(path)
        CacheDir.default = path

fastf1.Cache.enable_cache(CacheDir.default)

class ExportDir:

    default = '~/Documents/porpo/Export'

    def __init__(self, path):
        path = 'path'

    def Set(path):
        ExportExist = os.path.exists(path)
        if not ExportExist:
            os.makedirs(path)
        ExportDir.default = path

###############################################
# Analysis Classes
###############################################

class Session:
    def __init__(self, year, gp, ses):
        self = fastf1.get_session(year, gp, ses)
        self.load()

class Driver:
    def __init__(self, grandprix, abb):
        self.id = abb
        self.bio = grandprix.get_driver(self.id)
        self.ses = grandprix.laps.pick_driver(self.id)
        self.tel = grandprix.laps.pick_driver(self.id).get_car_data().add_distance()
        self.best = grandprix.laps.pick_driver(self.id).pick_fastest()
        self.best_tel = grandprix.laps.pick_driver(self.id).pick_fastest().get_car_data().add_distance()
        self.teamcolor = fastf1.plotting.team_color(self.bio['TeamName'])

class Lists:

    class make:
        def __init__(self, name, list):
            self.name = name
            self.list = list

        def print_list(self):
            print(self.list)

    Years = make('Years', list(range(2018, (int(datetime.datetime.today().year)+1))))
    GrandPrix = make('GrandPrix', list(fastf1.get_event_schedule(Years.list[-1])['EventName']))
    Sessions = make('Sessions', ['FP1', 'FP2', 'FP3', 'S', 'Q', 'R'])
    Drivers = make('Drivers', ['Driver 1', 'Driver 2', 'Driver 3'])
    DriversComp = make('DriversComp', [])
    SessionSlice = make('SessionSlice', ['Full Session', 'Specific Lap', 'Fastest Lap'])
    SesVars = make('SesVars', ['LapTime', 'LapNumber', 'Stint', 'PitOutTime', 'PitInTime', 'Sector1Time', 'Sector2Time', 'Sector3Time', 'SpeedI1', 'SpeedI2', 'SpeedFL', 'SpeedST', 'IsPersonalBest', 'Compound', 'TyreLife', 'TrackStatus'])
    LapVars = make('LapVars', ['Speed', 'RPM', 'nGear', 'Throttle', 'Brake', 'DRS', 'Status', 'Time', 'SessionTime', 'Distance'])
    DriverVars = make('DriverVars', ['Var 1', 'Var 2', 'Var 3'])

    Laps = make('Laps', [1, 2, 3, 4, 5])

###############################################
# Analysis Functions
###############################################

def set_data(driver, slice, lap_num):
    if slice == "Fastest Lap":
        self = driver.best_tel
    
    elif slice == "Specific Lap":
        lap_n = driver.ses[driver.ses['LapNumber'] == lap_num]
        lap_n_tel = lap_n.get_car_data().add_distance()
        self = lap_n_tel

    elif slice == "Full Session":
        self = driver.ses

    return self

def make_fig():
        fig = plt.figure(1, figsize=(16,9), constrained_layout=True)
        ax = fig.subplots()
        return fig, ax

def plot_ax(driver, data, fig, xvar, yvar, ax):
    ax.plot(data[xvar], data[yvar], color=driver.teamcolor, label=f'{driver.id}')
    ax.set_xlim(data[xvar].min(), data[xvar].max())

def compare(grandprix, driver, slice, xvar, yvar, fig, ax):
    for abb in driver:
        driver = Driver(grandprix, abb)
        data = set_data(driver, slice, lap_num)
        plot_ax(driver, data, fig, xvar, yvar, ax)

def set_title(grandprix, driver, yvar, slice, ses, lap_num, comp):
    if slice == "Specific Lap":
        analysis = f"Lap {lap_num}, {yvar} \n {grandprix.event.year} {grandprix.event['EventName']}, {ses}"

    elif slice != "Specific Lap":
        analysis = f"{slice}, {yvar} \n {grandprix.event.year} {grandprix.event['EventName']}, {ses}"

    if comp == True:
        title = analysis

    elif comp != True:
        title = f"{driver.bio['FullName']} " + analysis

    plt.suptitle(f"{title}")

def design_plot(ax):
        ax.set_xlabel(xvar)
        ax.set_ylabel(yvar)

        # Turn Grid, Minor ticks ON
        ax.minorticks_on()
        ax.grid(visible=True, axis='both', which='major', linewidth=0.8, alpha=.5)
        ax.grid(visible=True, axis='both', which='minor', linestyle=':', linewidth=0.5, alpha=.5)

        ax.legend()

def show_plot():
    plt.show()

def analyse():
    #Inputs
    global year, gp, ses, abb, slice
    global lap_num, xvar, yvar, comp

    year = values['-YEAR-']
    gp = values['-GP-']
    ses = values['-SESSION-']
    abb = values['-DRIVER-']
    slice = values['-SLICE-']
    lap_num = values['-LAPNUM-']
    xvar = values['-DRIVERXVAR-']
    yvar = values['-DRIVERYVAR-']
    comp = values['-COMPARE-']

    # Create Figure
    fig, ax = make_fig()

    # Get Comapre Status
    # Get Driver Data for SLICE
    # Plot Variables
    if comp == True:
        compare(grandprix, abb, slice, xvar, yvar, fig, ax)
        driver = Driver(grandprix, abb[0])

    elif comp != True:
        driver = Driver(grandprix, abb[0])
        data = set_data(driver, slice, lap_num)
        plot_ax(driver, data, fig, xvar, yvar, ax)
        
    design_plot(ax)
    set_title(grandprix, driver, yvar, slice, ses, lap_num, comp)

    # Show Plot
    show_plot()

###############################################
# Make Window Function / Layout
###############################################

def make_window():
    sg.theme('Reddit')

    menu_def = [[('&porpo'), ['&About', ('&Preferences'), ['&Set Cache Directory', 'Set Export Directory'], '&GitHub', 'E&xit']]]
    
    header_layout = [[sg.Image(source='src/common/images/icon_small.png', size=(120, 60), expand_x=True, expand_y=True)],]

    layout = [[sg.Menubar(menu_def, key='-MENU-')],
                [sg.Frame('', header_layout, size=(250,75), key='-HEAD-')],
                [sg.OptionMenu(Lists.Years.list, default_value=f'{Lists.Years.list[-1]}', expand_x=True, key='-YEAR-')],
                [sg.Button('Load Season', expand_x=True)],
                [sg.Listbox(Lists.GrandPrix.list, enable_events=True, expand_x=True, size=(None,10), select_mode='single', horizontal_scroll=False, visible=False, pad=(7,7,7,7), key='-GP-')],
                [sg.OptionMenu(Lists.Sessions.list, default_value=f'Select Session...', expand_x=True, visible=False, key='-SESSION-')],
                [sg.Button('Load Drivers for Session', visible=False, disabled=True, expand_x=True, key='-LOADDRIVERS-')],
                [sg.Listbox(Lists.Drivers.list, enable_events=True, expand_x=True, size=(None,10), select_mode='single', horizontal_scroll=False, visible=False, pad=(7,7,7,7), key='-DRIVER-')],
                [sg.Checkbox('Compare drivers?', enable_events=True, visible=False, key='-COMPARE-')],
                [sg.OptionMenu(Lists.SessionSlice.list, default_value=f'Evalutate Full Session?', disabled=True, expand_x=True, visible=False, key='-SLICE-')],
                [sg.Text('Enter Lap Number', visible=False, key='-LAPASK-')],
                [sg.Input(default_text= 0, expand_x=True, visible=False, key='-LAPNUM-')],
                [sg.Button('Select Data Points', visible=False, disabled=True, expand_x=True, key='-LOADVARS-')],
                [sg.OptionMenu(Lists.DriverVars.list, default_value='.Y Variable...', expand_x=True, visible=False, key='-DRIVERYVAR-')],
                [sg.OptionMenu(Lists.DriverVars.list, default_value='.X Variable...', expand_x=True, visible=False, key='-DRIVERXVAR-')],
                [sg.Button('Confirm All', visible=False, expand_x=True, key='-CONFIRM ALL-')],
                [sg.Button('Analyse', visible=False, disabled=True, expand_x=True, key='-PLOT-')], 
                ]

    window = sg.Window('porpo', layout, margins=(0, 0), finalize=True)

    window.set_min_size(window.size)
    
    return window

##################
# Main Function
##################

def main():
    window = make_window()

    # Window Open, Begin Event Loop
    while True:
        global values
        event, values = window.read(timeout=100)
        
###############################################
# Buttonn Function Class
## Button Functions
###############################################
        
        class ButtonFunc:

            #About
            def About():
                about_layout = [[sg.Text('porpo is not affiliated with Formula 1 or the FIA')],
                                [sg.Text('License MIT - Free to Distribute', justification='center')],]
                about_win = sg.Window('About porpo', about_layout, size=(200,50), modal=True, keep_on_top=True)
                event = about_win.read()
                if event == sg.WIN_CLOSED:
                    about_win.close()

            #Preferences
            def Preferences():
                pref_layout = [[[sg.Text('Session Cache Folder')], [sg.Button("Set Cache", expand_x=True)]],
                                [[sg.Text('Session Export Directory')], [sg.Button("Set Export", expand_x=True)],
                                [sg.OK('OK')]],]
                pref_win = sg.Window('porpo Preferences', pref_layout, modal=True, keep_on_top=True, disable_close=True, force_toplevel=True)
                event, values = pref_win.read()
                while True:
                    if event == 'OK' or sg.WIN_CLOSED:
                        pref_win.close()

                    elif event == 'Set Cache':
                        path = sg.popup_get_folder('Choose your CACHE directory', no_window=True, default_path=f'{CacheDir.default}')
                        CacheDir.Set(path)
                        print(f"Set CACHE to {path}")

                    elif event == 'Set Export':
                        path = sg.popup_get_folder('Choose your EXPORT directory', no_window=True, default_path=f'{ExportDir.default}')
                        ExportDir.Set(path)
                        print(f"Set EXPORT to {path}")

            #Set Cache Directory
            def Pref_SetCache():
                path = sg.popup_get_folder('Choose your folder', no_window=True, default_path=CacheDir.default, initial_folder=CacheDir.default)
                if path in (None, ''):
                    pass
                else:
                    CacheDir.Set(str(path))
                    print(f'[LOG] set CACHE to {path}')
            
            #Set Export Directory
            def Pref_SetExport():
                path = sg.popup_get_folder('Choose your folder', no_window=True, default_path=ExportDir.default, initial_folder=ExportDir.default)
                if path in (None, ''):
                    pass
                else:
                    ExportDir.Set(str(path))
                    print(f'[LOG] set EXPORT to {path}')

            #GitHub
            def GitHub():
                webbrowser.open('https://github.com/dtech-auto/porpo/', new=2)
                print(f"[LOG] Load Grand Prix for {values['-YEAR-']}")

            # Load GPs
            def LoadGPList():
                print(f"[LOG] Load Grand Prix for {values['-YEAR-']}")
                Lists.GrandPrix = Lists.make('Grand Prix', list(fastf1.get_event_schedule(int(values['-YEAR-']))['EventName']))
                window.Element('-GP-').update(values=Lists.GrandPrix.list, visible=True)
                window.Element('-SESSION-').update(visible=True)
                window.Element('-LOADDRIVERS-').update(visible=True, disabled=True)
                window.Element('-DRIVER-').update(visible=False)
                window.Element('-SLICE-').update(visible=False, disabled=True)
                window.Element('-LOADVARS-').update(visible=False, disabled=True)
                window.Element('-PLOT-').update(disabled=True, visible=False)
                window.Element('-DRIVERXVAR-').update(visible=False)
                window.Element('-DRIVERYVAR-').update(visible=False)
                window.Element('-CONFIRM ALL-').update(visible=False)
                window.Element('-COMPARE-').update(visible=False)
                window.Element('-LAPASK-').update(visible=False)
                window.Element('-LAPNUM-').update(visible=False)
                window.refresh()
                window.read(timeout=100)

            # Load Drivers
            def LoadDriverList():
                print(f'[LOG] Load Drivers for event...')
                global grandprix
                grandprix = fastf1.get_session(int(values['-YEAR-']), str(values['-GP-']), str(values['-SESSION-']))
                grandprix.load()
                driver_list = grandprix.results['Abbreviation']
                Lists.Drivers = Lists.make('Drivers', list(driver_list))
                window.Element('-DRIVER-').update(values=Lists.Drivers.list)
                window.Element('-DRIVER-').update(visible=True)
                window.Element('-COMPARE-').update(visible=True)
                window.Element('-SLICE-').update(visible=True, disabled=True)
                window.Element('-LOADVARS-').update(visible=True, disabled=True)
                window.Element('-PLOT-').update(disabled=True)
                window.Element('-LAPASK-').update(visible=False)
                window.Element('-LAPNUM-').update(visible=False)
                window.refresh()
                window.read(timeout=100)

            def LoadDriverVars():
                print(f'[LOG] Loading variables for driver(s)...')

                if values['-SLICE-'] == 'Full Session':
                    window.Element('-DRIVERXVAR-').update(values=Lists.SesVars.list)
                    window.Element('-DRIVERYVAR-').update(values=Lists.SesVars.list)
                    window.Element('-LAPASK-').update(visible=False)
                    window.Element('-LAPNUM-').update(visible=False)

                elif values['-SLICE-'] == 'Fastest Lap':
                    window.Element('-DRIVERXVAR-').update(values=Lists.LapVars.list)
                    window.Element('-DRIVERYVAR-').update(values=Lists.LapVars.list)
                    window.Element('-LAPASK-').update(visible=False)
                    window.Element('-LAPNUM-').update(visible=False)
                
                if values['-SLICE-'] == 'Specific Lap':
                    window.Element('-DRIVERXVAR-').update(values=Lists.LapVars.list)
                    window.Element('-DRIVERYVAR-').update(values=Lists.LapVars.list)
                    window.Element('-LAPASK-').update(visible=True)
                    window.Element('-LAPNUM-').update(visible=True)

                window.Element('-DRIVERXVAR-').update(visible=True)
                window.Element('-DRIVERYVAR-').update(visible=True)
                window.Element('-CONFIRM ALL-').update(visible=True)
                window.Element('-PLOT-').update(disabled=True, visible=True)
                window.refresh()
                window.read(timeout=100)

###############################################
# Begin 'If' Events for Button Pushes
###############################################

        # Exit
        if event in (None, 'Exit'):
            break

        # About
        elif event == 'About':
            ButtonFunc.About()

        # Preferences
        elif event == 'Preferences':
            ButtonFunc.Preferences()

        # Set Cache Dir
        elif event == 'Set Cache Directory':
            ButtonFunc.Pref_SetCache()

        # Set Export Dir
        elif event == 'Set Cache Directory':
            ButtonFunc.Pref_SetExport()

        # GitHub
        elif event == 'GitHub':
            ButtonFunc.GitHub()

        # Load GPs
        elif event == 'Load Season':
            ButtonFunc.LoadGPList()

        # Selected GP, enable Load Drivers List
        elif event == '-GP-':
            window.Element('-LOADDRIVERS-').update(disabled=False)
            window.Element('-PLOT-').update(disabled=False)
            window.refresh()

        # Selected Driver, enable Load VARS List
        elif event == '-DRIVER-':
            window.Element('-SLICE-').update(disabled=False)
            window.Element('-LOADVARS-').update(disabled=False)
            window.Element('-PLOT-').update(disabled=False)
            window.refresh()

        # Selected Compare Drivers, enable multi select
        elif event == '-COMPARE-':
            if values['-COMPARE-'] == True:
                window.Element('-DRIVER-').update(select_mode='multiple')
                window.Element('-SLICE-').update(disabled=True)
                window.refresh()
                window.read(timeout=100)
            if values['-COMPARE-'] == False:
                window.Element('-DRIVER-').update(select_mode='single')
                window.Element('-SLICE-').update(disabled=True)
                window.refresh()
                window.read(timeout=100)

        # Load Drivers        
        elif event == '-LOADDRIVERS-':
            ButtonFunc.LoadDriverList()

        # Load Driver VARSs        
        elif event == '-LOADVARS-':
            ButtonFunc.LoadDriverVars()

        # Confirm All
        elif event == '-CONFIRM ALL-':
            window.Element('-PLOT-').update(disabled=False)
            window.refresh()
            window.read(timeout=100)

        # Plot        
        elif event == '-PLOT-':
            analyse()

    window.close()
    exit(0)

###############################################
# Execute Main
###############################################

if __name__ == '__main__':
    sg.theme('DarkRed')
    main()
else:
    sg.theme('DarkRed')
    main()
