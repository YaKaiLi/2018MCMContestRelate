import pymysql  # 导入 pymysql
import numpy
from sklearn import preprocessing
from sklearn.decomposition import PCA
# 打开数据库连接
db = pymysql.connect(host="localhost", user="root",password="root", db="mcm", port=3306)

# 使用cursor()方法获取操作游标  
#cur = db.cursor(cursor=pymysql.cursors.DictCursor)
cur = db.cursor()

# 1.查询操作
# 编写sql 查询语句  user 对应我的表名  
sql = "select * from chazhiqian"
cur.execute(sql)  # 执行sql语句

results = cur.fetchall()  # 获取查询的所有记录
total = numpy.array(results)
#total = list(results)
#print("id", "name", "password")
# 遍历结果

for row in total:
    for j in range(0,8):
        if row[j] == 'NULL':
            row[j]=numpy.nan
#删除id字段
shanchuid = numpy.delete(total, 0, axis=1)
shanchuid = numpy.delete(shanchuid, 0, axis=1)
shanchuid = numpy.delete(shanchuid, 0, axis=1)
#shanchuid = total


#进行插值
imp = preprocessing.Imputer(missing_values='NaN', strategy='mean', axis=0)
imp.fit(shanchuid)
chazhijieguo = imp.transform(shanchuid)

#数据标准化
biaozhunhua = preprocessing.scale(chazhijieguo)
#数据归一化
min_max_scale = preprocessing.MinMaxScaler()
guiyihua = min_max_scale.fit_transform(biaozhunhua)
#数据同趋化
for row in guiyihua:
    row[0] = 1-row[0]
    row[-1] = 1-row[-1]

#PCA主成分分析
pca = PCA()
pca.fit(guiyihua)
quanzhong = (pca.explained_variance_ratio_)
##得到权重后线性加权
jisuanquanzhong_in = numpy.ones(846)
guiyihua = numpy.c_[guiyihua,jisuanquanzhong_in]
for row in guiyihua:
    row[5] = row[0] * quanzhong[0]+ row[1] * quanzhong[1]+row[2] * quanzhong[2]+row[3] * quanzhong[3]+ row[4] * quanzhong[4]

#填充id
guiyihua = numpy.c_[guiyihua,jisuanquanzhong_in]
for i in range(0,846):
    guiyihua[i][6] = total[i][0]

#print(quanzhong)
numpy.savetxt('outfile.csv', guiyihua, delimiter=',')
db.close()  # 关闭连接