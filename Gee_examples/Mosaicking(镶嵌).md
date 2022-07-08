您可以使用masking和imageCollection.mosaic()来实现各种不同的地图效果。mosaic()方法根据各层在输入集合中的顺序在输出图像中呈现。下面的例子使用mosaic()来组合蒙版NDWI和假颜色组合，并获得新的可视化结果:

```python
# Mosaic the visualization layers and display (or export).
mosaic = ee.ImageCollection([image_rgb, ndwi_rgb]).mosaic()

# Define a map centered on San Francisco Bay.
map_mosaic = folium.Map(location=[37.5010, -122.1899], zoom_start=10)

# Add the image layer to the map and display it.
map_mosaic.add_ee_layer(mosaic, None, 'mosaic')
display(map_mosaic)
```

在本例中，可以看到ImageCollection构造函数提供了两个可视化图像的列表。列表的顺序决定了图像在地图上呈现的顺序。

![image-20210802172808576](C:\Users\树风\AppData\Roaming\Typora\typora-user-images\image-20210802172808576.png)

陆地卫星8假彩色合成和NDWI的镶嵌图。美国旧金山湾区。