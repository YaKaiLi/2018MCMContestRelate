from __future__ import print_function
import pandas as pd
import pymysql
import numpy as np
from scipy import  stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARMA

def proper_model(data_ts, maxLag):
    init_bic = float("inf")
    init_p = 0
    init_q = 0
    init_properModel = None
    for p in np.arange(maxLag):
        for q in np.arange(maxLag):
            model = ARMA(data_ts, order=(p, q))
            try:
                results_ARMA = model.fit(disp=-1, method='css')
            except:
                continue
            bic = results_ARMA.bic
            if bic < init_bic:
                init_p = p
                init_q = q
                init_properModel = results_ARMA
                init_bic = bic
    return init_bic, init_p, init_q, init_properModel

if __name__ == '__main__':
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root",password="root", db="mcm", port=3306)

    # 使用cursor()方法获取操作游标
    #cur = db.cursor(cursor=pymysql.cursors.DictCursor)
    cur = db.cursor()

    # 1.查询操作
    # 编写sql 查询语句
    sql = "select floor(data) from `sesedsneed` WHERE `MSN` = 'SOTCB' AND `statecode` = 'AZ' ORDER BY `year`"
    cur.execute(sql)  # 执行sql语句

    results = cur.fetchall()  # 获取查询的所有记录
    resnp = np.array(results)
    total = pd.DataFrame(resnp,columns=['data'])
    #total = pd.Series(results)  # 通过元组创建series
    total.index = pd.Index(sm.tsa.datetools.dates_from_range('1960', '2009'))
    print(proper_model(total,8))

    db.close()  # 关闭连接