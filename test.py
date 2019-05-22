# -*- coding: utf-8 -*
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import rasterio.features
import rasterio.warp
import cv2
from osgeo import gdal
import os


#
# class GRID:
#
#     #读图像文件
#     def read_img(self,filename):
#         dataset=gdal.Open(filename)       #打开文件
#
#         im_width = dataset.RasterXSize    #栅格矩阵的列数
#         im_height = dataset.RasterYSize   #栅格矩阵的行数
#
#         im_geotrans = dataset.GetGeoTransform()  #仿射矩阵
#         im_proj = dataset.GetProjection() #地图投影信息
#         im_data = dataset.ReadAsArray(0,0,im_width,im_height) #将数据写成数组，对应栅格矩阵
#
#         print '行列：',im_data
#         print '仿射矩阵：', im_geotrans
#         print '地图投影信息：', im_proj
#         del dataset
#         return im_proj,im_geotrans,im_data
#
#     #写文件，以写成tif为例
#     def write_img(self,filename,im_proj,im_geotrans,im_data):
#         #gdal数据类型包括
#         #gdal.GDT_Byte,
#         #gdal .GDT_UInt16, gdal.GDT_Int16, gdal.GDT_UInt32, gdal.GDT_Int32,
#         #gdal.GDT_Float32, gdal.GDT_Float64
#
#         #判断栅格数据的数据类型
#         if 'int8' in im_data.dtype.name:
#             datatype = gdal.GDT_Byte
#         elif 'int16' in im_data.dtype.name:
#             datatype = gdal.GDT_UInt16
#         else:
#             datatype = gdal.GDT_Float32
#
#         #判读数组维数
#         if len(im_data.shape) == 3:
#             im_bands, im_height, im_width = im_data.shape
#         else:
#             im_bands, (im_height, im_width) = 1,im_data.shape
#
#         #创建文件
#         driver = gdal.GetDriverByName("HFA")            #数据类型必须有，因为要计算需要多大内存空间
#         dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)
#
#         dataset.SetGeoTransform(im_geotrans)              #写入仿射变换参数
#         dataset.SetProjection(im_proj)                    #写入投影
#
#         if im_bands == 1:
#             dataset.GetRasterBand(1).WriteArray(im_data)  #写入数组数据
#         else:
#             for i in range(im_bands):
#                 dataset.GetRasterBand(i+1).WriteArray(im_data[i])
#
#         del dataset
#
# if __name__ == "__main__":
#     os.chdir(r'D:/Data/exerciseofweibo/datareday/data/data2/')                        #切换路径到待处理图像所在文件夹
#     run = GRID()
#     proj,geotrans,data = run.read_img('dat_01.img')        #读数据
#     print proj
#     print geotrans
#     print data
#     # print data.shape
#     run.write_img('2.img',proj,geotrans,data) #写数据
#


dataset = gdal.Open("D:/Data/exerciseofweibo/datareday/data/data2/ers2dem.img")

print(dataset.GetDescription())#数据描述

print(dataset.RasterCount)#波段数
#
cols=dataset.RasterXSize#image length
rows=(dataset.RasterYSize)#image width
print cols ,rows

xoffset=cols/2
yoffset=rows/2

band = dataset.GetRasterBand(1)#取第三波段
r=band.ReadAsArray(xoffset,yoffset,1000,1000)#从数据的中心位置位置开始，取1000行1000列数据

band = dataset.GetRasterBand(1)
g=band.ReadAsArray(xoffset,yoffset,1000,1000)

band = dataset.GetRasterBand(1)
b=band.ReadAsArray(xoffset,yoffset,1000,1000)




img2=cv2.merge([r,g,b])
plt.imshow(img2)
plt.xticks([]),plt.yticks([]) # 不显示坐标轴
plt.show()