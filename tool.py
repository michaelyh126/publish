import arcpy
from arcpy import env

import publish
import create_service

def remove_uni(s):
    """remove the leading unicode designator from a string"""
    s2 = ''
    if s.startswith("u'"):
        s2 = s.replace("u'", "'", 1)
    elif s.startswith('u"'):
        s2 = s.replace('u"', '"', 1)
    return s2

def test():
    path='D:/GIS/chongmin.mxd'
    # con=create_service.GetAGSConnectionFile(path)
    create_service.PublishMxd(path)

# pip install flask -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
# pyinstaller -F xxx.py
# C:/Users/root/Documents/ArcGIS/D.mxd

if __name__ == '__main__':
    # sddraft='ex486ce3680-6c9d-11ed-ad37-f0e441246c37.sddraft'
    # sd='D:/chongmin5b04799e-6c8a-11ed-9e36-6c6a773bbaf9.sd'
    # con='D:/GIS/ex4.ags'
    # analysis = arcpy.mapping.AnalyzeForSD(sddraft)
    # arcpy.StageService_server(sddraft, sd)
    # arcpy.UploadServiceDefinition_server(sd, con)

    mxd = arcpy.mapping.MapDocument(r"D:/GIS/p.mxd")



    # test()