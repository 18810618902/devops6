#!/usr/bin/python
#-\*-coding: utf-8-\*-

import MySQLdb



def mysql_stuct(sql_struct):

    # 待审核/执行的sql语句（需包含目标数据库的地址、端口 等参数）
    sql1 = '/* --user=root;--password=123456;--host=10.10.10.90;--port=3306;--enable-execute; */\
    inception_magic_start;\
    use inc_test;'
    sql2 = 'inception_magic_commit;'
    sql = sql1 + sql_struct + sql2
    print sql
    try:
        conn=MySQLdb.connect(host='10.10.10.90',user='',passwd='',db='',port=6669,use_unicode=True,charset="utf8")  # inception的地址、端口等
        cur=conn.cursor()
        ret = cur.execute(sql)
        result=cur.fetchall()
        print result
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
         print "Mysql Error {}".format(e)



if __name__ == '__main__':
    mysql_stuct('insert into mytable1 (myname) values ("zhangsan"),("lisi");')