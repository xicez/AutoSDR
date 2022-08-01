from databricks import sql
from functions import dbsql_contactrefresh
import login as lg

# --------------------------------- DATABRICKS SQL CONNECTOR ---------------------------------

def dbsql_init():
    connection = sql.connect(server_hostname = lg.DATABRICKS_SERVER_HOSTNAME,
                            http_path = lg.DATABRICKS_HTTP_PATH,
                            access_token = lg.DATABRICKS_TOKEN)
    return connection

def dbsql_kill(cursor, connection):
    cursor.close()
    connection.close()


def dbsql_leadrefresh():

    print('Initializing DB SQL Connection...')
    connection = dbsql_init()
    cursor = connection.cursor()
    
    print('Executing SQL Query...')
    cursor.execute('SELECT * FROM nigel.openleadqueue')
    
    result = cursor.fetchall()
    
    email = [row.email for row in result]
    campaign = [row.OutreachCampaign for row in result]

    leadResult = {email[i]: campaign[i] for i in range(len(email))} 

    print('Terminating DB SQL Connection')
    dbsql_kill(cursor, connection)

    return leadResult

def dbsql_query(delta_table):

    print('Initializing DB SQL Connection...')
    connection = dbsql_init()
    cursor = connection.cursor()
    
    print('Executing SQL Query...')
    cursor.execute(f'SELECT * FROM nigel.{delta_table}')
    
    result = cursor.fetchall()
    
    email = [row.email for row in result]
    campaign = [row.OutreachCampaign for row in result]

    leadResult = {email[i]: campaign[i] for i in range(len(email))} 

    print('Terminating DB SQL Connection')
    dbsql_kill(cursor, connection)

    return leadResult



class KPI: 
    def __init__(self):
        self.weekly_calls = 0
        self.weekly_connects = 0

        self.open_leads = len(dbsql_leadrefresh())
        self.open_partners = 0

    def refresh(self):
        self.weekly_calls = 200
        self.weekly_connects = 1000
        self.open_leads = 200
        self.open_partners = 999
        

kpi = KPI()

print(f'Calls: {kpi.weekly_calls}, Connects: {kpi.weekly_connects}, Open Leads: {kpi.open_leads}, Open Partners: {kpi.open_partners}')

kpi.refresh()

print(f'Calls: {kpi.weekly_calls}, Connects: {kpi.weekly_connects}, Open Leads: {kpi.open_leads}, Open Partners: {kpi.open_partners}')


