import sqlite3
import os.path
import scipy as sp
import Match
from Classifier import LMS
from Classifier import MS
from sqlite3 import Error
from operator import itemgetter



def create_connection(db_file):
    # Code from https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
    # create a database connection to the SQLite database
    #   specified by the db_file
    # :param db_file: database file
    # :return: Connection object or None
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn



def get_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT home_team_api_id, away_team_api_id, home_team_goal, away_team_goal, b365h, b365d, b365a, bwh, bwd, bwa, iwh, iwd, iwa, lbh, lbd, lba FROM Match;")    
    return cur.fetchall()

def get_m(data):
    m = []
    for d in data:
        b365 = [d[i] for i in range(4,7)]
        bw = [d[i] for i in range(7,10)]
        iw = [d[i] for i in range(10,13)]
        lb = [d[i] for i in range(13,16)]
        if (None in b365) or (None in bw) or (None in iw) or (None in lb):
            continue   
        mi = Match.Match(home=d[0],
                         away=d[1],
                         home_goals=d[2],
                         away_goals=d[3],
                         b365=b365,
                         bw=bw,
                         iw=iw,
                         lb=lb)
        m.append(mi)
    return m

def do_LMS(m):
    all_acc = {}

    b365_classifier = LMS(m, "b365")
    all_acc["b365"] = b365_classifier.start()   

    bw_classifier = LMS(m, "bw")
    all_acc["bw"] = bw_classifier.start()

    iw_classifier = LMS(m, "iw")
    all_acc["iw"] = iw_classifier.start()

    lb_classifier = LMS(m, "lb")
    all_acc["lb"] = lb_classifier.start()

    for (k,v) in all_acc.items():
        print(f"[LMS] Company: {k} \t Average Accuracy: {v}")
    print(f"\n[LMS] Company with the most accuracy: {max(all_acc.items(), key=itemgetter(1))[0]} ({max(all_acc.values())})")

def do_MS(m):
    all_acc = {}

    b365_classifier = MS(m, "b365")
    all_acc["b365"] = b365_classifier.start()

    b365_classifier = MS(m, "bw")
    all_acc["bw"] = b365_classifier.start()

    b365_classifier = MS(m, "iw")
    all_acc["iw"] = b365_classifier.start()

    b365_classifier = MS(m, "lb")
    all_acc["lb"] = b365_classifier.start()

    for (k,v) in all_acc.items():
        print(f"[MS] Company: {k} \t Average Accuracy: {v}")
    print(f"\n[MS] Company with the most accuracy: {max(all_acc.items(), key=itemgetter(1))[0]} ({max(all_acc.values())})")



def main():   
        
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "database.sqlite")
    conn = create_connection(db_path)
    data = get_data(conn)
    m = get_m(data)
    
    print("Starting LMS Algorithm...")
    do_LMS(m)
    print("End of LMS Algorithm.")

    print(50*"=")

    print("Starting MS Algorithm...")
    do_MS(m)
    print("End of MS Algorithm.")
    

if __name__ == "__main__":
    main()
    pass