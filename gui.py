import datetime
import os
import webbrowser

import fastf1
import matplotlib.pylab as plt
import PySimpleGUI as sg
from fastf1 import plotting
from pandas import DataFrame

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
# Define Year List for GPs (2018+ Available)
###############################################

##############################

import fastf1
from fastf1 import plotting

class Session:

    # Create Session Object
    # event = Session(year, gp, ses)
    def __init__(self, year, gp, ses):
        self.year = year
        self.gp = gp
        self.ses = ses

    # Load Session Object's data
    # Session.load(eventIQ)
    def load(self):
        CacheDir.Set(CacheDir.default)
        fastf1.Cache.enable_cache(CacheDir.default)
        session = fastf1.get_session(self.year, self.gp, self.ses)
        session.load()
        self.session = session
        self.results = session.results
        self.event_name = session.event['EventName']

class DriverIQ:
    #Load Driver Data
    #info = eventIQ.session.get_driver('identifier')
    def __init__(self, id):
        self.info = eventIQ.session.get_driver(id)
        self.ses = eventIQ.session.laps.pick_driver(id)
        self.data = None
        self.fullname = self.info['FullName']
        self.team = self.info['TeamName']
        self.team_color = fastf1.plotting.team_color(self.team)


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
    SessionSlice = make('SessionSlice', ['Full Session', 'Specific Lap', 'Fastest'])
    DriverVars = make('DriverVars', ['Var 1', 'Var 2', 'Var 3'])

###############################################
# Define Window
###############################################

def make_window():
    sg.theme('DarkBlack')

    menu_def = [[('&porpo'), ['&About', ('&Preferences'), ['&Set Cache Directory', 'Set Export Directory'], '&GitHub', 'E&xit']]]
    
    header_layout = [[sg.Image(source='src/common/images/icon_small.png', size=(120,60), expand_x=True, expand_y=True)],]

    layout = [[sg.Menubar(menu_def, key='-MENU-')],
                [sg.Frame('', header_layout, size=(250,75), key='-HEAD-')],
                [sg.OptionMenu(Lists.Years.list, default_value=f'{Lists.Years.list[-1]}', expand_x=True, key='-YEAR-')],
                [sg.Button('Load Season', expand_x=True)],
                [sg.Listbox(Lists.GrandPrix.list, enable_events=True, expand_x=True, size=(None,10), select_mode='single', horizontal_scroll=False, visible=False, pad=(7,7,7,7), key='-GP-')],
                [sg.OptionMenu(Lists.Sessions.list, default_value=f'Select Session...', expand_x=True, visible=False, key='-SESSION-')],
                [sg.Button('Load Drivers for Session', visible=False, expand_x=True, key='-LOADDRIVERS-')],
                [sg.Listbox(Lists.Drivers.list, enable_events=True, expand_x=True, size=(None,10), select_mode='single', horizontal_scroll=False, visible=False, pad=(7,7,7,7), key='-DRIVER-')],
                [sg.OptionMenu(Lists.SessionSlice.list, default_value=f'Evalutate Full Session?', expand_x=True, visible=False, key='-SLICE-')],
                [sg.Button('Select Driver Data Points', visible=False, expand_x=True, key='-LOADVARS-')],
                [sg.OptionMenu(Lists.DriverVars.list, default_value='.Y Variable...', expand_x=True, visible=False, key='-DRIVERYVAR-')],
                [sg.OptionMenu(Lists.DriverVars.list, default_value='.X Variable...', expand_x=True, visible=False, key='-DRIVERXVAR-')],
                [sg.Button('Confirm All', visible=False, expand_x=True, key='-CONFIRM ALL-')],
                [sg.Button('Analyse', visible=False, disabled=True, expand_x=True, key='-PLOT-')], 
                ]

    window = sg.Window('porpo', layout, margins=(0, 0), finalize=True)

    window.set_min_size(window.size)
    
    return window

###############################################
# Define Main fuction to run Window
###############################################

def main():
    window = make_window()

    # Window Open, Begin Event Loop
    while True:
        event, values = window.read(timeout=100)
        
