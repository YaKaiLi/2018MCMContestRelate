import pymysql  # 导入 pymysql
import numpy
import pandas as pd
import pyflux as pf
#from datetime import datetime
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

def predict_recover(ts, df, diffn):
    if diffn != 0:
        ts.iloc[0] = ts.iloc[0]+df['log'][diffn]
        ts = ts.cumsum()
    ts = numpy.exp(ts)
#    ts.dropna(inplace=True)
    print('还原完成')
    return ts

def test_stationarity(timeseries):
    dftest = adfuller(timeseries, autolag='AIC')
    return dftest[1]
    #此函数返回的是p值

if __name__ == '__main__':

    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root",password="root", db="mcm", port=3306)

    # 使用cursor()方法获取操作游标
    #cur = db.cursor(cursor=pymysql.cursors.DictCursor)
    cur = db.cursor()

    # 1.查询操作
    # 编写sql 查询语句  user 对应我的表名
    sql = "select * from `sesedsneed` WHERE `MSN` = 'NUETB' AND `statecode` = 'CA' ORDER BY `year`"
    cur.execute(sql)  # 执行sql语句

    results = cur.fetchall()  # 获取查询的所有记录
    resnp = numpy.array(results)
    #total = pd.DataFrame(resnp)
    total = pd.DataFrame(resnp,columns=['msn','statecode','year','data'])
    #total.index = total['year'].values
    #total = pd.Series(results)  # 通过元组创建series
    total.index = pd.Index(sm.tsa.datetools.dates_from_range('1960', '2009'))

    #print(total)
    #exit(0)
    '''
    plt.figure(figsize=(30,5))
    plt.plot(total.index,total['data'])
    plt.ylabel('data')
    plt.title('summary')
    plt.show()
    '''
    model = pf.ARIMA(data=total,ar=5,ma=4,integ=0,target='data')
    x = model.fit("MLE")
    x.summary()
    #test_predict = model.predict(5)
    #test_predict = predict_recover(test_predict, total, diffn)
    #print(test_predict)
    #print(model.predict(h=5, intervals=True))
    #model.plot_z(indices=range(1,9))
    #model.plot_fit(figsize=(15,5))
    #model.plot_fit()
    #model.plot_predict_is(h=5,figsize=(30,5))
    #model.plot_predict(h=5)
    #model.predict(h=20)
    #plt.show()
    #print(model.predict(h=41, intervals=True))

    #print(quanzhong)
    #numpy.savetxt('outfile.csv', guiyihua, delimiter=',')
    db.close()  # 关闭连接
