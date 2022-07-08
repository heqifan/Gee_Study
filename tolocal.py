import ee
import os
import numpy as np
import pandas as pd
import rasterio
from glob import glob
from rasterio.merge import merge
import shutil
import geemap
import math
import concurrent.futures

def export_image(region: ee.Geometry, image: ee.Image, outfile: str, scale: int,
                   crs='epsg:4326', sep=0.25, file_per_band=False, num_workers=None):
    """
    Args:
        geo: ee.Geometry, 需要下载的区域矢量几何
        image: ee.Image, 需要下载的影像
        outfile: str, 输出文件路径和名称，不需要文件后缀，下载的影响默认后缀为tif
        scale: int, 下载时的像元大小
        crs: str, 下载影像的投影，默认为 'epsg:4326' wgs1984投影
        sep: float, 影像裁剪大小(单位：经纬度)，默认为0.25
        file_per_band：bool，是否分波段下载
        num_workers: int 为同时下载个数,默认为CUP数量加1
    Returns: None
    """
    import os
    import numpy as np
    import rasterio
    from glob import glob
    from rasterio.merge import merge
    import shutil
    import geemap
    import math
    
    class Mayerror(Exception):   # 自定义报错
        pass
        

    if not os.path.exists(outfile + ".tif"):
        bounds = region.bounds()
        bands = image.bandNames().size().getInfo()
        poy = np.array(bounds.coordinates().getInfo()[0])
        min_x = poy[:, 0].min()
        max_x = poy[:, 0].max()
        min_y = poy[:, 1].min()
        max_y = poy[:, 1].max()
        step = scale / 10 * sep / (int(math.sqrt(bands))+1)
        end_x = int((max_x - min_x) / step) + 1
        end_y = int((max_y - min_y) / step) + 1
        polys = []
        for i in range(end_y):
            y1 = min_y + step * i
            y2 = min_y + step * (i + 1)
            if y2 > max_y:
                y2 = max_y
            for j in range(end_x):
                x1 = min_x + step * j
                x2 = min_x + step * (j + 1)
                if x2 > max_x:
                    x2 = max_x
                poly = ee.Geometry(ee.Geometry.Rectangle([float(x1), float(y1), float(x2), float(y2)]), None, False)
                polys.append(poly)
        if len(polys) > 1:
            print(f"分割成{len(polys)}份, 开始下载:")
            path = outfile+'_mk'
            if not os.path.exists(path):
                os.makedirs(path)
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                for j, i in enumerate(polys):
                    if not os.path.exists(path+f'/temp_{j}.tif'):
                          executor.submit(geemap.ee_export_image, image, path + f'/temp_{j}.tif',
                                          scale=scale, crs=crs, region=i, file_per_band=file_per_band)
                    else:
                        continue
            if file_per_band:
                bands = image.bandNames().getInfo()
                for band in bands:
                    files = glob(path+"/*"+band+".tif")
                    try:
                        if len(files) < len(polys):
                            raise Mayerror('下载不完全！！！')
                        src_files_to_mosaic = []
                        for tif_f in files:
                            src = rasterio.open(tif_f)
                            src_files_to_mosaic.append(src)
                        mosaic, out_trans = merge(src_files_to_mosaic)
                        out_meta = src.meta.copy()
                        out_meta.update({"driver": "GTiff",
                                         "height": mosaic.shape[1],
                                         "width": mosaic.shape[2],
                                         "transform": out_trans,
                                         })
                        with rasterio.open(outfile+"_"+band+".tif", "w", **out_meta) as dest:
                            dest.write(mosaic)
                        for src in src_files_to_mosaic:
                            src.close()
                    except Mayerror as e:
                        print(e)
                        return export_image(region, image, outfile, scale, crs, sep, file_per_band, num_workers)
            else:
                files = glob(path+"/*.tif")
                try:
                    if len(files) < len(polys):
                        raise Mayerror('下载不完全！！！')
                    src_files_to_mosaic = []
                    for tif_f in files:
                        src = rasterio.open(tif_f)
                        src_files_to_mosaic.append(src)
                    mosaic, out_trans = merge(src_files_to_mosaic)
                    out_meta = src.meta.copy()
                    out_meta.update({"driver": "GTiff",
                                     "height": mosaic.shape[1],
                                     "width": mosaic.shape[2],
                                     "transform": out_trans,
                                     })
                    with rasterio.open(outfile+".tif", "w", **out_meta) as dest:
                        dest.write(mosaic)
                    for src in src_files_to_mosaic:
                        src.close()
                except Mayerror as e:
                    print(e)
                    return export_image(region, image, outfile, scale, crs, sep, file_per_band, num_workers)
            shutil.rmtree(path)
        else:
            geemap.ee_export_image(image, outfile+'.tif', scale=scale, crs=crs, region=region, file_per_band=file_per_band)
        print(outfile + ".tif"+" download successful !!!")
    else:
        print(outfile + ".tif"+" already download !!!")
    

