from cgi import test
from readline import get_line_buffer
from tkinter import E
import PySimpleGUI as sg
import functions as fs
import sys
import time
import threading



# --------------------------------- Define the Functions ---------------------------------

def get_lead_list():

    leadData = fs.leadDataRefresh()
    leadList = leadData['email'].values.tolist()
    print('Loading leads')

    return leadData

def get_contact_list():

    contactData = fs.contactDataRefresh()
    contactList = contactData['email'].values.tolist()
    print('Loading contacts')

    return contactData

def get_dais_list():

    daisData = fs.daisDataRefresh()
    daisList = daisData['Email'].values.tolist()
    print('Loading dais leads')

    return daisData


def refresh_all_data(window):
    """
    A worker thread that communicates with the GUI through a queue
    This thread can block for as long as it wants and the GUI will not be affected
    """
    print('Starting thread - will refresh lead Queues')

    leadList = get_lead_list()['email'].values.tolist()
    print(f'Lead Queue refreshed - Current number of leads is {len(leadList)}')

    window['-LEAD LIST-'].update(leadList)
    window['lenLeadList'].update(f'Number of Leads: {len(leadList)}')


    contactList = get_contact_list()['email'].values.tolist()
    print(f'Contact Queue refreshed - Current number of leads is {len(contactList)}')

    window['-CONTACT LIST-'].update(contactList)
    window['lenContactList'].update(f'Number of Contacts: {len(contactList)}')


    daisList = get_dais_list()['Email'].values.tolist()
    print(f'DAIS Queue refreshed - Current number of leads is {len(daisList)}')

    window['-DAIS LIST-'].update(daisList)
    window['lenDaisList'].update(f'Number of DAIS Leads: {len(daisList)}')



def sequence_leads(leadList):
    fs.sequence_leads(leadList, leadList['campaign'])




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

    top_buttons = sg.pin(sg.Column([[sg.Button('Refresh', bind_return_key=True),sg.B('Sequence'), sg.B('Call'), sg.B('Transfer Contacts'), sg.B('Partner Opps - Coming Soon')]]))

    first_col = sg.Column([
        [sg.Text('Current Lead List:', tooltip=find_tooltip)],
        [sg.Listbox(values='', select_mode=sg.SELECT_MODE_EXTENDED, size=(50,20), bind_return_key=True, key='-LEAD LIST-')],
        [sg.Text(f'Number of Leads: {len(leadList)}', tooltip=find_tooltip, k='lenLeadList')],
    ], element_justification='l', expand_x=True, expand_y=True)

    sec_col = sg.Column([
        [sg.Text('Current Contact List:', tooltip=find_tooltip)],
        [sg.Listbox(values='', select_mode=sg.SELECT_MODE_EXTENDED, size=(50,20), bind_return_key=True, key='-CONTACT LIST-')],
        [sg.Text(f'Number of Contacts: {len(contactList)}', tooltip=find_tooltip, k='lenContactList')],
    ], element_justification='l', expand_x=True, expand_y=True)

    third_col = sg.Column([
        [sg.Text('Current DAIS List:', tooltip=find_tooltip)],
        [sg.Listbox(values='', select_mode=sg.SELECT_MODE_EXTENDED, size=(50,20), bind_return_key=True, key='-DAIS LIST-')],
        [sg.Text(f'Number of DAIS Leads: {len(daisList)}', tooltip=find_tooltip, k='lenDaisList')],
    ], element_justification='l', expand_x=True, expand_y=True)


    right_col = [
        [sg.Text('Console Log:', tooltip=find_tooltip)],
        [sg.Output(size=(70, 21), k='console')],

        [sg.Text('Pending Actions:', tooltip=find_tooltip)],
        [sg.Listbox(size=(70, 21), values=actionList, select_mode=sg.SELECT_MODE_EXTENDED, bind_return_key=True, key='-ACTION LIST-')],

        [sg.B('Enable Autopilot'), sg.Button('Autopilot Settings')],
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
    window['-PANE-'].expand(True, True, True)
    window['-DAIS LIST-'].expand(True, True, True)
    window['-ACTION LIST-'].expand(True, True, True)
    window['console'].expand(True, True, True)


    window.bind('<F1>', '-FOCUS FILTER-')
    window.bind('<F2>', '-FOCUS FIND-')
    window.bind('<F3>', '-FOCUS RE FIND-')

    window.bring_to_front()


    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: 
            break


        if event == 'Refresh':
            threading.Thread(target=refresh_all_data, args=(window,), daemon=True).start()
            window.refresh()

        elif event == 'Sequence Leads':
            threading.Thread(target=sequence_leads, args=(), daemon=True).start()


        elif event == 'Enable Autopilot':
            
            leadList = get_lead_list()
            contactList = get_contact_list()
            daisList = get_dais_list()



            window['-LEAD LIST-'].update(leadList)

            consoleLog.append('Updating Contact List')
            window['-CONSOLE LOG-'].update('\n'.join('\n'.join(consoleLog)))
            window.Refresh()


            window['-CONTACT LIST-'].update(contactList)

            consoleLog.append('Updating DAIS Lead List')
            window['-CONSOLE LOG-'].update('\n'.join('\n'.join(consoleLog)))
            window.Refresh()


            window['-DAIS LIST-'].update(daisList)

            window['-ACTION LIST-'].update('\n'.join(actionList[-3:]))

            print('all lists have been updated- ready to start logic')

            if len(leadList) > 0:
                fs.leadSequence()
        
        elif event == 'Call':
            fs.startAutoDialer()
        
        elif event == '-THREAD-':
            print('Got a message back from the thread: ', values[event])


    window.close()

if __name__ == '__main__':
    the_gui()
    print('Exiting Program')