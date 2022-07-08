```python
import geemap
import ee
Map = geemap.Map()
Map
```



```python
roi = ee.FeatureCollection("users/yehuigeo/poyanghu")   #导入鄱阳湖矢量文件，这里可以直接导入使用
dem = ee.Image("USGS/SRTMGL1_003")        #导入哨兵影像
#这里用的是哨兵二号的影像，一些去云以及水体指数代表的波段与lansat5，7，8都有所不一样，都需要修改
Map.addLayer(dem,{},'dem',False)     #添加到图层进行查看
Map.addLayer(roi,{},'roi')

```

```python
#定义去云函数
def maskS2clouds(image):     
    qa = image.select('QA60')  #这里我要用‘QA60’这个波段所以这样写
  #第10位和第11位分别是云和卷云。  
    cloudBitMask = 1 << 10
    cirrusBitMask = 1 << 11 
  # 这两个标志都应该设置为零，表示明确的条件。  
    mask = qa.bitwiseAnd(cloudBitMask).eq(0) .And(qa.bitwiseAnd(cirrusBitMask).eq(0))
    return image.updateMask(mask)

#定义哨兵二号的NDVI指数的函数
def ND_VI(image,b1,b2,bName):  
    VI = image.normalizedDifference([b1,b2]).rename(bName)
    return VI.updateMask(VI.gt(-1).And(VI.lt(1)))
#这里对大于-1小于1的像元进行掩膜

#定义计算哨兵二号的EVI指数的函数
def funEVI(image,a,b,c):         
    VI = image.expression(             
        '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
      'BLUE': image.select(a),   
      'RED': image.select(b),   
      'NIR': image.select(c)}).rename('EVI')
    return VI.updateMask(VI.gt(-1).And(VI.lt(1)))
#定义添加波段的函数
def addLandsatVIs(img):
    NDVI = ND_VI(img,'B8','B4','NDVI')
    EVI = funEVI(img,'B2','B4','B8')
    mNDWI = ND_VI(img,'B3','B6','mNDWI')
    return img.addBands(NDVI).addBands(EVI).addBands(mNDWI)

#定义水像元的函数
def Water(img):           # 水提取 MNDWI > NDVI或MNDWI > EVI 和 EVI < 0.1
    return    img.select('mNDWI').gt(img.select('EVI')).Or(img.select('mNDWI').gt(img.select('NDVI'))) .And(img.select('EVI').lt(0.1))
```

```python
for year in range(2020,2021):  
    START_DATE  = str(year) + '-06'
    END_DATE = str(year) + '-09'
    collection = ee.ImageCollection('COPERNICUS/S2') .filterBounds(roi)     .filterDate(START_DATE,END_DATE ).map(maskS2clouds).select(['B1', 'B2', 'B3', 'B4', 'B5','B6','B7','B8','QA60'])  .map(addLandsatVIs)    
    #添加需要的波段
    total_Pos = collection.map(Water).filterBounds(roi)        #计算水像元
    
    clipped_image = total_Pos.mode().clip(roi)   #计算imagecollection中的众数
    geemap.ee_export_image_to_drive(clipped_image,       #导出
                            folder = 'Water',
                           description = "mode2",
                            region=roi.geometry(),
                            scale = 30,
                           crs = 'EPSG:4527'
                          )
    clipped_image = total_Pos.max().clip(roi)
    geemap.ee_export_image_to_drive(clipped_image,       #导出
                            folder = 'Water',
                           description = "max2",
                            region=roi.geometry(),
                            scale = 30,
                           crs = 'EPSG:4527'
                          )
```

