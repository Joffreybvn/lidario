
import lidario as lio
import rasterio
from rasterio.mask import mask
import numpy as np

# TODO:
# Translator return multiple data structure
# Object to retrieve only metadata
# Increase raster resolution

dtm = rasterio.open("/media/becode/Elements/wallonia-ml/lidar/TIF Wallonie 2013-2014/DSM/DSM_BRABANT_WALLON/RELIEF_WALLONIE_MNS_2013_2014.tif")


if __name__ == '__main__':

    shape = [{'type': 'Polygon', 'coordinates': [[(182545.32672299084, 162803.11793349683), (182540.70250971318, 162801.0220066402), (182539.92463073373, 162803.0260931747), (182537.93350985483, 162802.24429725204), (182534.55473017017, 162809.74636963103), (182541.08707224843, 162812.70320118777), (182545.32672299084, 162803.11793349683)]]}]
    mask_values = rasterio.mask.mask(dtm, shapes=shape, all_touched=True, crop=True)

    translator = lio.Translator("mask", "df", metadata=True)
    result = translator.translate(mask_values)

    print(result)
