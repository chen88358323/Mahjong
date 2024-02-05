import datetime

import os,sys,platform
from test.util.cc.duplicateFIle.model import FileDetailModelDao,FileDetailModel,FileDetailModelDup
from test.util.cc.duplicateFIle import logger
from test.util.cc.duplicateFIle.utils import  encryutil
videoType = ['.avi', '.mp4', '.ts', '.flv', '.rmvb', '.rm']
#批量文件处理个数
platform='windows'
batchsize=500

class FileChecking():
    def __init__(self):
        logger.log.info("正在进行初始化设置......")
        #默认的配置信息
        self.searchHeavyPaths=set()#等待查重的文件夹路径
        self.WaitForComparisonFiles=set()#等待对比的文件
        self.FileCheckValue={}#文件及其校验值
        self.result={}
        self.saveReaultPath="Result"

        #重命名存储结果的文件
        nowTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+".txt"
        self.saveReaultPath+=str(nowTime)
        logger.log.info(self.saveReaultPath+"初始化完成！")

        #执行主程序
        self.__main()

        logger.log.info("程序执行完成，按任意键退出程序")


    #根据后缀名判断是否是视频文件
    def __isVideo(self,path):
        res=False
        for type in videoType:
            if(path.endswith(type)):
                res=True
                break
        return  res
    #清理文件列表中可能存在的重复数据
    def __clearFileObjList(self,fileObjList,fileCodeSet):
        if len(fileObjList)!=len(fileCodeSet):

            tarlist=[]
            duplist=[]
            for fileobj in fileObjList:
                if fileobj.hcode in fileCodeSet:
                    fileCodeSet.remove(fileobj.hcode)
                    tarlist.append(fileobj)
            dulicatelist= list(set(fileObjList)-set(tarlist))
            if(len(dulicatelist))>0:

                logger.log.error("上传数据集存在重复数据")
                for fileobj in dulicatelist:
                    fileobjdup=FileDetailModelDao.convert2FileDetailModelDup(fileobj)
                    duplist.append(fileobjdup)
                    FileDetailModelDao.addBatch(duplist)
            fileObjList=tarlist

        return fileObjList

    def __getdriver(self,path):
        driver, rem = os.path.splitdrive(path)
        return  driver

    # def filterUselessFile(filename):
    #path  获取需要对比的文件完整路径
    #
    def __findFileDetail(self,path):#获取需要对比的文件完整路径
        fileObjList=[]
        fileCodeSet=set()

        # dirver为盘符路径  C:\Users\wuyanzu\  获取盘符为c:
        driver=self.__getdriver(path)
        platformscan=self.__getPlatform()

        for dirpath, dirnames, filenames in os.walk(path):
            i=0
            for filename in filenames:
                if i==batchsize:#满足条件批量插入
                    i=0
                    self.__batchAndClear(fileObjList,fileCodeSet)

                portion = os.path.splitext(filename)
                if portion[1] in videoType:
                    fullfilepath = os.path.join(dirpath, filename)

                    # DBModule.add
                    #code=self.__mdavMD5HighPerform(fullfilepath)
                    #头尾计算md5
                    code=encryutil.calc_file_hash(fullfilepath)

                    if os.path.isfile(fullfilepath):
                        isDir=0
                    else:
                        isDir=1
                    # dirpath  filename portion[1]
                    filedir = dirpath.replace(driver, '')
                    obj=FileDetailModel.FileDetailModel(hcode=code,isdir=isDir,path=filedir,filename=filename,
                                        filetype=portion[1],systemdriver=driver,platformscan=platformscan,
                                                        keyword=None,belong=None)
                    fileObjList.append(obj)
                    fileCodeSet.add(code)
                    i+=1
        #
        self.__batchAndClear(fileObjList,fileCodeSet)

    #fileObjList  FileDetailModel 集合
    #fileCodeSet  hcode set ，放置提交的一批次数据中含有重复内容
    def __batchAndClear(self,fileObjList,fileCodeSet):
        if (fileObjList is not None and len(fileObjList) > 0):
            fileObjList = self.__clearFileObjList(fileObjList, fileCodeSet)
            FileDetailModelDao.addBatch(fileObjList)
            fileObjList.clear()
            fileCodeSet.clear()


    def __findAllFileTree(self):#查找每一个待查重的文件的所有的子文件
        logger.log.info("\n\n\n\n准备获取所有待对比的文件完整路径......")
        for path in self.searchHeavyPaths:
            # try:
            self.__findFileDetail(path)
            # except:
            #     pass
        logger.log.info("获取文件目录树完成！")


    def __contrastCheckValue(self):
        logger.log.info("正在处理数据......")
        self.result = {}
        for i in self.FileCheckValue.values():
            self.result[i] = []
        for i in self.FileCheckValue.keys():
            self.result[self.FileCheckValue[i]].append(i)
        #logger.log.info(self.FileCheckValue)
        logger.log.info("查重完成，正在生成结果......")

    def __saveReault(self,pt):
        logfile='D:\\temp\\dist\\'+self.saveReaultPath
        logger.log.info('log '+logfile)
        file=open(logfile,"a",encoding='utf-8')
        file.write(pt+"\n")
        file.close()

    #比对两个数据表内的数据
    def __showReault(self):
        dupfilelist=[]
        num=FileDetailModelDao.querydupfileCounts()
        if(num>0):
            print('show result duplicate num:'+str(num))
            #1.获取重复数据列表
            dupfilelist=FileDetailModelDao.queryAlldupfiles()
            if dupfilelist is not None and len(dupfilelist)>0:
                for dupfile in dupfilelist:
                    # 2.查询对应数据原始数据对应列表
                    file=FileDetailModelDao.queryfilebycode(dupfile.hcode)
                    if file is None:  # 这里好像判断没啥用，不如直接返回
                        logger.log.info(dupfile.hcode+" 没有对应filedetail表的记录")
                    else:
                        logger.log.warning("*******************************************")
                        logger.log.warning(dupfile.hcode )
                        logger.log.warning("file   :"+(file.systemdriver+file.path+file.filename))
                        logger.log.warning("dupfile:"+(dupfile.systemdriver+dupfile.path+dupfile.filename))
                        logger.log.warning("                             ")
            else:
                logger.log.warn("*******************************************")
                logger.log.warn("filedetail_dup 无数据")

            #3. todo 迁移文件至缓存文件夹
        else:
            print( 'filedetail_dup 无重复数据')



    #主流程
    def __main(self):
        path = input()
        print("清理表数据请输入y,拒绝请按其他键")
        if path == "y":
            #清理数据表
            self.__cleartables()
        else:
            print("未清理表数据")
        #1.加载待扫描路径
        self.__getSearchHeavyPaths()
        # 2.开始扫描入库
        self.__findAllFileTree()
        # 3.数据比较

        #es
        #写文件
        # self.__contrastCheckValue()
        self.__showReault()
        # self.__removeFile()


    #获取当前系统信息
    def __getPlatform(self):


        if sys.platform.startswith('linux'):
            current_os="Linux"
        elif sys.platform.startswith('win'):
            current_os="Windows"
        elif sys.platform.startswith('darwin'):
            current_os = "MAC"
        else:
            current_os = str(sys.platform)
        return current_os

