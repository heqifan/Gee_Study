要以颜色显示图像的单个条带，请使用css样式的颜色字符串列表表示的颜色渐变设置调色板参数。下面的示例演示了如何使用从青色('00FFFF')到蓝色('0000FF')的颜色来渲染归一化差水指数(NDWI)图像:

```python
# Load an image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')

# Create an NDWI image, define visualization parameters and display.
ndwi = image.normalizedDifference(['B3', 'B5'])
ndwi_viz = {'min': 0.5, 'max': 1, 'palette': ['00FFFF', '0000FF']}

# Define a map centered on San Francisco Bay.
map_ndwi = folium.Map(location=[37.5010, -122.1899], zoom_start=10)

# Add the image layer to the map and display it.
map_ndwi.add_ee_layer(ndwi, ndwi_viz, 'NDWI')
display(map_ndwi)
```

在本例中，请注意，min和max参数指示了调色板应应用的像素值范围。中间值是线性拉伸的。

![image-20210802172100367](C:\Users\树风\AppData\Roaming\Typora\typora-user-images\image-20210802172100367.png)

Landsat 8 NDWI，美国旧金山湾区。青色是低值，蓝色是高值。
