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

    sg.theme_button_color(color = 'white')
    sg.theme_text_color(color = '#333333')
    sg.theme_input_background_color(color = 'white')
    sg.theme_text_element_background_color(color = 'white')
    sg.theme_element_text_color(color = '#13262e')
    sg.theme_input_text_color(color = '#13262e')

    right_click_email = [['Open in Outreach'], ['Delete']]


    # First the window layout...2 columns

    find_tooltip = "Find in file\nEnter a string in box to search for string inside of the files.\nFile list will update with list of files string found inside."
    filter_tooltip = "Filter files\nEnter a string in box to narrow down the list of files.\nFile list will update with list of files with string in filename."
    find_re_tooltip = "Find in file using Regular Expression\nEnter a string in box to search for string inside of the files.\nSearch is performed after clicking the FindRE button."

    # ----- Home Page Layout Elements -----

    sidebar = [
        [sg.Image(source='./img/logo.png', background_color='#13262e')],
        [sg.B('Control Panel',  p=0, expand_x=True, size=(20,1.5), border_width=0, mouseover_colors=('white','#203742'), button_color=('#acbabf','#13262e'))],
        [sg.B('Partner Tools',  p=0, expand_x=True, size=(20,1.5), border_width=0, mouseover_colors=('white','#203742'), button_color=('#acbabf','#13262e'))], 
        [sg.B('Calling Tools',  p=0, expand_x=True, size=(20,1.5), border_width=0, mouseover_colors=('white','#203742'), button_color=('#acbabf','#13262e'))], 
        [sg.B('Debugging View',  p=0, expand_x=True, size=(20,1.5), border_width=0, mouseover_colors=('white','#203742'), button_color=('#acbabf','#13262e'))],

        [sg.HorizontalSeparator(color = '#acbabf', pad = ((15,15),(400,5)), k = None)],
        [sg.Button('Refresh All Data', bind_return_key=True,expand_x=True, size=(20,1.5), border_width=0, mouseover_colors=('white','#203742'), button_color=('#acbabf','#13262e'))],
        ]

    home_first_col = [
        [sg.Text('Current Lead List:', tooltip=find_tooltip, background_color='#ffffff')],
        [sg.B('Refresh Leads', p=((10,0),(5,5))), sg.B('Sequence Leads')],
        [sg.Listbox(values='', select_mode=sg.SELECT_MODE_EXTENDED, size=(50,20), bind_return_key=True, key='-LEAD LIST-', background_color='#f7f7f7', no_scrollbar=True, right_click_menu=right_click_email)],
        [sg.Text(f'Number of Leads: {len(leadList)}', tooltip=find_tooltip, k='lenLeadList')],
        [sg.Text('Current Contact List:', tooltip=find_tooltip)],
        [sg.B('Refresh Contacts', p=((10,0),(5,5))), sg.B('Sequence Contacts'), sg.B('Transfer Non-Workable')],
        [sg.Listbox(values='', select_mode=sg.SELECT_MODE_EXTENDED, size=(50,20), bind_return_key=True, key='-CONTACT LIST-', background_color='#f7f7f7', no_scrollbar=True)],
        [sg.Text(f'Number of workable Contacts:', tooltip=find_tooltip, k='lenContactList')],
    ]

    home_sec_col = [
        [sg.Text('Current DAIS List:', tooltip=find_tooltip)],
        [sg.B('Refresh DAIS', p=((10,0),(5,5))), sg.B('Sequence DAIS')],
        [sg.Listbox(values='', select_mode=sg.SELECT_MODE_EXTENDED, size=(50,20), bind_return_key=True, key='-DAIS LIST-', background_color='#f7f7f7', no_scrollbar=True)],
        [sg.Text(f'Number of DAIS Leads: {len(daisList)}', tooltip=find_tooltip, k='lenDaisList')],
        [sg.Text('Open Partner Leads:', tooltip=find_tooltip)],
        [sg.B('Refresh Partners', p=((10,0),(5,5)))],
        [sg.Listbox(values='', select_mode=sg.SELECT_MODE_EXTENDED, size=(50,20), bind_return_key=True, key='-PARTNER LIST-', background_color='#f7f7f7', no_scrollbar=True)],
        [sg.Text(f'Number of Partner Leads: {len(daisList)}', tooltip=find_tooltip, k='lenDaisList')],
    ] 


    home_third_col = [
        [sg.Text('Console Log:', tooltip=find_tooltip)],
        [sg.Output(size=(70, 21), k='console', background_color='#f7f7f7')],
        [sg.B('Enable Autopilot'), sg.Button('Autopilot Settings')],
        [sg.T('Sales Toolkit v2.3 (Development)')],
        [sg.T('PySimpleGUI ver ' + sg.version.split(' ')[0] + '  tkinter ver ' + sg.tclversion_detailed, font='Default 8', pad=(0,0))],
        [sg.T('Python ver ' + sys.version, font='Default 8', pad=(0,0))],
        [sg.T('Interpreter ' + sg.execute_py_get_interpreter(), font='Default 8', pad=(0,0))],
    ]


    options_at_bottom = sg.pin(sg.Column([[sg.CB('Setting 1', enable_events=True, k='-VERBOSE-', tooltip='Enable to see the matches in the right hand column', background_color='#13262e', text_color='white'),
                         sg.CB('Another setting', default=True, enable_events=True, k='-FIRST MATCH ONLY-', tooltip='Disable to see ALL matches found in files', background_color='#13262e', text_color='white'),
                         sg.CB('Yet another setting', default=True, enable_events=True, k='-IGNORE CASE-', background_color='#13262e', text_color='white'),
                         sg.CB('I love checkboxes', default=False, enable_events=True, k='-WAIT-', background_color='#13262e', text_color='white')
                        ]], pad=(0,0), k='-OPTIONS BOTTOM-',  expand_x=True, expand_y=False, background_color='#13262e'),  expand_x=True, expand_y=False)

    # ----- Debugging Window Elements -----

    debugging_pane1 = [
                [sg.Text('Auto Sequencer:', tooltip=find_tooltip)], # Need to update tooltip 
                [sg.Image(source='./img/test.png', background_color='white', size=(250,250))],
    ]

    debugging_pane2 = [
                [sg.Text('Auto Dialer:', tooltip=find_tooltip)], # Need to update tooltip 
                [sg.Image(source='./img/test.png', background_color='white', size=(250,250))],
    ]

    debugging_pane3 = [
                [sg.Text('Auto Contact Transfer:', tooltip=find_tooltip)], # Need to update tooltip 
                [sg.Image(source='./img/test.png', background_color='white', size=(250,250))],
    ]

    debugging_pane4 = [
                [sg.Text('Auto Contact Transfer:', tooltip=find_tooltip)], # Need to update tooltip 
                [sg.Image(source='./img/test.png', background_color='white', size=(250,250))],
    ]


    # ----- LAYOUTS -----




    # ----- Home Page Window Layout -----

    home_col1 = sg.Column(home_first_col, element_justification='l',  expand_x=True, expand_y=True, background_color='#ffffff', pad=0, k='-home_col1-')
    home_col2 = sg.Column(home_sec_col, element_justification='l',  expand_x=True, expand_y=True, background_color='#ffffff', k='-home_col2-')
    home_col3 = sg.Column(home_third_col, element_justification='l',  expand_x=True, expand_y=True, background_color='#ffffff', k='-home_col3-')

    # ----- Debug Page Window Layout -----

    debug_col1 = sg.Column(debugging_pane1, element_justification='c',  expand_x=True, expand_y=True, visible=False, background_color='#ffffff', k='-debug_col1-')
    debug_col2 = sg.Column(debugging_pane2, element_justification='c',  expand_x=True, expand_y=True, visible=False, background_color='#ffffff', k='-debug_col2-')
    debug_col3 = sg.Column(debugging_pane3, element_justification='c',  expand_x=True, expand_y=True, visible=False, background_color='#ffffff', k='-debug_col3-')
    debug_col4 = sg.Column(debugging_pane4, element_justification='c',  expand_x=True, expand_y=True, visible=False, background_color='#ffffff', k='-debug_col4-')


    # ----- Full Window Layout -----

    layout = [
                [sg.Column(sidebar, element_justification='l', expand_y=True, expand_x=False, background_color='#13262e', k='sidebar', pad=(0,0)),
                    sg.Pane(
                        [

                            # -- HOME PAGE --
                            home_col1,
                            home_col2,
                            home_col3,
                            # -- DEBUG PAGE -- 
                            debug_col1, 
                            debug_col2,
                            debug_col3,
                            debug_col4,

                        ], orientation='h', relief=sg.RELIEF_SUNKEN, k='-PANE-', background_color='#ffffff' ,pad=0)
                ],
                [options_at_bottom, sg.Sizegrip(background_color = '#13262e')]
            ]

    # --------------------------------- Create Window ---------------------------------
    window = sg.Window('Sales Toolkit v2.3 - Development Version', layout, finalize=True,  resizable=True, use_default_focus=False, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, margins=(0,0), background_color='white')
    window.set_min_size(window.size)


    window['-LEAD LIST-'].expand(True, True, True)
    window['-CONTACT LIST-'].expand(True, True, True)
    window['-DAIS LIST-'].expand(True, True, True)
    window['-PANE-'].expand(True, True, True)
    window['-DAIS LIST-'].expand(True, True, True)
    window['console'].expand(True, True, True)
    window['-PARTNER LIST-'].expand(True, True, True)
    window['sidebar'].expand(expand_x=False, expand_y=True)



    window.bind('<F1>', '-FOCUS FILTER-')
    window.bind('<F2>', '-FOCUS FIND-')
    window.bind('<F3>', '-FOCUS RE FIND-')

    window.bring_to_front()



    # ----- Event Listener -----


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

