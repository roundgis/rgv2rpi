#encoding: utf-8

#initialize the system

import sqlite3
import rgv_consts
import models
import rg_lib
import settings


def SetRoot(connid):
    connid.execute("insert into rgv_user(id,uno,password,name) values(?,?,?,?)",
                   ("root", rgv_consts.UserNo.ROOT, 'root', "root"))


def main(db_path):
    with rg_lib.DbConnWrap(sqlite3.connect(db_path, check_same_thread=False)) as conn:
        conn.conn_obj.execute("PRAGMA journal_mode=WAL")
        conn.conn_obj.execute("drop table if exists rgv_user")
        conn.conn_obj.execute("drop table if exists {0}".format(models.Group.TBL))
        conn.conn_obj.execute(rg_lib.Sqlite.CreateTable(models.User.USER_TBL, models.User.FIELDS))
        conn.conn_obj.execute(rg_lib.Sqlite.CreateTable(models.Group.TBL, models.Group.FIELDS))
        SetRoot(conn.conn_obj)


if __name__ == "__main__":
    main(settings.BIZ_DB['path'])


