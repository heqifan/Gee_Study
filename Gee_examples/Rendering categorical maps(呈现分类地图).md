调色板对于呈现离散的有价值地图也很有用，例如土地覆盖地图。在有多个类的情况下，使用调色板为每个类提供不同的颜色。(image.remap()方法在这种上下文中可能很有用，可以将任意标签转换为连续整数)。下面的例子使用调色板来渲染土地覆盖类别:

```python
# Load 2012 MODIS land cover and select the IGBP classification.
cover = ee.Image('MODIS/051/MCD12Q1/2012_01_01').select('Land_Cover_Type_1')

# Define a palette for the 18 distinct land cover classes.
igbp_palette = [
    'aec3d4',  # water
    '152106',
    '225129',
    '369b47',
    '30eb5b',
    '387242',  # forest
    '6a2325',
    'c3aa69',
    'b76031',
    'd9903d',
    '91af40',  # shrub, grass
    '111149',  # wetlands
    'cdb33b',  # croplands
    'cc0013',  # urban
    '33280d',  # crop mosaic
    'd7cdcc',  # snow and ice
    'f7e084',  # barren
    '6f6f6f'   # tundra
]

# Define a map centered on the United States.
map_palette = folium.Map(location=[40.413, -99.229], zoom_start=5)

# Add the image layer to the map and display it. Specify the min and max labels
# and the color palette matching the labels.
map_palette.add_ee_layer(
    cover, {'min': 0, 'max': 17, 'palette': igbp_palette}, 'IGBP classes')
display(map_palette)
```

![image-20210802173142700](C:\Users\树风\AppData\Roaming\Typora\typora-user-images\image-20210802173142700.png)

基于IGBP的MODIS 2012土地覆盖分类。

