# -*- coding: utf-8 -*-
'''对备份数据库的相关操作'''
import MySQLdb

# 查找回滚语句
def rollbackdb(backname,backid):
    print backname,backid
    try:
        conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123456', db = backname, port=3306,use_unicode=True, charset="utf8")
        cur = conn.cursor()
        sql = "select tablename from $_$Inception_backup_information$_$ where opid_time = %s;" %(backid)
        cur.execute(sql)
        tablename = cur.fetchone()
        sql = "select rollback_statement from %s where opid_time = %s;" % (tablename[0],backid)
        cur.execute(sql)
        res = cur.fetchone()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return res[0]