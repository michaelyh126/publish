# -*- coding:UTF-8 -*-
import arcpy
import sys
from arcpy import env
from site import addsitedir
from sys import executable
from os import path
interpreter = executable
sitepkg = path.dirname(interpreter) + "\\site-packages"
print(sitepkg)
addsitedir(sitepkg)


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
    print('Start Processing ...')
    test()
    raw_input("Enter enter key to exit...")


