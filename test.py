# -*- coding: utf-8 -*-
import os

import arcpy
from arcpy import env
import publish

def test():
    # -*- coding:UTF-8 -*-
    server_username = 'siteadmin'
    server_password = '123456'
    # env.workspace = "C:/Users/86139/Documents"
    wrkspc = "C:/Users/86139/Documents"


    connection_type = 'ADMINISTER_GIS_SERVICES'
    out_folder_path = "D:/GIS"
    out_name = 'ex4.ags'
    server_url = 'http://localhost:6080/arcgis/admin'
    use_arcgis_desktop_staging_folder = False
    staging_folder_path = out_folder_path
    arcpy.mapping.CreateGISServerConnectionFile(connection_type, out_folder_path, out_name, server_url,
                                                'ARCGIS_SERVER', use_arcgis_desktop_staging_folder,
                                                staging_folder_path, server_username, server_password,
                                                "SAVE_USERNAME")
    mxdname = wrkspc + '/ex4.mxd'
    mapDoc = arcpy.mapping.MapDocument(wrkspc + '/ex4.mxd')
    service_name = 'ex'
    sddraft = wrkspc + '/' + service_name + '.sddraft'
    sd = wrkspc + '/' + service_name + '.sd'
    summary = 'ex'
    tags = 'ex'
    con = out_folder_path + '/' + out_name
    analysis = arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, service_name, 'ARCGIS_SERVER', con, True, 'Test',
                                              summary, tags)
    if analysis['errors'] == {}:
        arcpy.StageService_server(sddraft, sd)
        arcpy.UploadServiceDefinition_server(sd, con)
    else:
        print analysis['errors']


if __name__ == '__main__':
    # mxd=publish.create_mxd('tif')
    # publish.rewrite_mxd_tif(mxd)
    publish.startpy('C:/Users/86139/PycharmProjects/myArcgis/mxd_Dir/tif__b8b56f21-7ade-11ed-ad5e-6c6a773bbaf9.mxd')


    # publish.startpy('C:/Users/86139/PycharmProjects/myArcgis/mxd_Dir/cm__6afe680f-76d6-11ed-a3fa-6c6a773bbaf9.mxd')


    # lst = os.listdir('mxd_Dir/')
    # print (lst)
    # mxd=publish.create_mxd('test')
    # publish.rewrite_mxd(mxd,'D:/GIS/ShangHai_ChongMing/庙镇.shp')