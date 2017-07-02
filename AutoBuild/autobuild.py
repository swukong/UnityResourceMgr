#! usr/bin/python #coding=utf-8

'''
自动化打包脚本
'''

import os, sys, platform
import  configfile

#######全局变量

#输入的APK版本号
ApkVersion = "2.0.0.0"
#基础资源版本号
BaseResVersion = "1.0.0.0"
#增量资源版本号
AppendResVersion = "1.0.0.0"
#输入平台：0-Windows 1-Android 2-IOS
BuildPlatform = -1

##############

def CheckVersionFormat(version):
    return True

def UserInputVersion():

    while True:
        s = raw_input("请输入打包平台(0-Windows 1-Android 2-IOS)：")
        if (s.isdigit()):
            BuildPlatform = int(s)
            if BuildPlatform in [0, 1, 2]:
                if (IsWindowsPlatform() and (BuildPlatform == 2)):
                    print "Windows平台无法打包IOS"
                else:
                    break

    '''
    while True:
        ApkVersion = raw_input("请输入APK版本号(格式：2.x.x.x)：")
        if CheckVersionFormat(ApkVersion):
            break
    '''
    while True:
        BaseResVersion = raw_input("请输入基础资源版本号(格式：1.x.x.x)：")
        if CheckVersionFormat(BaseResVersion):
            break
    '''
    while True:
        AppendResVersion = raw_input("请输入增量资源版本号(格式：1.x.x.x)：")
        if CheckVersionFormat(AppendResVersion):
            break
    '''
    return

def SaveVersionInfo():
    return

def LoadVersionInfo():
    fileName = "%s/buildVersion.cfg" % GetUnityOrgProjPath()
    if (not os.path.exists(fileName)) or (not os.path.isfile(fileName)):
        return
    file = open(fileName, "r");
    if file == None:
        return
    version = file.readline()
    BaseResVersion = version
    AppendResVersion = version

    print "当前资源版本: %s \n" % version
    return

def GetUnityOrgProjPath():
    result = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    return result

def GetUnityProjPath():
    result = GetUnityOrgProjPath() + "/outPath/Proj"
    return result

def IsWindowsPlatform():
    return "Windows" in platform.system()

def IsMacPlatform():
    return "Darwin" in platform.system()

def UnityBuildABProj():
    projPath = GetUnityProjPath()
    if (not os.path.exists(projPath)) or (not os.path.isdir(projPath)):
        if IsMacPlatform():
            cmd = "/Application/Unity/Unity.app/Contents/MacOS/Unity"
            if not os.path.exists(cmd):
                print "\n未安装Unity, 请下载Unity!!!"
                return False
            os.system("%s -quit -batchmode -nographics -createProject %s" % (cmd, projPath))
        elif IsWindowsPlatform():
            os.system("Unity.exe -quit -batchmode -nographics -createProject %s" % projPath)
        else:
            print "不支持此平台打包"
            return False
    return True

def UnityAndroidProjToApk():
    return

def UnityIOSProjToIPA():
    return

def UnityToExe():
    projPath = GetUnityOrgProjPath()
    if (not os.path.exists(projPath)) or (not os.path.isdir(projPath)):
        print "项目为空"
        return False
    if IsMacPlatform():
        cmd = "/Application/Unity/Unity.app/Contents/MacOS/Unity"
        if not os.path.exists(cmd):
            print "\n未安装Unity, 请下载Unity!!!"
            return False
        os.system("%s -quit -batchmode -nographics -projectPath %s -executeMethod AssetBundleBuild.Cmd_Win" % (cmd, projPath))
    elif IsWindowsPlatform():
        os.system("Unity.exe -quit -batchmode -nographics -projectPath %s -executeMethod AssetBundleBuild.Cmd_Win" % projPath)
    return True

# 主函数
def Main():

    if (IsWindowsPlatform()):
        print "打包前请确认设置好Unity.exe环境变量"

    LoadVersionInfo()
    UserInputVersion()
    SaveVersionInfo()
    # Windows平台直接生成EXE
    if BuildPlatform == 0:
        UnityToExe()
    else:
        UnityBuildABProj()
        if BuildPlatform == 1:
            UnityAndroidProjToApk()
        elif BuildPlatform == 2:
            UnityIOSProjToIPA()
    return

##################################### 调用入口 ###################################
Main()
#################################################################################