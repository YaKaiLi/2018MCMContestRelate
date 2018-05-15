import pymysql  # 导入 pymysql
import numpy
import pandas as pd
from statsmodels.tsa.stattools import acf, pacf
import matplotlib.pyplot as plt
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
    #total = pd.DataFrame(resnp,columns=['data'])
    #total.index = total['year'].values
    #total = pd.Series(results)  # 通过元组创建series
    #total.index = pd.Index(sm.tsa.datetools.dates_from_range('1960', '2009'))
    #total['diff'] = None
    lag_acf = acf(total, nlags=20)
    lag_pacf = pacf(total, nlags=20, method='ols')
    # Plot ACF:
    plt.subplot(121)
    plt.plot(lag_acf)
    plt.axhline(y=0, linestyle='--', color='gray')
    plt.axhline(y=-1.96 / numpy.sqrt(len(total)), linestyle='--', color='gray')
    plt.axhline(y=1.96 / numpy.sqrt(len(total)), linestyle='--', color='gray')
    plt.title('Autocorrelation Function')

    # Plot PACF:
    plt.subplot(122)
    plt.plot(lag_pacf)
    plt.axhline(y=0, linestyle='--', color='gray')
    plt.axhline(y=-1.96 / numpy.sqrt(len(total)), linestyle='--', color='gray')
    plt.axhline(y=1.96 / numpy.sqrt(len(total)), linestyle='--', color='gray')
    plt.title('Partial Autocorrelation Function')
    plt.tight_layout()
    plt.show()
    #exit(0)
    #print(best_diff(total['data']))
    #print(total)

    '''
    plt.figure(figsize=(30,5))
    plt.plot(total.index,total['data'])
    plt.ylabel('data')
    plt.title('summary')
    plt.show()
'''
    db.close()  # 关闭连接
