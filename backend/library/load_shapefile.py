from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import Province

world_mapping = {
    'objectid': 'OBJECTID',
    'area': 'AREA',
    'perimeter': 'PERIMETER',
    'pzanj_field': 'PZANJ_',
    'pzanj_id': 'PZANJ_ID',
    'sourcethm': 'SOURCETHM',
    'acres': 'ACRES',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'ostn_name': 'ostn_name',
    'code': 'code',
    'areaasss': 'AREAASSS',
    'areaaqqqqq': 'areaaqqqqq',
    'per': 'per',
    'codeddd': 'CODEDDD',
    'ara': 'ara',
    'geom': 'MULTIPOLYGON',

}

province_shape = "/home/Province/province.shp"


def run(verbose=True):
    lm = LayerMapping(Province, province_shape, world_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)