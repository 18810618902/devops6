#!/usr/bin/python
#-\*-coding: utf-8-\*-

import MySQLdb

# 待审核/执行的sql语句（需包含目标数据库的地址、端口 等参数）
def table_structure(dbaddr,dbname, mysql_structure):
    #sql='/* --user=root;--password=123456;--host=192.168.1.233;--port=3306;--enable-execute; */\
    sql='/* %s;--enable-check; */\
    inception_magic_start;\
    use  %s; %s inception_magic_commit;' % (dbaddr,dbname,mysql_structure)
    try:
        conn=MySQLdb.connect(host='127.0.0.1',user='',passwd='',db='',port=6669,use_unicode=True,charset="utf8")  # inception的地址、端口等
        cur=conn.cursor()
        ret=cur.execute(sql)
        result=cur.fetchall()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return   result