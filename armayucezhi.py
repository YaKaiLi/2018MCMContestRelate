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
        ts.iloc[0] = ts.iloc[0]+df['log'][49]
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
    sql = "select data from `sesedsneed_copy` WHERE `MSN` = 'WYTCB' AND `statecode` = 'TX' ORDER BY `year`"
    cur.execute(sql)  # 执行sql语句

    results = cur.fetchall()  # 获取查询的所有记录
    resnp = numpy.array(results)
    total = pd.DataFrame(resnp)
    diffn=1
    #print(total)
    #exit(0)
    total_diff = total.diff(diffn)
    #diff[0][0] = 1
    #total['log'] = numpy.log(total[0])
    total_diff.dropna(inplace=True)
    total_diff = pd.DataFrame(total_diff)
    total_diff.columns = ['diff']
    total_diff.index = pd.Index(sm.tsa.datetools.dates_from_range('1961', '2009'))
    total.index = pd.Index(sm.tsa.datetools.dates_from_range('1960', '2009'))
    total.columns = ['data']
    model = pf.ARIMA(data=total_diff,ar=1,ma=1,integ=0,target='diff')
    x = model.fit("MLE")
    predict_diff = model.predict(h=40)

    predict_diff.iloc[0] = predict_diff.iloc[0] + total['data'][49]
    predict = predict_diff.cumsum()
    predict.columns = ['data']
    frame = [total,predict]
    zong = pd.concat(frame)

    #numpy.savetxt('AZ_WWTCB.csv', zong, delimiter=',')

    plt.figure(figsize=(30,10))
    plt.plot(zong.index,zong['data'])
    plt.ylabel('data')
    plt.title('summary')
    plt.show()

    #x.summary()
    #test_predict = predict_recover(test_predict, total, diffn)
    #test_predict.index = pd.Index(sm.tsa.datetools.dates_from_range('2010', '2050'))
    #print(test_predict)
    #print(model.predict(h=5, intervals=True))
    #model.plot_z(indices=range(1,9))
    #model.plot_fit(figsize=(15,5))
    #model.plot_fit()
    #model.plot_predict_is(5,figsize=(30,5))
    #model.plot_predict(h=5,figsize=(25,10))
    #model.plot_predict(h=5)
    #model.predict(h=20)
    #plt.show()


    #print(quanzhong)
    #numpy.savetxt('outfile.csv', guiyihua, delimiter=',')
    db.close()  # 关闭连接
