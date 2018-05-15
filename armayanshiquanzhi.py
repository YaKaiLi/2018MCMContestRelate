import pymysql  # 导入 pymysql
import numpy
import pandas as pd
import pyflux as pf
#from datetime import datetime
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

if __name__ == '__main__':

    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root",password="root", db="mcm", port=3306)

    # 使用cursor()方法获取操作游标
    #cur = db.cursor(cursor=pymysql.cursors.DictCursor)
    cur = db.cursor()

    # 1.查询操作
    # 编写sql 查询语句  user 对应我的表名
    sql = "select data from `sesedsneed_copy` WHERE `MSN` = 'WWTCB' AND `statecode` = 'AZ' ORDER BY `year`"
    cur.execute(sql)  # 执行sql语句

    results = cur.fetchall()  # 获取查询的所有记录
    resnp = numpy.array(results)
    total = pd.DataFrame(resnp)
    #total = pd.DataFrame(resnp,columns=['msn','statecode','year','data'])
    #total.index = total['year'].values
    #total = pd.Series(results)  # 通过元组创建series
    #total.index = pd.Index(sm.tsa.datetools.dates_from_range('1960', '2009'))
    #print(total)
    #exit(0)
    #diff[0][0] = 1
    #total['log'] = numpy.log(total[0])
    total.index = pd.Index(sm.tsa.datetools.dates_from_range('1960', '2009'))
    total.columns = ['data']
    model = pf.ARIMA(data=total,ar=4,ma=4,integ=0,target='data')
    x = model.fit("MLE")
    predict = model.predict(5)

    #x.summary()
    #print(quanzhong)
    #numpy.savetxt('outfile.csv', guiyihua, delimiter=',')
    db.close()  # 关闭连接