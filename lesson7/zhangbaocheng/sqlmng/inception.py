#!/usr/bin/env python
# -*-coding:utf-8 -*-
import MySQLdb
def  table_structure(mysql_structure):

    # 待审核/执行的sql语句（需包含目标数据库的地址、端口 等参数）                                                                                  
    sql1='/* --user=root;--password=123456;--host=192.168.8.114;--port=3306;--enable-execute; */\
    inception_magic_start;'
    sql2 = 'inception_magic_commit;'
    sql = sql1 + mysql_structure + sql2 
    try:
        conn=MySQLdb.connect(host='127.0.0.1',user='',passwd='',db='',port=6669,use_unicode=True,charset="utf8")  # inception的地址
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
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

