下面举例说明如何使用参数将Landsat 8图像作为伪彩色合成:

```python
# Load an image.
image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')

# Define the visualization parameters.
image_viz_params = {
    'bands': ['B5', 'B4', 'B3'],
    'min': 0,
    'max': 0.5,
    'gamma': [0.95, 1.1, 1]
}

# Define a map centered on San Francisco Bay.
map_l8 = folium.Map(location=[37.5010, -122.1899], zoom_start=10)

# Add the image layer to the map and display it.
map_l8.add_ee_layer(image, image_viz_params, 'false color composite')
display(map_l8)
```

在这个例子中，'B5'被分配到红色，'B4'被分配到绿色，'B3'被分配到蓝色。

![image-20210802171910718](C:\Users\树风\AppData\Roaming\Typora\typora-user-images\image-20210802171910718.png)

美国加利福尼亚州旧金山湾区陆地卫星8号的假彩色合成图。

