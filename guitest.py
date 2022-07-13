from cgi import test
from readline import get_line_buffer
from tkinter import E
import PySimpleGUI as sg
import functions as fs
import sys

def testfunc():
    print('The test worked')

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('AutoSDR - Development Version v2.2.1', justification='center')],
            [sg.Text('Number of Leads:'), sg.Text(size=(15,1), key='-LEADOUTPUT-'), sg.Text('Number of Contacts:'), sg.Text(size=(15,1), key='-CONTACTOUTPUT-')],
            [sg.Text('Number of DAIS Leads:'), sg.Text(size=(15,1), key='-DAISLEADOUTPUT-'), sg.Text('Number of Partner Leads:'), sg.Text(size=(15,1), key='-PARTNEROUTPUT-')],
            [sg.Text('Functions:')],
            [sg.Button('Sequence Prospects'), sg.Button('Call Prospects'), sg.Button('Transfer Contacts'), sg.Button('Manual Data Refresh')],
            [sg.Text('Under Development:')],
            [sg.Button('[Coming Soon] Sequence Partner Leads'), sg.Button('[Coming Soon] Create Partner Opps'), sg.Button('[Coming Soon] Sequence DAIS Leads')] 
        ]
# Create the Window
#window = sg.Window('AutoSDR v2.2.1 (Development Version)', layout)

def get_lead_list():
    """
    Returns list of filenames of files to display
    No path is shown, only the short filename
    :return: List of filenames
    :rtype: List[str]
    """

    ld = fs.leadDataRefresh()
    leadList = ld['email'].values.tolist()
    print(leadList)
    return leadList




ML_KEY = '-ML-'         # Multline's key


# --------------------------------- Create the window ---------------------------------
def make_window():
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

    top_buttons = sg.pin(sg.Column([[sg.Button('Refresh'),sg.B('Sequence'), sg.B('Call'), sg.B('Coming Soon'), sg.B('Coming Soon')]]))

    first_col = sg.Column([
        [sg.Text('Current Lead List:', tooltip=find_tooltip)],
        [sg.Listbox(values=get_lead_list(), select_mode=sg.SELECT_MODE_EXTENDED, size=(50,20), bind_return_key=True, key='-LEAD LIST-')],
    ], element_justification='l', expand_x=True, expand_y=True)

    sec_col = sg.Column([
        [sg.Text('Current Contact List:', tooltip=find_tooltip)],
        [sg.Listbox(values=get_lead_list(), select_mode=sg.SELECT_MODE_EXTENDED, size=(50,20), bind_return_key=True, key='-CONTACT LIST-')],
    ], element_justification='l', expand_x=True, expand_y=True)

    third_col = sg.Column([
        [sg.Text('Current DAIS List:', tooltip=find_tooltip)],
        [sg.Listbox(values=get_lead_list(), select_mode=sg.SELECT_MODE_EXTENDED, size=(50,20), bind_return_key=True, key='-DAIS LIST-')],
    ], element_justification='l', expand_x=True, expand_y=True)


    right_col = [
        [sg.Multiline(size=(70, 21), write_only=True, key=ML_KEY, reroute_stdout=True, echo_stdout_stderr=True, reroute_cprint=True)],
        [sg.B('Settings'), sg.Button('Exit')],
        [sg.T('AutoSDR v2.2.1 (Development)')],
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

    layout = [[sg.Text('AutoSDR Toolkit', font='Any 20')],
              [sg.Pane([top_buttons], orientation='h', relief=sg.RELIEF_SUNKEN, k='-UPPER PANE-')],
              [sg.Pane([sg.Column([[first_col]], element_justification='l',  expand_x=True, expand_y=True), sg.Column([[sec_col]], element_justification='l',  expand_x=True, expand_y=True), sg.Column([[third_col]], element_justification='l',  expand_x=True, expand_y=True), sg.Column(right_col, element_justification='c', expand_x=True, expand_y=True) ], orientation='h', relief=sg.RELIEF_SUNKEN, k='-PANE-')],
              [options_at_bottom, sg.Sizegrip()]]

    # --------------------------------- Create Window ---------------------------------
    window = sg.Window('AutoSDR v2.2.1 - Development Version', layout, finalize=True,  resizable=True, use_default_focus=False, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT)
    window.set_min_size(window.size)

    window['-LEAD LIST-'].expand(True, True, True)
    window['-CONTACT LIST-'].expand(True, True, True)
    window['-DAIS LIST-'].expand(True, True, True)
    window[ML_KEY].expand(True, True, True)
    window['-PANE-'].expand(True, True, True)


    window.bind('<F1>', '-FOCUS FILTER-')
    window.bind('<F2>', '-FOCUS FIND-')
    window.bind('<F3>', '-FOCUS RE FIND-')


    # sg.cprint_set_output_destination(window, ML_KEY)
    window.bring_to_front()
    return window










while True:
    window = make_window()
    event, values = window.read()
    if event == sg.WIN_CLOSED: 
        break
    
    if event == 'Sequence Prospects':
        testfunc()

    if event == 'Call Prospects':
        testfunc()

    if event == 'Transfer Contacts':
        testfunc()

    if event == 'Manual Data Refresh':
        get_lead_list()

    if event == '[Coming Soon] Sequence Partner Leads':
        testfunc()

    if event == '[Coming Soon] Create Partner Opps':
        testfunc()

    if event == '[Coming Soon] Sequence DAIS Leads':
        testfunc()

window.close()
