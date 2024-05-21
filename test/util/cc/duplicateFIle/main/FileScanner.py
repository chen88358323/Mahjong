import datetime
from collections import ChainMap
import os
from test.util.cc.duplicateFIle.cc.model import FileDetailModelDup, FileDetailModel, FileDetailModelDao,LocalCache
from test.util.cc.duplicateFIle.cc.utils import logger,encryutil,dirutil

#TODO  增加虚拟盘符支持
#TODO  ES增加

#视频类型分类
category=['spj','sp','ds','hj','mj','md','pic','jvid','xz','sm','of','tui','pic','zp',]

#虚拟分区，为区分每个分区的唯一性
virtualLocation=['ZB','SPJ','SP','SPJ-A','SPJHJ','E','H','I','J','K','G','O','V','X','N','T','','Z',]


videoType = ['.avi', '.mp4', '.ts', '.flv','.mkv','.mov', '.rmvb', '.rm', '.mpeg', '.wmv']

#批量文件处理个数
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
        logger.log.info(self.saveReaultPath + "初始化完成！")

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


        return duplicate_objects
    #清理文件列表中可能存在的重复数据
    def __clearFileObjList(self,fileObjList,fileCodeSet):
        if len(fileObjList)!=len(fileCodeSet):

            tarlist=[]
            duplist=[]
            #遍历，生成tarlist
            for fileobj in fileObjList:
                if fileobj.hcode in fileCodeSet:
                    fileCodeSet.remove(fileobj.hcode)
                    tarlist.append(fileobj)

            dulicatelist= list(set(fileObjList)-set(tarlist))
            if(dulicatelist is not None and len(dulicatelist))>0:
                logger.log.error("上传数据集存在重复数据" + str(len(dulicatelist)))
                for fileobj in dulicatelist:
                    fileobjdup= FileDetailModelDao.convert2FileDetailModelDup(fileobj)
                    duplist.append(fileobjdup)
                #增加重复数据
                FileDetailModelDao.addBatch(duplist)
                duplist.clear()
                dulicatelist.clear()

            fileObjList=tarlist

        return fileObjList


    # 判断是否是扫描文件
    def __isScanFile(self,filesuffix):
        return True
        # if (filesuffix in videoType):
        #     return  True
        # else:
        #     return  False
    # def filterUselessFile(filename):


    #path  获取需要对比的文件完整路径
    #
    def __findFileDetail(self,path):#获取需要对比的文件完整路径
        fileObjList = []
        fileCodeSet = set()

        originalcache=LocalCache.load_snapshot(path)
        # dirver为盘符路径  C:\Users\wuyanzu\  获取盘符为c:
        # platformscan  Windows  or  LinuxYES
        driver, platformscan = dirutil.getDriverAndPlatForm(path)
        virtualPath=dirutil.getVirtualPath(path,'.ini')
        addcache =  dict()
        if originalcache is None:#无缓存直接扫描
            for dirpath, dirnames, filenames in os.walk(path):
                # print("dirpath"+dirpath)
                # print("dirnames"+dirnames)
                if dirutil.isScanDir(dirpath):
                    continue
                else:
                    i = 0
                    for filename in filenames:
                        if i == batchsize:  # 满足条件批量插入
                            i = 0
                            fileObjList = self.__batchAndClear(fileObjList, fileCodeSet)
                        obj = self.__buildFileDetailModel(filename, dirpath, driver, platformscan,virtualPath)
                        fileObjList.append(obj)
                        fileCodeSet.add(obj.hcode)
                        #file.systemdriver + file.path + file.filename
                        addcache[obj.systemdriver+obj.path+obj.filename]=obj.hcode
                        i += 1
                    #TODO ADD ES
                    self.__batchAndClear(fileObjList, fileCodeSet)
            #存储全部缓存
            LocalCache.save_snapshot(path, addcache)
        else:
            originalFileList=originalcache.keys()

            newCacheFileList=[]
            for dirpath, dirnames, filenames in os.walk(path):
                if dirutil.isScanDir(dirpath):
                    continue
                else:
                    i = 0
                    for filename in filenames:
                        fullfilepath = os.path.join(dirpath, filename)
                        newCacheFileList.append(fullfilepath)


            addfiles=[file for file in newCacheFileList if file not in originalFileList ]

            delfiles=[file for file in originalFileList if file not in newCacheFileList]

            logger.log.info('增量扫描文件 新增文件数' + str(len(addfiles))+' 删除文件数'+str(len(delfiles)))
            #1.扫描新增filelist 生成缓存 #TODO ADD ES
            newCacheDict=self.__batchAddFileDetailModelByFileList(addfiles,driver, platformscan ,virtualPath)

            self.__syncDelFile(originalcache,delfiles,driver)
            #两个缓存相加
            newCache=ChainMap(newCacheDict,originalcache)
            LocalCache.save_snapshot(path, newCache)

    #将删除信息增加值LOCALCACHE  DB  TODO ES
    def __syncDelFile(self,originalcache,delfiles,driver):
        # 2.1 根据keylist更新删除的数据  CACHE #
        originalcache ,delcache  = LocalCache.clearCacheByKeyList(originalcache, delfiles)
        # 2.2 根据keylist更新删除的数据  DB #TODO ADD ES
        hashs = []
        pathes = []
        filenames = []
        if delcache is not None and len(delcache)>0:
            for k ,v in delcache.items():
                fn,dn=dirutil.splitPath2fnameDname(k,driver)
                hashs.append(v)
                pathes.append(dn)
                filenames.append(fn)
            FileDetailModelDao.delBatchByHC_PATH_FN(hashs,pathes,filenames)
        #3. TODO ADD ES

    #根据文件列表，批量更新数据库
    def __batchAddFileDetailModelByFileList(self,filelist,driver, platformscan ,virtualPath):
        fileObjList = []
        fileCodeSet =  set()

        addcache= dict()
        if filelist is None or len(filelist) ==0:
            return dict()
        else:
            i = 0
            for f in filelist:
                if i == batchsize:  # 满足条件批量插入
                    i = 0
                    fileObjList = self.__batchAndClear(fileObjList, fileCodeSet)
                obj = self.__buildFileDetailModelByPath(f,driver, platformscan,virtualPath )
                fileObjList.append(obj)
                fileCodeSet.add(obj.hcode)
                # file.systemdriver + file.path + file.filename
                #新增缓存
                addcache[obj.systemdriver + obj.path + obj.filename] = obj.hcode
                i += 1
            fileObjList = self.__batchAndClear(fileObjList, fileCodeSet)
        return addcache
        # 构建文件列表构建详细信息对象
    def __buildFileDetailModelByPath(self, filepath, driver, platformscan,virtualPath):
        filename,filedir = dirutil.splitPath2fnameDname(filepath,driver)

        portion = os.path.splitext(filename)

        # 头尾计算md5
        code, filesize = encryutil.calc_halffile_hash(filepath)
        isDir = 0
        obj = FileDetailModel.FileDetailModel(hcode=code, isdir=isDir, path=filedir, filename=filename,
                                              filetype=portion[1], systemdriver=driver,
                                              platformscan=platformscan,
                                              keyword=None, belong=None, filesize=filesize,
                                              virdriver=virtualPath)
        return obj
    #构建文件详细信息对象
    def __buildFileDetailModel(self,filename,dirpath,driver,platformscan,virtualPath):
        portion = os.path.splitext(filename)
        # if self.__isScanFile(portion[1]):
        fullfilepath = os.path.join(dirpath, filename)

        # 头尾计算md5
        # code ,filesize = encryutil.calc_file_hash(fullfilepath)
        # 尾计算md5
        code, filesize = encryutil.calc_halffile_hash(fullfilepath)

        if os.path.isfile(fullfilepath):
            isDir = 0
        else:
            isDir = 1
        # dirpath  filename portion[1]
        filedir = dirpath.replace(driver, '')
        obj = FileDetailModel.FileDetailModel(hcode=code, isdir=isDir, path=filedir, filename=filename,
                                              filetype=portion[1], systemdriver=driver,
                                              platformscan=platformscan,
                                              keyword=None, belong=None, filesize=filesize,
                                              virdriver=virtualPath)
        return  obj
    #fileObjList  FileDetailModel 集合
    #fileCodeSet  hcode set ，放置提交的一批次数据中含有重复内容
    def __batchAndClear(self,fileObjList,fileCodeSet):
        if (fileObjList is not None and len(fileObjList) > 0):
            fileObjList = self.__clearFileObjList(fileObjList, fileCodeSet)
            FileDetailModelDao.addBatch(fileObjList)
            # fileObjList.clear()
            fileCodeSet.clear()
        return fileObjList


    def __findAllFileTree(self):#查找每一个待查重的文件的所有的子文件
        for path in self.searchHeavyPaths:
            logger.log.info("\n\n\n\n准备获取所有待对比的文件完整路径......")
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
        logger.log.info('log ' + logfile)
        file=open(logfile,"a",encoding='utf-8')
        file.write(pt+"\n")
        file.close()

    #比对两个数据表内的数据
    def __showReault(self):
        dupfilelist=[]
        num= FileDetailModelDao.querydupfileCounts()
        if(num>0):
            print('show result duplicate num:'+str(num))
            #1.获取重复数据列表
            dupfilelist= FileDetailModelDao.queryAlldupfiles()
            if dupfilelist is not None and len(dupfilelist)>0:
                for dupfile in dupfilelist:
                    # 2.查询对应数据原始数据对应列表
                    file= FileDetailModelDao.queryfilebycode(dupfile.hcode)
                    if file is None:  # 这里好像判断没啥用，不如直接返回
                        logger.log.info(dupfile.hcode + " 没有对应filedetail表的记录")
                    else:
                        logger.log.warning("*******************************************")
                        logger.log.warning(dupfile.hcode)
                        logger.log.warning("file   :" + (file.systemdriver + file.path + file.filename))
                        logger.log.warning("dupfile:" + (dupfile.systemdriver + dupfile.path + dupfile.filename))
                        logger.log.warning("                             ")
            else:
                logger.log.warning("*******************************************")
                logger.log.warning("filedetail_dup 无数据")

            #3. todo 迁移文件至缓存文件夹
        else:
            print( 'filedetail_dup 无重复数据')



    #主流程
    def __main(self):
        # self.__contrastCheckValue()
        # self.__showReault()
        # self.__exchange()#清理数据，将
        # os._exit(0)

        ans = input()
        print("慎用慎用，只在测试环境输入YES,拒绝请按其他键")
        if ans == "YES":
            #清理数据 DB CACHE
            self.__cleardata4Test()
        else:
            print("未清理表数据")

        #1.加载待扫描路径
        self.__getSearchHeavyPaths()
        # 2.获取当前文件根路径的缓存文件，没有进行全表扫描
        # 3.开始扫描入库
        self.__findAllFileTree()
        # 4.显示重复数据
        # self.__showReault()
        #es
        #写文件
        # self.__contrastCheckValue()
        #self.__showReault()




    # if sys.platform.startswith('linux'):
    #     print('当前系统为 Linux')
    # elif sys.platform.startswith('win'):
    #     print('当前系统为 Windows')
    # elif sys.platform.startswith('darwin'):
    #     print('当前系统为 macOS')
    # else:
    #     print('无法识别当前系统')

    def __getSearchHeavyPaths(self):#获取需要进行查重的文件夹目录
        #本地测试
        self.searchHeavyPaths.add("D:\\360Download\\仓鼠管家\\")
        #self.searchHeavyPaths.add("K:\\spj\\spj\\")
        #self.searchHeavyPaths.add("J:\\\\榨汁夏\\")
        # self.searchHeavyPaths.add("I:\\")

        ##########linux  /home/cc/code/python/test/util/cc/duplicateFIle

        # self.searchHeavyPaths.add("/media/cc/MOIVESOFT/")
        # self.searchHeavyPaths.add("/media/cc/PJYP/")
        # self.searchHeavyPaths.add("/media/cc/ZP/")
        # self.searchHeavyPaths.add("/media/cc/娱乐/")
        # self.searchHeavyPaths.add("/media/cc/文档/")
        # self.searchHeavyPaths.add("/media/cc/系统/")
        # self.searchHeavyPaths.add("/media/cc/软件/")
        ##########linux
        # self.searchHeavyPaths.add("J:\\")
        # self.searchHeavyPaths.add("K:\\")
        # self.searchHeavyPaths.add("L:\\")
        # self.searchHeavyPaths.add("V:\\")
        # self.searchHeavyPaths.add("W:\\")
        # self.searchHeavyPaths.add("X:\\")
        # self.searchHeavyPaths.add("F:\\")
        # self.searchHeavyPaths.add("E:\\")
        # self.searchHeavyPaths.add("H:\\")
        # self.searchHeavyPaths.add("I:\\")
        # self.searchHeavyPaths.add("J:\\")
        # self.searchHeavyPaths.add("K:\\")

    def __cleardata4Test(self):
        FileDetailModelDao.truncatetables(FileDetailModel.FileDetailModel.__tablename__)
        FileDetailModelDao.truncatetables(FileDetailModelDup.FileDetailModelDup.__tablename__)
        testcachepath=r'D:\filescan.cache'
        if os.path.isfile(testcachepath):
            os.remove()


    #清理数据，将dup表数据迁移至原表中，dup表该数据进行删除
    def __exchange(self):
        hcodelist=[]
        #1.读取文件hcode
        with open('../hcode.txt', 'r', encoding="UTF-8") as file:
            content=file.readline().replace(" ","")
            content = content.replace("/n", "")
            hcodelist.append(content)
            print("hcode "+content)
        #2.获取两边信息
        for code in hcodelist:
            # 3.convert存储,删除
            file    = FileDetailModelDao.updateFileBycode(code)
            dupfile = FileDetailModelDao.querydupfilebycode(code)
            FileDetailModelDao.delDupFileByID(dupfile.id, dupfile.hcode)




if __name__ == '__main__':
    a=FileChecking()