# -*- coding: utf-8 -*-
import arcpy
import os
import xml.dom.minidom as DOM


def SetSddraftParam(sddraft_file_path):
    '''修改Sddraft文件的参数。（一般就修改开启WMS、WFS功能）

    Args:
        sddraft_file_path: .sddraft文件的路径。
    '''
    doc = DOM.parse(sddraft_file_path)
    ext = doc.getElementsByTagName('Extensions')[0]
    svcExts = ext.childNodes
    for svcExt in svcExts:
        typename_ele = svcExt.getElementsByTagName('TypeName')[0]
        if typename_ele.firstChild.data == 'WMSServer':
            enable_ele = svcExt.getElementsByTagName('Enabled')[0]
            enable_ele.firstChild.data = 'true'
            break
    if os.path.exists(sddraft_file_path):
        os.remove(sddraft_file_path)
    f = open(sddraft_file_path, 'w')
    doc.writexml(f)
    f.close()


def GetAGSConnectionFile(out_folder_path):
    '''在指定文件夹新建test.ags文件。

    Args:
        out_folder_path: .ags文件的输出文件夹路径。

    Returns:
        返回.ags文件的路径。
    '''
    out_name = 'test.ags'
    server_url = 'http://localhost:6080/arcgis/admin'
    use_arcgis_desktop_staging_folder = False
    staging_folder_path = out_folder_path
    username = 'siteadmin'
    password = '123456'
    out_file_path = os.path.join(out_folder_path, out_name)
    if os.path.exists(out_file_path):
        os.remove(out_file_path)
    arcpy.mapping.CreateGISServerConnectionFile('ADMINISTER_GIS_SERVICES',
                                                out_folder_path,
                                                out_name,
                                                server_url,
                                                'ARCGIS_SERVER',
                                                use_arcgis_desktop_staging_folder,
                                                staging_folder_path,
                                                username,
                                                password,
                                                True)
    return out_file_path


def PublishMxd(mxd_file_path, mxd_folder_path, con_file_path):
    '''发布服务。

    Args:
        mxd_file_path:mxd文档的路径。
        mxd_folder_path:mxd文档所在文件夹的路径。
        con_file_path:服务器连接文件路径
    '''
    # 检查mxd文件是否存在
    print "Checking mxd file path..."
    if os.path.exists(mxd_file_path) == False:
        print "mxd file is not exist！"
        return

    # 打开mxd文档
    try:
        print "Opening mxd file..."
        mxd = arcpy.mapping.MapDocument(mxd_file_path)
    except Exception, e:
        print "open mxd error: ", e
        return

    # 获取默认的数据框
    print "Loading mxd file default dataframes..."
    df = ""
    try:
        frames = arcpy.mapping.ListDataFrames(mxd, "图层")
        if len(frames) == 0:
            frames = arcpy.mapping.ListDataFrames(mxd, "Layers")
        df = frames[0]
    except Exception, e:
        print "load mxd file default dataframes failed：", e
        return
    # 组织参数发布服务
    mxdNameWithExt = os.path.basename(mxd_file_path)
    (serviceName, extension) = os.path.splitext(mxdNameWithExt)
    sddraft_file_path = os.path.join(mxd_folder_path, serviceName + '.sddraft')
    summary = 'Test'
    tags = 'Test'
    # 创建草图文件
    print "CreateMapSDDraft..."
    if os.path.exists(sddraft_file_path):
        os.remove(sddraft_file_path)
    arcpy.mapping.CreateMapSDDraft(mxd, sddraft_file_path, serviceName, 'ARCGIS_SERVER', con_file_path, False, None,
                                   summary, tags)
    # 设置草图文件内的参数（开启WMS功能，WFS功能等）
    SetSddraftParam(sddraft_file_path)
    # 分析草图文件
    analysis = arcpy.mapping.AnalyzeForSD(sddraft_file_path)
    if analysis['errors'] == {}:
        for message in analysis['messages']:
            print analysis['messages'][message]
            print message[0].encode("gb2312") + "(%s)" % message[1]
        for warning in analysis['warnings']:
            print analysis['warnings'][warning]
            print warning[0].encode("gb2312") + "(%s)" % warning[1]
        # 过渡服务
        print "StageService..."
        sdPath = os.path.join(mxd_folder_path1, serviceName + '.sd')
        arcpy.StageService_server(sddraft_file_path, sdPath)
        # 上传服务定义
        print "UploadServiceDefinition_server..."
        arcpy.UploadServiceDefinition_server(sdPath, con_file_path)
    else:
        for error in analysis['errors']:
            print analysis['errors'][error]
            print error[0].encode("gb2312") + "(%s)" % error[1]


def PublishAll(mxd_folder_path):
    '''遍历指定文件夹内的所有mxd文档，并逐个发布服务。

    Args:
        mxd_folder_path:包含mxd文档的文件夹路径。
    '''
    print "Check folder path..."
    if os.path.isdir(mxd_folder_path) == False:
        print "folder path is not exist！"
        return
    print "Get .ags file..."
    con_file_path = GetAGSConnectionFile(mxd_folder_path)
    print "******************Traversing a folder******************"
    files = os.listdir(mxd_folder_path)
    mxdCount = 0
    for f in files:
        if f.endswith(".mxd"):
            mxdCount = mxdCount + 1
    mxdNo = 1
    for f in files:
        if f.endswith(".mxd"):
            mxd_file_path = os.path.join(mxd_folder_path, f)
            print "Publishing: " + f + "(%d/%d)" % (mxdNo, mxdCount)
            mxdNo = mxdNo + 1
            PublishMxd(mxd_file_path, mxd_folder_path, con_file_path)
        else:
            continue


mxd_folder_path = r'E:\MyCode\Mypy\py2\mxd'
publishServices.PublishAll(mxd_folder_path)
