#!/usr/bin/python
#-\*-coding: utf-8-\*-

import pymysql

def table_structure(mysql_structure):
    sql='/* --user=inc;--password=123456;--host=192.168.10.240;--port=3306;--enable-execute; */\
    inception_magic_start;\
    %s\
    inception_magic_commit;' % mysql_structure

    print sql
    try:
        conn=pymysql.connect(host='127.0.0.1',user='',passwd='',db='',port=6669,use_unicode=True,charset="utf8")
        cur=conn.cursor()
        ret=cur.execute(sql)
        result=cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        print result
        '''
        for row in result:
            print row[0], "|",row[1],"|",row[2],"|",row[3],"|",row[4],"|",
            row[5],"|",row[6],"|",row[7],"|",row[8],"|",row[9],"|",row[10]
        '''
        cur.close()
        conn.close()
    except pymysql.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])