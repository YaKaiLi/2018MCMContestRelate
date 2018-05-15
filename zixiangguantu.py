import pymysql  # 导入 pymysql
import numpy
import pandas as pd
import pyflux as pf
#from datetime import datetime
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_pacf,plot_acf

if __name__ == '__main__':

    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root",password="root", db="mcm", port=3306)

    # 使用cursor()方法获取操作游标
    #cur = db.cursor(cursor=pymysql.cursors.DictCursor)
    cur = db.cursor()

    # 1.查询操作
    # 编写sql 查询语句  user 对应我的表名
    sql = "select * from `sesedsneed_copy` WHERE `MSN` = 'WWTCB' AND `statecode` = 'TX' ORDER BY `year`"
    cur.execute(sql)  # 执行sql语句

    results = cur.fetchall()  # 获取查询的所有记录
    resnp = numpy.array(results)
    total = pd.DataFrame(resnp,columns=['msn','statecode','year','data'])
    total.index = total['year'].values
    ts = total['data']
    print(resnp)
    plot_acf(ts)
    plt.show()
    '''
    plt.figure(figsize=(30,5))
    plt.plot(total.index,total['data'])
    plt.ylabel('data')
    plt.title('summary')
    plt.show()
    '''
    db.close()  # 关闭连接
