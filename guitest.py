from cgi import test
from readline import get_line_buffer
from tkinter import E
import PySimpleGUI as sg
import functions as fs
import sys
import time
import threading

# --------------------------------- TO-DO LIST ---------------------------------
# FINISH ASSIGNING FUNCTIONS TO ALL BUTTONS
# FIND A USE FOR THE SETTINGS CHECKBOXES
# CREATE A POP-UP WINDOW FOR AUTOPILOT SETTINGS (ONCE YOU DEFINE SETTINGS)
# MAKE A THEME WITH DATABRICKS COLORS



# --------------------------------- Define the Functions ---------------------------------

def autodial():
    fs.startAutoDialer()

    fs.sequence_leads(email, campaign)



# --------------------------------- Create the window ---------------------------------
def the_gui():

    """

    INITIALIZE VARIABLES

    """
    
    leadList = []
    contactList = []
    daisList = []

    print(len(leadList))
    print(len(contactList))
    print(len(daisList))

    consoleLog = []
    actionList = []

    """
    Creates the main window
    :return: The main window object
    :rtype: (sg.Window)
    """
    sg.theme('DarkAmber')
    # First the window layout...2 columns

    find_tooltip = "Find in file\nEnter a string in box to search for string inside of the files.\nFile list will update with list of files string found inside."
    filter_tooltip = "Filter files\nEnter a string in box to narrow down the list of files.\nFile list will update with list of files with string in filename."
    find_re_tooltip = "Find in file using Regular Expression\nEnter a string in box to search for string inside of the files.\nSearch is performed after clicking the FindRE button."

    top_buttons = sg.pin(sg.Column([[sg.Button('Refresh All Data', bind_return_key=True), sg.B('Call Prospects'), sg.B('Unused Button'), sg.B('TEST')]]))

    first_col = sg.Column([
        [sg.Text('Current Lead List:', tooltip=find_tooltip)],
        [sg.B('Refresh Leads', p=((10,0),(5,5))), sg.B('Sequence Leads')],
        [sg.Listbox(values='', select_mode=sg.SELECT_MODE_EXTENDED, size=(50,20), bind_return_key=True, key='-LEAD LIST-')],
        [sg.Text(f'Number of Leads: {len(leadList)}', tooltip=find_tooltip, k='lenLeadList')],
    ], element_justification='l', expand_x=True, expand_y=True)

    sec_col = sg.Column([
        [sg.Text('Current Contact List:', tooltip=find_tooltip)],
        [sg.B('Refresh Contacts', p=((10,0),(5,5))), sg.B('Sequence Contacts')],
        [sg.Listbox(values='', select_mode=sg.SELECT_MODE_EXTENDED, size=(50,20), bind_return_key=True, key='-CONTACT LIST-')],
        [sg.Text(f'Number of non-workable Contacts:', tooltip=find_tooltip, k='lenContactList')],
        [sg.B('Transfer Contacts', p=((10,0),(5,5)))],
        [sg.Listbox(values='', select_mode=sg.SELECT_MODE_EXTENDED, size=(50,20), bind_return_key=True, key='-CONTACT TRANSFER LIST-')],
        [sg.Text(f'Number of non-workable Contacts: {len(contactList)}', tooltip=find_tooltip, k='lenContactTransferList')],
    ], element_justification='l', expand_x=True, expand_y=True)

    suspect_col = sg.Column([
        [sg.Text('Current Suspect Lead List:', tooltip=find_tooltip)],
        [sg.B('Refresh Suspect', p=((10,0),(5,5))), sg.B('Sequence Suspect')],

        [sg.Listbox(values='', select_mode=sg.SELECT_MODE_EXTENDED, size=(50,20), bind_return_key=True, key='-SUSPECT LIST-')],
        [sg.Text(f'Number of Leads: {len(leadList)}', tooltip=find_tooltip, k='lenSuspectList')],
    ], element_justification='l', expand_x=True, expand_y=True)

    third_col = sg.Column([
        [sg.Text('Current DAIS List:', tooltip=find_tooltip)],
        [sg.B('Refresh DAIS', p=((10,0),(5,5))), sg.B('Sequence DAIS')],
        [sg.Listbox(values='', select_mode=sg.SELECT_MODE_EXTENDED, size=(50,20), bind_return_key=True, key='-DAIS LIST-')],
        [sg.Text(f'Number of DAIS Leads: {len(daisList)}', tooltip=find_tooltip, k='lenDaisList')],
    ], element_justification='l', expand_x=True, expand_y=True)


    right_col = [
        [sg.Text('Console Log:', tooltip=find_tooltip)],
        [sg.Output(size=(70, 21), k='console')],
        [sg.B('Enable Autopilot'), sg.Button('Autopilot Settings')],
        [sg.T('Sales Toolkit v2.3 (Development)')],
        [sg.T('PySimpleGUI ver ' + sg.version.split(' ')[0] + '  tkinter ver ' + sg.tclversion_detailed, font='Default 8', pad=(0,0))],
        [sg.T('Python ver ' + sys.version, font='Default 8', pad=(0,0))],
        [sg.T('Interpreter ' + sg.execute_py_get_interpreter(), font='Default 8', pad=(0,0))],
    ]

    options_at_bottom = sg.pin(sg.Column([[sg.CB('Setting 1', enable_events=True, k='-VERBOSE-', tooltip='Enable to see the matches in the right hand column'),
                         sg.CB('Another setting', default=True, enable_events=True, k='-FIRST MATCH ONLY-', tooltip='Disable to see ALL matches found in files'),
                         sg.CB('Yet another setting', default=True, enable_events=True, k='-IGNORE CASE-'),
                         sg.CB('I love checkboxes', default=False, enable_events=True, k='-WAIT-')
                                           ]],
                                         pad=(0,0), k='-OPTIONS BOTTOM-',  expand_x=True, expand_y=False),  expand_x=True, expand_y=False)

    #choose_folder_at_top = sg.pin(sg.Column([[sg.T('Click settings to set top of your tree or choose a previously chosen folder'),
    #                                  sg.Combo(sorted(sg.user_settings_get_entry('-folder names-', [])), default_value=sg.user_settings_get_entry('-demos folder-', ''), size=(50, 30), key='-FOLDERNAME-', enable_events=True, readonly=True)]], pad=(0,0), k='-FOLDER CHOOSE-'))
    # ----- Full layout -----

    layout = [[sg.Text('Databricks Sales Toolkit', font='Any 20')],
              [sg.Pane([top_buttons], orientation='h', relief=sg.RELIEF_SUNKEN, k='-UPPER PANE-')],
              [sg.Pane([sg.Column([[first_col]], element_justification='l',  expand_x=True, expand_y=True), sg.Column([[sec_col]], element_justification='l',  expand_x=True, expand_y=True), sg.Column([[third_col]], element_justification='l',  expand_x=True, expand_y=True), sg.Column([[suspect_col]], element_justification='l',  expand_x=True, expand_y=True), sg.Column(right_col, element_justification='c', expand_x=True, expand_y=True) ], orientation='h', relief=sg.RELIEF_SUNKEN, k='-PANE-')],
              [options_at_bottom, sg.Sizegrip()]]

    # --------------------------------- Create Window ---------------------------------
    window = sg.Window('Sales Toolkit v2.3 - Development Version', layout, finalize=True,  resizable=True, use_default_focus=False, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT)
    window.set_min_size(window.size)

    window['-LEAD LIST-'].expand(True, True, True)
    window['-CONTACT LIST-'].expand(True, True, True)
    window['-CONTACT TRANSFER LIST-'].expand(True, True, True)
    window['-DAIS LIST-'].expand(True, True, True)
    window['-SUSPECT LIST-'].expand(True, True, True)
    window['-PANE-'].expand(True, True, True)
    window['-DAIS LIST-'].expand(True, True, True)
    window['console'].expand(True, True, True)


    window.bind('<F1>', '-FOCUS FILTER-')
    window.bind('<F2>', '-FOCUS FIND-')
    window.bind('<F3>', '-FOCUS RE FIND-')

    window.bring_to_front()


    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: 
            break


        if event == 'Refresh All Data':
            threading.Thread(target=fs.dbsql_refresh_all, args=(window,), daemon=True).start()

        if event == 'Refresh Leads':
            print('This button has not been assigned a function yet')

        if event == 'Sequence Leads':
            threading.Thread(target=fs.sequence_leads, args=(window,), daemon=True).start()

        if event == 'TEST':
            threading.Thread(target=fs.testfunction, args=(window,), daemon=True).start()

        if event == 'Call Prospects':
            threading.Thread(target=autodial, args=(), daemon=True).start()
        
        if event == 'Refresh DAIS':
            print('This button has not been assigned a function yet')

        if event == 'Sequence DAIS':
            print('This button has not been assigned a function yet')

        if event == 'Refresh Contacts':
            print('This button has not been assigned a function yet')

        if event == 'Sequence Contacts':
            print('This button has not been assigned a function yet')

        if event == 'Transfer Contacts':
            print('This button has not been assigned a function yet')

        if event == 'Refresh Suspect':
            print('This button has not been assigned a function yet')

        if event == 'Sequence Suspect':
            print('This button has not been assigned a function yet')

        if event == 'Enable Autopilot':
            print('This button has not been assigned a function yet')            

        if event == 'Autopilot Settings':
            print('This button has not been assigned a function yet')  

        if event == 'Unused Button':
            print('This button has not been assigned a function yet')  


    window.close()

if __name__ == '__main__':
    the_gui()
    print('Exiting Program')