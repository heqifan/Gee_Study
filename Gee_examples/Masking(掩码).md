可以使用image. updatemask()根据掩码图像中像素非零的位置来设置各个像素的不透明度。在蒙版中等于0的像素将被排除在计算之外，并且显示时不透明度设置为0。下面的示例使用NDWI阈值来更新之前创建的NDWI层的掩码:

```python
# Mask the non-watery parts of the image, where NDWI < 0.4.
ndwi_masked = ndwi.updateMask(ndwi.gte(0.4))

# Define a map centered on San Francisco Bay.
map_ndwi_masked = folium.Map(location=[37.5010, -122.1899], zoom_start=10)

# Add the image layer to the map and display it.
map_ndwi_masked.add_ee_layer(ndwi_masked, ndwi_viz, 'NDWI masked')
display(map_ndwi_masked)
```





