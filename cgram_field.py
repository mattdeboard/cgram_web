import sys
from os import path
from osgeo import ogr
from random import randrange

def new_shpfile(shpfile):
    #In the future I will need to add an arg to this function to generate a new shapefile name vice a static one
    ds = ogr.Open(shpfile, 1)
    lyr = ds.GetLayerByName(shpfile.split('.')[0])
    driver = ogr.GetDriverByName('ESRI Shapefile')
    outfile = '%s_new.shp' % randrange(100000)
    driver.CopyDataSource(ds, outfile)
    newfile = ogr.Open(outfile, 1)
    new_lyr = newfile.GetLayerByIndex(0)
    return new_lyr, newfile
 
def cust_fielddefn(field):
    fieldDefn = ogr.FieldDefn(field, ogr.OFTInteger)
    fieldDefn.SetWidth(14)
    fieldDefn.SetPrecision(6)
    return fieldDefn

def write_custom_field(shpfile, cust_field_name):
    ''' This function writes the custom field definition to the layer of the shapefile. Format is write_custom_field(<shapefile name.ext>, <custom field name>).
    Example: write_custom_field('home/user/example.shp', 'foo')'''
    lyr, outfile = new_shpfile(shpfile)
    if cust_field_name not in (field.name for field in lyr.schema):
        output = cust_fielddefn(cust_field_name)
        lyr.CreateField(output)
        return outfile
    else:
        error = 'This field name (%s) already exists. Please choose another.' % cust_field_name
        return error


if __name__ == '__main__':
    try:
        write_custom_field(sys.argv[0:])
    except TypeError:
        print 'Syntax for this command is: python cgram_field.py <shapefilename> <custom_field_name>'
        shp = str(raw_input('Enter the shapefile name, including extension: '))
        fld = str(raw_input('Enter the custom field name: '))
        write_custom_field(shp, fld)
