具体请参考[landsat8的NDWI指数计算](https://zhuanlan.zhihu.com/p/29672090)

```javascript

NDWI = (绿波段 - 近红外波段) / (绿波段 + 近红外波段)

landsat8: NDWI = (band3 - band5) / (band3 + band5)
landsat5/7: NDWI = (band2 - band4) / (band2 + band4)
sentinel2: NDWI = (band3 - band8) / (band3 + band8)
```

```javascript
/landsat 8 NDWI Demo
function NDWI_V1(img) {
 var nir = img.select("B5");
 var green = img.select("B3");
 var ndwi = green.subtract(nir).divide(green.add(nir));
 return ndwi;
}

function NDWI_V2(img) {
 var nir = img.select("B5");
 var green = img.select("B3");
 var ndwi = img.expression(
   "(B3 - B5)/(B3 + B5)",
   {
     "B5": nir,
     "B3": green
   }
 );
 return ndwi;
}


function NDWI_V3(img) {
 var ndwi = img.normalizedDifference(["B3","B5"]);
 return ndwi;
}


//landsat8 and roi
var l8_col = ee.ImageCollection("LANDSAT/LC8_L1T_TOA");
var roi = ee.Geometry.Point([124.1455078125,45.644768217751924]);
var img = ee.Image(l8_col.filterBounds(roi)
                       .filterDate("2017-02-01", "2017-09-23")
                       .first());
var ndwi1 = NDWI_V1(img);
var ndwi2 = NDWI_V2(img);
var ndwi3 = NDWI_V3(img);
var visParam = {
 min: -0.5,
 max: 0.5,
 palette: ['00FFFF', '0000FF']
};
Map.addLayer(img, {bands:["B4", "B3", "B2"], max:0.3}, "raw_img");
Map.addLayer(ndwi1, visParam, "ndwi_1");
Map.addLayer(ndwi2, visParam, "ndwi_2");
Map.addLayer(ndwi3, visParam, "ndwi_3");
Map.centerObject(roi, 9);

//show charts
var ndwi_list = l8_col.filterDate("2017-01-01", "2017-09-23")
   .map(function(image) {
   var cloud = ee.Algorithms.Landsat.simpleCloudScore(image).select("cloud");
   var mask = cloud.lte(20);
   var ndwi = image.normalizedDifference(['B3', 'B5']).rename('NDWI');
   return image.addBands(ndwi).updateMask(mask);
});
var chart1 = ui.Chart.image.series({
 imageCollection: ndwi_list.select('NDWI'),
 region: roi,
 reducer: ee.Reducer.mean(),
 scale: 30
}).setOptions({title: 'NDWI IMAGE SERIES'});
print(chart1);


var chart2 = ui.Chart.image.doySeries({
 imageCollection: ndwi_list.select('NDWI'),
 region:roi,
 regionReducer: ee.Reducer.mean(),
 scale:30
}).setOptions({title: "ROI NDWI EACH DAY SERIES"})
print(chart2)
```

