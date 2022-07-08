```python
csv_points_to_shp(in_csv, out_shp, latitude='latitude', longitude='longitude')`
#latitude ：纬度
#longitude ：经度

```





```python
csv_to_ee(in_csv, latitude='latitude', longitude='longitude', encoding='utf-8', geodesic=True)
#为CSV文件创建点，并将数据导出为GeoJSON。
#geodesic = 线段是否应解释为球面测地线。如果为假，表示线段应被解释为指定CRS中的平面线。如果不存在，如果CRS是地理上的(包括默认的EPSG:4326)默认为true，如果CRS是投射的，默认为false。
```



```python
csv_to_geojson(in_csv, out_geojson=None, latitude='latitude', longitude='longitude', encoding='utf-8') 
#为CSV文件创建点，并将数据导出为GeoJSON
```



```python
csv_to_geopandas(in_csv, latitude='latitude', longitude='longitude', encoding='utf-8') 
#为CSV文件创建点，并将它们转换为GeoDataFrame。
```