#import sys
    # if sys.platform.startswith('linux'):
    #     print('当前系统为 Linux')
    # elif sys.platform.startswith('win'):
    #     print('当前系统为 Windows')
    # elif sys.platform.startswith('darwin'):
    #     print('当前系统为 macOS')
    # else:
    #     print('无法识别当前系统')

    def __getSearchHeavyPaths(self):#获取需要进行查重的文件夹目录
        self.searchHeavyPaths.add("D:\\360Download\\仓鼠管家\\")
        # self.searchHeavyPaths.add("I:\\")
        # self.searchHeavyPaths.add("J:\\")
        # self.searchHeavyPaths.add("K:\\")
        # self.searchHeavyPaths.add("L:\\")
        # self.searchHeavyPaths.add("V:\\")
        # self.searchHeavyPaths.add("W:\\")
        # self.searchHeavyPaths.add("X:\\")
        # self.searchHeavyPaths.add("H:\\done")
        # self.searchHeavyPaths.add("I:\\done")
        # self.searchHeavyPaths.add("J:\\done")
        # self.searchHeavyPaths.add("K:\\done")

    def __cleartables(self):
        FileDetailModelDao.truncatetables(FileDetailModel.FileDetailModel.__tablename__)
        FileDetailModelDao.truncatetables(FileDetailModelDup.FileDetailModelDup.__tablename__)




if __name__ == '__main__':
    a=FileChecking()