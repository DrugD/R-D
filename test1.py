# -*- coding: utf-8 -*-

from osgeo import gdal
import osr
import numpy as np
from matplotlib import pyplot as plt
from gdalconst import *
from matplotlib import cm
gdal.AllRegister()
filename = r"D:/Data/exerciseofweibo/datareday/data/data2/ers2dem.img"
data = gdal.Open(filename, GA_ReadOnly)
def convertToUTM(dataset, dx, utmZone):
    datum = 'WGS84'
    oldRef = osr.SpatialReference()  #初始化空间坐标

    # 从数据集中复制投影坐标系
    oldRef.ImportFromWkt(dataset.GetProjectionRef())
    newRef = osr.SpatialReference()
    print oldRef
    print newRef
    newRef.SetUTM(abs(utmZone), utmZone > 0)
    # 创建一个坐标转换对象
    transform = osr.CoordinateTransformation(oldRef, newRef)
    print transform
    tVect = dataset.GetGeoTransform()
    print tVect
    nx, ny = dataset.RasterXSize, dataset.RasterYSize
    #转换左上角坐标,x,y
    (ulx, uly, ulz ) = transform.TransformPoint(tVect[0], tVect[3])
    #转换左下角坐标
    (lrx, lry, lrz ) = transform.TransformPoint(tVect[0] + tVect[1]*nx+ny*tVect[2],
                                              tVect[3] + tVect[5]*ny+nx*tVect[4])
    #分别是左上角x，每个像素宽，旋转，分别是左上角y,旋转，像素高
    newtVect = (ulx, dx, tVect[2], uly, tVect[4], -dx)
    print newtVect
    return newtVect
nx, ny = data.RasterXSize, data.RasterYSize
dx = 10 #格网间隔
utmZone = 10  #南半球为负,utm 带号=（经度整数位/6）的整数部分+31（东经为正值，西经为负值）

gridNew = data.ReadAsArray().astype(np.float)#所有点高程
(upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size) = convertToUTM(data, dx, utmZone)
xllcenter = upper_left_x + dx/2  # 左下角像素中心x坐标（utm)
yllcenter = upper_left_y - (ny-1)*dx - dx/2 # 左下角像素中心y坐标
###yllcenter 之所以是<- (ny-1)*dx - dx/2>,是此时坐标系为笛卡尔，
##东西为x,南北朝上为y,左上角坐标减去(ny-1)*dx可得左下角像素坐标，再减去0.5个格网，就得到左下角像素的中心坐标
#每个像素的坐标
xcoordinates = [x*dx + xllcenter for x in range(nx)]
ycoordinates = [y*dx + yllcenter for y in range(ny)]

#创建2d格网描述x,y
X,Y = np.meshgrid(xcoordinates, ycoordinates)

plt.figure()
plt.contourf(X, Y, gridNew, levels=np.linspace(np.amin(gridNew[gridNew > 0]),
                   np.amax(gridNew), 50),cmap=cm.gist_earth)
plt.show()
data=None