# TODO: Create a helper function to eliminate all this copy/paste bullshit 

        if event == 'Debugging View':
            window['-home_col1-'].update(visible=False)
            window['-home_col2-'].update(visible=False)
            window['-home_col3-'].update(visible=False)

            window['-debug_col1-'].update(visible=True)
            window['-debug_col2-'].update(visible=True)
            window['-debug_col3-'].update(visible=True)
            window['-debug_col4-'].update(visible=True)
        

        if event == 'Control Panel':
            window['-home_col1-'].update(visible=True)
            window['-home_col2-'].update(visible=True)
            window['-home_col3-'].update(visible=True)

            window['-debug_col1-'].update(visible=False)
            window['-debug_col2-'].update(visible=False)
            window['-debug_col3-'].update(visible=False)
            window['-debug_col4-'].update(visible=False)

        if event == 'Calling Tools':
            window['-home_col1-'].update(visible=False)
            window['-home_col2-'].update(visible=False)
            window['-home_col3-'].update(visible=False)

            window['-debug_col1-'].update(visible=False)
            window['-debug_col2-'].update(visible=False)
            window['-debug_col3-'].update(visible=False)
            window['-debug_col4-'].update(visible=False)

        if event == 'Partner Tools':
            window['-home_col1-'].update(visible=False)
            window['-home_col2-'].update(visible=False)
            window['-home_col3-'].update(visible=False)

            window['-debug_col1-'].update(visible=False)
            window['-debug_col2-'].update(visible=False)
            window['-debug_col3-'].update(visible=False)
            window['-debug_col4-'].update(visible=False)

        if event == 'Call Prospects':
            threading.Thread(target=fs.startAutoDialer, args=(), daemon=True).start()
        
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
    print('Exiting Program')
    the_gui()