#-\*-coding: utf-8-\*-

import MySQLdb

# 待审核/执行的sql语句（需包含目标数据库的地址、端口 等参数）
def table_structure(operate,mysql_structure,dbqs):
    sql='/* --user=%s;--password=%s;--host=%s;--port=%s;--enable-%s; */\
    inception_magic_start;\
    use %s; %s inception_magic_commit;' % (dbqs.user,dbqs.password,dbqs.host,dbqs.port,operate,dbqs.name,mysql_structure)
    try:
        conn=MySQLdb.connect(host='127.0.0.1',user='',passwd='',db='',port=6669,use_unicode=True,charset="utf8")  # inception的地址、端口等
        cur=conn.cursor()
        cur.execute(sql)
        result=cur.fetchall()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return result

# 获取备份语句
def rollbackdb(backname,backid):
    try:
        conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123456', db = backname, port=3306,use_unicode=True, charset="utf8")
        cur = conn.cursor()
        sql = 'select tablename from $_$Inception_backup_information$_$ where opid_time = %s' %(backid)
        cur.execute(sql)
        tablename = cur.fetchone()
        sql = 'select rollback_statement from %s where opid_time = %s' % (tablename[0],backid)
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return res

