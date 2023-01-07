# -*- coding: utf-8 -*-
# encoding=utf8
import os
import uuid
import arcpy
import sys

# 使用者的用户名
server_username = 'siteadmin'
# 使用者的密码
server_password = '123456'

# 创建ags文件
def GetAGSConnectionFile(mxd_file_path):
    mxd_file=mxd_file_path.rsplit('/',1)
    name=mxd_file[1]
    connection_type = 'ADMINISTER_GIS_SERVICES'
    out_folder_path = "D:/GIS"  '''改为自己的输出路径'''
    out_name = name+str(uuid.uuid1())+'.ags'
    server_url = 'http://localhost:6080/arcgis/admin'
    use_arcgis_desktop_staging_folder = False
    staging_folder_path = out_folder_path
    arcpy.mapping.CreateGISServerConnectionFile(connection_type, out_folder_path, out_name, server_url,
                                                'ARCGIS_SERVER', use_arcgis_desktop_staging_folder,
                                                staging_folder_path, server_username, server_password,
                                                "SAVE_USERNAME")
    return out_folder_path+'/'+out_name

# 发布服务，con为ags文件路径
def PublishMxd(mxd_file_path, con= 'D:/GIS/ex4.ags'):
    mxd_file=mxd_file_path.rsplit('/',1)
    wrkspc=mxd_file[0]
    file_name=mxd_file[1]
    name= os.path.splitext(file_name)[0]
    mapDoc = arcpy.mapping.MapDocument(mxd_file_path)
    service_name = name+str(uuid.uuid1())
    ''''''
    sddraft = wrkspc + '/' + service_name + '.sddraft'
    sd = wrkspc + '/' + service_name + '.sd'
    summary = '1'
    tags = '1'
    analysis = arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, service_name, 'ARCGIS_SERVER', con, True, 'Default',
                                              summary, tags)
    analysis = arcpy.mapping.AnalyzeForSD(sddraft)
    if analysis['errors'] == {}:
        arcpy.StageService_server(sddraft, sd)
        arcpy.UploadServiceDefinition_server(sd, con)
    else:
        print analysis['errors']
        return 'error'
    return 'success'


def publish(mxd_file_path):
    # con=GetAGSConnectionFile(mxd_file_path)
    PublishMxd(mxd_file_path)

if __name__ == '__main__':
    publish(sys.argv[1])