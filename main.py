# -*- coding: utf-8 -*

# dataset = gdal.Open("D:/Data/exerciseofweibo/datareday/data/data2/dat_01.img")
# print dataset.RasterXSize
# print dataset.RasterYSize

from osgeo import gdal
import numpy as np
import cv2
import matplotlib.pyplot as plt
import re
import rasterio
import os
import matplotlib.pyplot as plt
import numpy as np

# np.set_printoptions(threshold=np.inf)#使print大量数据不用符号...代替而显示所有
#
# dataset = gdal.Open("D:/Data/exerciseofweibo/datareday/data/data2/ers2dem.img")
#
# print(dataset.GetDescription())#数据描述
#
# print(dataset.RasterCount)#波段数
# #
# cols=dataset.RasterXSize#image length
# rows=(dataset.RasterYSize)#image width
# print cols ,rows
#
# xoffset=cols/2
# yoffset=rows/2
#
# band = dataset.GetRasterBand(1)#取第三波段
# r=band.ReadAsArray(xoffset,yoffset,1000,1000)#从数据的中心位置位置开始，取1000行1000列数据
#
# band = dataset.GetRasterBand(1)
# g=band.ReadAsArray(xoffset,yoffset,1000,1000)
#
# band = dataset.GetRasterBand(1)
# b=band.ReadAsArray(xoffset,yoffset,1000,1000)
#
#
#
#
# img2=cv2.merge([r,g,b])
# plt.imshow(img2)
# plt.xticks([]),plt.yticks([]) # 不显示坐标轴
# plt.show()

# f = open('D:/Data/exerciseofweibo/datareday/data/data2/ers2/DAT_01.001', 'r')
# print f
# f.close()


# print 360+360+360+360+720+1886
# +650+12288+12288+449+10012+360
# print 4046 + 387 + 30 + 60 + 70 + 19
# 291-306
# 307·322
# 323·338

# position
# 387-408
# 409-430
# 431-452

# velocity
# 453-474
# 475-496
# 497-518



# 创建数据[]

position=[[]]*5
velocity=[[]]*5
t1=0
delta_t=0
t0_azi=0
t0_range=0
delta_t_azi=0
delta_t_range=0
line=0
pixel=0
delta_r_azi=0
delta_r_range=0
a=0
b=0
B=[]
L=[]
#
# # 基础信息
# with rasterio.open('D:/Data/exerciseofweibo/datareday/data/data2/ers2dem.img') as ds:
#     # print(ds.read())
#     print'该栅格数据的基本数据集信息（这些信息都是以数据集属性的形式表示的）：'
#     print'数据格式：',ds.driver
#     print'波段数目：',ds.count
#     print'影像宽度：',ds.width
#     line=ds.width
#     print'影像高度：',ds.height
#     pixel=ds.height
#     print'地理范围：',ds.bounds
#     # print'反射变换参数（六参数模型）：\n ',ds.transform
#     print'投影定义：',ds.crs
#     # 获取第一个波段数据，跟GDAL一样索引从1开始
#     # 直接获得numpy.ndarray类型的二维数组表示，如果read()函数不加参数，则得到所有波段（第一个维度是波段）
#     band1 = ds.read(1)
#     # band2 = ds.read(2)
#     print'第一波段的最大值：',band1.max()
#     print'第一波段的最小值：',band1.min()
#     print'第一波段的平均值：',band1.mean()
#     # 根据地理坐标得到行列号
#     # x, y = (ds.bounds.left + 300, ds.bounds.top - 300)  # 距离左上角东300米，南300米的投影坐标
#     # row, col = ds.index(x, y)  # 对应的行列号
#     # print'(投影坐标',x, y,')对应的行列号是(',row, col,')'
#     # # 根据行列号得到地理坐标
#     # x, y = ds.xy(row, col)  # 中心点的坐标
#     # print'行列号(',row, col,')对应的中心投影坐标是(',x, y,')'
#     # # 那么如何得到对应点左上角的信息
#     # x, y = (row, col) * ds.transform
#     # print'行列号(',row, col,')对应的左上角投影坐标是(',x, y,')'
#     # # band = ds.GetRasterBand(1)
#     # # b=band.ReadAsArray(1,1,1000,1000)
#     plt.imshow(band1)
#     plt.show()
#     # plt.imshow(band2)
#     # plt.show()


# 读取轨道参数
with open('D:/Data/exerciseofweibo/datareday/data/data2/ers2/LEA_01/LEA_01', 'r') as f:
    for i in range(30):
        f.seek(4612+i*22, 0)
        # 4612是根据pdf中的参数描述的位置算出来的
        pos = f.tell()
        text_to_number = f.read(22)
        if (i+1)%6==1:
            # print 'positionX:',text_to_number
            position[0].append(text_to_number)
        if (i+1)%6==2:
            # print 'positionY:',text_to_number
            position[1].append(text_to_number)
        if (i+1)%6==3:
            # print 'positionZ:',text_to_number
            position[2].append(text_to_number)
        if (i+1)%6==4:
            # print 'velocityX:',text_to_number
            velocity[0].append(text_to_number)
        if (i+1)%6==5:
            # print 'velocityX:',text_to_number
            velocity[1].append(text_to_number)
        if (i+1)%6==0:
            # print 'velocityX:',text_to_number
            velocity[2].append(text_to_number)
    print '轨道数据读取...(5个时刻坐标与速度)'

