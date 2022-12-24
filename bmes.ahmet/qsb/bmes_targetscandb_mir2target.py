import bmes
import sys
import os
sys.path.append(os.environ['BMESAHMETDIR'])


def bmes_targetscandb_mir2target(mirna, scorethreshold=0.8):
    dbfile = bmes.downloadurl(
        'http://sacan.biomed.drexel.edu/ftp/binf/targetscandb.sqlite')
    import sqlite3
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()

    sql = 'SELECT distinct("generefseqid") FROM "mir2target" WHERE score>=%f AND mirna IN ("%s","%s-3p","%s-5p")' % (
        scorethreshold, mirna, mirna, mirna)
    print('--- SQL: %s\n' % (sql))

    cur.execute(sql)
    rows = cur.fetchall()
    ret = [row[0] for row in rows]
    return ret
