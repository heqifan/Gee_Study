具体请参考[landsat8的NDVI指数计算](https://zhuanlan.zhihu.com/p/29620366)

```javascript
NDVI = (近红外波段 - 红波段) / (近红外波段 + 红波段)

Landsat8: NDVI = (band5 - band4) / (band5 + band4)
Sentinel2: NDVI = (band8 - band4) / (band8 + band4)
Modis: NDVI = (band2 - band1) / (band2 + band1)
ETM/TM: NDVI = (band4 - band3) / (band4 + band3)
AVHRR: NDVI = (CH2 - CH1) / (CH2 + CH1)
...
```

```javascript
//landsat 8 NDVI Demo

//方法一：普通方式，通过将数学公式翻译为代码直接计算
function NDVI_V1(img) {
 var nir = img.select("B5");
 var red = img.select("B4");
 var ndvi = nir.subtract(red).divide(nir.add(red));
 return ndvi;
}

//方法二：将计算公式直接带入，通过解析字符串实现计算。这种方式更加灵活，在某些特殊情况下非常好用，而且非常直观。
function NDVI_V2(img) {
 var nir = img.select("B5");
 var red = img.select("B4");
 var ndvi = img.expression(
   "(B5 - B4)/(B5 + B4)",
   {
     "B5": nir,
     "B4": red
   }
 );
 return ndvi;
}


//方法三：GEE将计算公式封装为一个方法可以直接调用
function NDVI_V3(img) {
 var ndvi = img.normalizedDifference(["B5","B4"]);
 return ndvi;
}


//landsat8 and roi 我们这里使用的2017年全部的Landsat8影像，地点是沧州附近 
var l8_col = ee.ImageCollection("LANDSAT/LC08/C01/T1_RT_TOA");
var roi = ee.Geometry.Point([117.0703125,38.09133660751176]);
var img = ee.Image(l8_col.filterBounds(roi)
                       .filterDate("2017-01-01", "2017-09-24")
                       .first());
var ndvi1 = NDVI_V1(img);
var ndvi2 = NDVI_V2(img);
var ndvi3 = NDVI_V3(img);
//NDVI显示配置，NDVI值范围是-1到1
var visParam = {
 min: -0.2,
 max: 0.8,
 palette: 'FFFFFF, CE7E45, DF923D, F1B555, FCD163, 99B718, 74A901, 66A000, 529400,' +
   '3E8601, 207401, 056201, 004C00, 023B01, 012E01, 011D01, 011301'
};
//原始影像真彩色
Map.addLayer(img, {bands:["B4", "B3", "B2"], max:0.3}, "raw_img");
Map.addLayer(ndvi1, visParam, "ndvi_1");
Map.addLayer(ndvi2, visParam, "ndvi_2");
Map.addLayer(ndvi3, visParam, "ndvi_3");
Map.centerObject(roi, 9);

//上面只是展示了图像，我们在分析的时候还需要查看我们所筛选的影像NDVI值
var ndvi_list = l8_col.filterDate("2017-01-01", "2017-09-24")
   .map(function(image) {
   //通过云筛选landsat8
   var cloud = ee.Algorithms.Landsat.simpleCloudScore(image).select("cloud");
   var mask = cloud.lte(20);
   var ndvi = image.normalizedDifference(['B5', 'B4']).rename('NDVI');
   return image.addBands(ndvi).updateMask(mask);
});


//展示每一张影像NDVI值 
var chart1 = ui.Chart.image.series({
 //影像集合
 imageCollection: ndvi_list.select('NDVI'),
 //关心区域
 region: roi,
 //关心区域计算方式，这里采用的是均值。也就是比如roi是一个矩形，
 //那么在图表中这个点的值就是矩形内所有像素值求平均。
 reducer: ee.Reducer.mean(),
 //分辨率
 scale: 30
}).setOptions({title: 'NDVI IMAGE SERIES'});
print(chart1);


//展示每一天所关心区域的NDVI值
var chart2 = ui.Chart.image.doySeries({
 imageCollection: ndvi_list.select('NDVI'),
 region:roi,
 regionReducer: ee.Reducer.mean(),
 scale:30
}).setOptions({title: "ROI NDVI EACH DAY SERIES"})
print(chart2)
```