# print velocity
# print position
#
# with open('D:/Data/exerciseofweibo/datareday/data/data2/ers2/LEA_01/LEA_01', 'r') as f:
#     temp=0
#     for i in range(4*2):
#         f.seek(3684+temp, 0)
#         # 4612是根据pdf中的参数描述的位置算出来的
#         pos = f.tell()
#         text_to_number = f.read(10)
#         # print text_to_number
#         if i%2==0:
#             temp = temp+15
#             B.append(text_to_number)
#         else:
#             temp= temp +17
#             L.append(text_to_number)
#     print '轨道数据读取...(SAR图像四个角点经纬度)'
#
# # print B
# # print L
#
# with open('D:/Data/exerciseofweibo/datareday/data/data2/ers2/LEA_01/LEA_01', 'r') as f:
#     f.seek(4387, 0)
#     # 4612是根据pdf中的参数描述的位置算出来的
#     pos = f.tell()
#     text_to_number = f.read(22)
#     # print '轨道点第一个点记录时间:\n',text_to_number
#     t1=text_to_number
#     f.seek(4409, 0)
#     # 4612是根据pdf中的参数描述的位置算出来的
#     pos = f.tell()
#     text_to_number = f.read(21)
#     # print '轨道点间时间间隔：\n',text_to_number
#     delta_t=text_to_number
#     print '轨道数据读取...(轨道点记录时间)'
#
#
# with open('D:/Data/exerciseofweibo/datareday/data/data2/ers2/LEA_01/LEA_01', 'r') as f:
#     f.seek(2878, 0)
#     # 4612是根据pdf中的参数描述的位置算出来的
#     pos = f.tell()
#     text_to_number = f.read(15)
#     # print text_to_number
#     a=text_to_number
#     f.seek(2878+16, 0)
#     # 4612是根据pdf中的参数描述的位置算出来的
#     pos = f.tell()
#     text_to_number = f.read(15)
#     # print text_to_number
#     b=text_to_number
#     print '轨道数据读取...(参考椭球长半轴、短半轴)'
#
#
# delta_r_azi=3.9840000
# delta_t_range=7.9040000


# 11728.060
# 第一行成像时间，单位为秒；
# 1679.9020000
# 脉冲排斥频率'（prf）~aculal“值）
# Pulse Repelition Frequent}' (PRF) ~aclual "alue)
# 方位向（行）采样重复频率；单位HZ；
# 5.5365520
# 第一距离像素的零多普勒测距时间（2瓦\'）
# Zero-doppler range time (two-wa\') of first range pixel
# MHz
# 距离向（列）采样频率，单位MHZ；
# 18.9624680
# 范围采样率
# Range sampling rale
# millisecond
# 第一列距离向时间，单位毫秒


#这4个数据不太清楚意义与应用--待议
t0_azi=11727.669
t0_range=11728.060
delta_t_azi=5.5365520
# 距离向（列）采样频率，单位MHZ；
delta_t_range=18.9624680
# 第一列距离向时间，单位毫秒



# 多项式拟合
print position
print velocity


# 时间
x=[1.172766900000000e+04,1.172766900000000e+04+4.167000000000000e+00,1.172766900000000e+04+4.167000000000000e+00*2,1.172766900000000e+04+4.167000000000000e+00*3,1.172766900000000e+04+4.167000000000000e+00*4]

y1=np.reshape(position,(5,15))
y=np.reshape(y1[0],(5,3))

# 格式转化
x=np.array(x)
y=np.array(y)
y=y.astype(np.float64)


y1=[]
y2=[]
y3=[]

# p=np.zeros((3,3))
for i in range(5):
    y1.append(y[i][0])
    y2.append(y[i][1])
    y3.append(y[i][2])

print y1
print y2
print y3

# 多项式拟合
p1=np.poly1d(np.polyfit(x,y1,3))
p2=np.poly1d(np.polyfit(x,y2,3))
p3=np.poly1d(np.polyfit(x,y3,3))

# 得到多项式系数
#输出拟合的系数，顺序从高阶低阶
print p1.coeffs
print p2.coeffs
print p3.coeffs
print '输出拟合的系数，顺序从高阶低阶...'


# 获取任一时刻卫星轨道矢量
temp_t=1.172766900000000e+04+4.167000000000000e+00*2
temp_x = p1.coeffs[0]*temp_t*temp_t*temp_t+p1.coeffs[1]*temp_t*temp_t+p1.coeffs[2]*temp_t+p1.coeffs[3]
temp_y = p2.coeffs[0]*temp_t*temp_t*temp_t+p2.coeffs[1]*temp_t*temp_t+p2.coeffs[2]*temp_t+p2.coeffs[3]
temp_z = p3.coeffs[0]*temp_t*temp_t*temp_t+p3.coeffs[1]*temp_t*temp_t+p3.coeffs[2]*temp_t+p3.coeffs[3]
print temp_x
print temp_y
print temp_z

