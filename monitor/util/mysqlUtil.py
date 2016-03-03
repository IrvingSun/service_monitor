#!encoding=UTF-8

import MySQLdb
import MySQLdb.cursors

from log import logger, Log


class DbBase(object):
    """DbBase 数据库操作基类，管理连接的获取和关闭"""

    def __init__(self, arg):
        self.host = arg['host']
        self.port = arg['port']
        self.dbname = arg['dbname']
        self.user = arg['user']
        self.password = arg['password']

    def get_con(self):
        con = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.dbname,
                              port=self.port, charset="utf8", cursorclass=MySQLdb.cursors.DictCursor)
        return con

    def execute_slef(self, sqls, cursor):
        """ 自定义执行sql实现 """
        results = {}
        return results

    def execute_sql(self, sqls, fun=execute_slef):
        # 连接mysql，获取连接的对象
        conn = self.get_con()
        # 获取连接的cursor对象，用于执行查询
        cursor = conn.cursor()
        logger.info("sql=" + "; ".join(list(sqls)))
        try:
            # 执行sql
            results = fun(sqls, cursor)
            # 提交事务
            conn.commit()
        except Exception, e:
            # 回滚
            conn.rollback()
            raise e
        finally:
            # 关闭资源
            cursor.close()
            conn.close()

        return results


class MysqlUtil(DbBase):
    """MysqlUtil 数据库常用操作"""

    def __init__(self, arg):
        # 初始化 DbBase中的数据库基本信息
        super(MysqlUtil, self).__init__(arg)

    def execute_modify(self, sqls, cursor):
        """ 数据 增、删、改 """
        n = cursor.execute(sqls[0])
        return n

    def execute_query(self, sqls, cursor):
        """ 数据查询 """
        cursor.execute(sqls[0])
        # 使用fetchall函数，将结果集（多维元组）存入rows里面
        results = cursor.fetchall()
        return results

    def execute_multi_sql(self, sqls, cursor):
        """ 多语句执行，无返回 """
        return map(lambda sql: cursor.execute(sql), sqls)

    @Log(True)
    def do_query(self, sql):
        """ 外部调用 查询 """
        try:
            results = self.execute_sql([sql], fun=self.execute_query)
        except Exception, e:
            logger.error('do_query error')
            raise e
        return results

    @Log(True)
    def do_modify(self, sql):
        """ 外部调用 修改 """
        try:
            results = self.execute_sql([sql], fun=self.execute_modify)
        except Exception, e:
            logger.error('do_modify error')
            raise e
        return results

    @Log(True)
    def do_multi_sql(self, sqls):
        """ 外部多sql语句调用 """
        try:
            results = self.execute_sql(sqls, fun=self.execute_multi_sql)
        except Exception, e:
            logger.error('do_multi_sql error')
            raise e
        return results


if __name__ == '__main__':
    dbInfo = {
        "host": "",
        "port": ,
        "dbname": "",
        "user": "",
        "password": ""
    }
    mysqlUtil = MysqlUtil(dbInfo)
    sql1 = "select * from address_freight limit 1"
    result1 = mysqlUtil.do_query(sql1)
    sql2 = "update operate_log set yn = 1 where id = 1957"
    result2 = mysqlUtil.do_modify(sql2)
    sql3 = "update operate_log set yn = 1 where id = 1958"
    result3 = mysqlUtil.do_multi_sql([sql2, sql3])

    print result1, '\n', result2, '\n', result3