def export_collection(region: ee.Geometry, images: ee.Image, outfile: str, scale: int,
                       crs='epsg:4326', sep=0.25, file_per_band=False, num_workers=None):
    """
    Args:
        geo: ee.Geometry, 需要下载的区域矢量几何
        images: ee.Image, 需要下载的影像集
        outfile: str, 输出文件路径
        scale: int, 下载时的像元大小
        crs: str, 下载影像的投影，默认为 'epsg:4326' wgs1984投影
        sep: float, 影像裁剪大小(单位：经纬度)，默认为0.25
        file_per_band：bool，是否分波段下载
        num_workers: int 为同时下载个数,默认为CUP数量加1
    Returns: None
    """
    count = int(images.size().getInfo())
    print(f"Total number of images: {count}\n")
    out_dir = outfile+os.sep+"ImageCollection_mk"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for i in range(0, count):
        image = ee.Image(images.toList(count).get(i))
        name = image.get("system:index").getInfo()
        filename = os.path.join(os.path.abspath(out_dir), name)
        print(f"Exporting {i + 1}/{count}: {name}")
        export_image(region=region, image=image, outfile=filename, scale=scale,
                       crs='epsg:4326', sep=0.25, file_per_band=file_per_band, num_workers=None)
    print("正在合并!!!")
    tifs = pd.Series(glob(out_dir+os.sep+"*.tif"))
    dates = tifs.str.split("\\").str[-1].str[:8].unique()
    if file_per_band:
        bands = image.bandNames().getInfo()
        for band in bands:
            fileband = tifs[tifs.str.contains(band)]
            for date in dates:
                dfs = fileband[fileband.str.contains(date)]
                src_files_to_mosaic = []
                for tif_f in dfs:
                    src = rasterio.open(tif_f)
                    src_files_to_mosaic.append(src)
                mosaic, out_trans = merge(src_files_to_mosaic)
                out_meta = src.meta.copy()
                out_meta.update({"driver": "GTiff",
                                 "height": mosaic.shape[1],
                                 "width": mosaic.shape[2],
                                 "transform": out_trans,
                                 })
                with rasterio.open(outfile+os.sep+date+"_"+band+".tif", "w", **out_meta) as dest:
                    dest.write(mosaic)
                for src in src_files_to_mosaic:
                    src.close()
    else:
        for date in dates:
            dfs = fileband[fileband.str.contains(date)]
            src_files_to_mosaic = []
            for tif_f in dfs:
                src = rasterio.open(tif_f)
                src_files_to_mosaic.append(src)
            mosaic, out_trans = merge(src_files_to_mosaic)
            out_meta = src.meta.copy()
            out_meta.update({"driver": "GTiff",
                             "height": mosaic.shape[1],
                             "width": mosaic.shape[2],
                             "transform": out_trans,
                             })
            with rasterio.open(outfile+os.sep+date+".tif", "w", **out_meta) as dest:
                dest.write(mosaic)
            for src in src_files_to_mosaic:
                src.close()
    shutil.rmtree(out_dir)
    print("下载完成！！！")