import geopandas as gpd
import numpy as np
import os
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from shapely import geometry


def raster_to_utm(raster: object, utm: gpd.GeoDataFrame):

    raster_path, raster_filename = os.path.split(raster)
    raster_name, raster_ext = os.path.splitext(raster_filename)

    with rasterio.open(raster) as src:

        # Get the raster bounds centroid
        bounds = src.bounds
        vertices = [
            geometry.Point(bounds.left, bounds.bottom),
            geometry.Point(bounds.right, bounds.bottom),
            geometry.Point(bounds.right, bounds.top),
            geometry.Point(bounds.left, bounds.top),
            geometry.Point(bounds.left, bounds.bottom)
        ]

        poly = geometry.Polygon([[p.x, p.y] for p in vertices])

        gdf = gpd.GeoDataFrame(
            {
                "title": [raster_name],
                "geometry": poly.centroid
            }
        )
        gdf.crs = src.crs
        gdf.to_crs(epsg=4326)

        # Run spatial join and get correct UTM zone EPSG
        joined = utm.sjoin(gdf, how="inner", predicate='intersects')
        dst_crs = f"EPSG:{joined['EPSG'].values[0]}"

        # Reproject the raster
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds
        )

        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        outname = os.path.join(raster_path, raster_name + '_UTM' + raster_ext)

        with rasterio.open(outname, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, 1),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest
                )
    return outname

if __name__ == '__main__':
    pass
