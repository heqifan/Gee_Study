```python
# Create a circle by drawing a 20000 meter buffer around a point.
roi = ee.Geometry.Point([-122.4481, 37.7599]).buffer(20000)
mosaic_clipped = mosaic.clip(roi)

# Define a map centered on San Francisco.
map_mosaic_clipped = folium.Map(location=[37.7599, -122.4481], zoom_start=10)

# Add the image layer to the map and display it.
map_mosaic_clipped.add_ee_layer(mosaic_clipped, None, 'mosaic clipped')
display(map_mosaic_clipped)
```

在前面的示例中，请注意，坐标被提供给了Geometry构造函数，并且缓冲区长度被指定为20,000米。在“几何图形”页了解有关几何图形的更多信息。

![image-20210802172946463](C:\Users\树风\AppData\Roaming\Typora\typora-user-images\image-20210802172946463.png)

上图所示的嵌合体，夹在美国加州旧金山附近的一个缓冲区上。