###############################################
# Define what happens when a button is pushed
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
                window.Element('-LOADDRIVERS-').update(visible=True)
                window.Element('-DRIVER-').update(visible=False)
                window.refresh()
                window.read(timeout=100)

            # Load Drivers
            def LoadDriverList():
                print(f"[LOG] Load Drivers for ...")
                global eventIQ
                eventIQ = Session(int(values['-YEAR-']), str(values['-GP-']), str(values['-SESSION-']))
                Session.load(eventIQ)
                results = eventIQ.session.results
                drivers = results['Abbreviation']
                Lists.Drivers = Lists.make('Drivers', list(drivers))
                window.Element('-DRIVER-').update(values=Lists.Drivers.list)
                window.Element('-DRIVER-').update(visible=True)
                window.Element('-SLICE-').update(visible=True)
                window.Element('-LOADVARS-').update(visible=True)
                window.refresh()
                window.read(timeout=100)

            def LoadDriverVars():
                print(f"[LOG] Load variables for {values['-DRIVER-'][0]}")
                global driver
                id = values['-DRIVER-'][0]
                driver = DriverIQ(id)
                info = driver.info
                ses = driver.ses
                fullname = driver.fullname
                team = driver.team
                team_color = driver.team_color
                print(f'Getting data for {fullname}...\n')

                if values['-SLICE-'] == 'Fastest':
                    f_lap = ses.pick_fastest()
                    fastest_lap = f_lap.get_telemetry()
                    driver.data = fastest_lap
                    var_list = list(driver.data)

                elif values['-SLICE-'] == 'Specific Lap':
                    #driver.data = None
                    # var_list = list(driver.data)
                    pass

                else:
                    driver.data = ses
                    var_list = list(driver.data)
                
                var_list = list(driver.data)
                Lists.DriverVars = Lists.make('DriverVars', var_list)
                window.Element('-DRIVERXVAR-').update(values=Lists.DriverVars.list)
                window.Element('-DRIVERYVAR-').update(values=Lists.DriverVars.list)
                window.Element('-DRIVERXVAR-').update(visible=True)
                window.Element('-DRIVERYVAR-').update(visible=True)
                window.Element('-CONFIRM ALL-').update(visible=True)
                window.Element('-PLOT-').update(visible=True)
                window.refresh()
                window.read(timeout=100)
                

            def Confirm():
                window.Element('-PLOT-').update(disabled=False)
                window.refresh()
                window.read(timeout=100)

            def Analyse():
                print(f"[LOG] Plotting variables for {values['-DRIVER-']}")

                driver_yvar = driver.data[f"{values['-DRIVERYVAR-']}"]
                driver_xvar = driver.data[f"{values['-DRIVERXVAR-']}"]
                x = driver_xvar
                y = driver_yvar
                xmin, xmax = x.min(), x.max()
            
                fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1', misc_mpl_mods=True)
                fig = plt.figure(1, figsize=(16,9), constrained_layout=True)
                plot1 = fig.subplots()
                plot1.plot(x, y, color=driver.team_color, label=f"{y.name}")
                plot1.set_ylabel(f"{y.name}")
                plot1.set_xlabel(f"{x.name}")
                plot1.set_xlim(xmin, xmax)
                plot1.minorticks_on()
                plot1.grid(visible=True, axis='both', which='major', linewidth=0.8, alpha=.5)
                plot1.grid(visible=True, axis='both', which='minor', linestyle=':', linewidth=0.5, alpha=.5)
                plt.suptitle(f"{values['-DRIVER-'][0]} - {values['-GP-'][0]}\n{values['-DRIVERYVAR-']} Analysis")
                plt.savefig(f"{ExportDir.default}/Plot.png", dpi=300)
                plt.show()


###############################################
# Begin 'If' Events for Button Push
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

        # Load Drivers        
        elif event == '-LOADDRIVERS-':
            ButtonFunc.LoadDriverList()

        # Load Drivers        
        elif event == '-LOADVARS-':
            ButtonFunc.LoadDriverVars()

        # Confirm All
        elif event == '-CONFIRM ALL-':
            ButtonFunc.Confirm()

        # Plot        
        elif event == '-PLOT-':
            ButtonFunc.Analyse()

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