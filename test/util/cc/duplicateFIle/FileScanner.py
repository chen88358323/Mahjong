import datetime
import hashlib
import os
import copy
from test.util.cc.duplicateFIle.model import FileDetailModelDao,FileDetailModel
from test.util.cc.duplicateFIle import logger
videoType = ['.avi', '.mp4', '.ts', '.flv', '.rmvb', '.rm']
#批量文件处理个数
batchsize=50
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
            for fileobj in fileObjList:
                if fileobj.hcode in fileCodeSet:
                    fileCodeSet.remove(fileobj.hcode)
                    tarlist.append(fileobj)
            dulicatelist= list(set(fileObjList)-set(tarlist))
            if(len(dulicatelist))>0:
                logger.log.error("该记录存在重复数据")
                for fileobj in dulicatelist:
                    logger.log.error(str(fileobj))
            fileObjList=tarlist

        return fileObjList


    # def filterUselessFile(filename):
    def __findFileDetail(self,path):#获取需要对比的文件完整路径
        fileObjList=[]
        fileCodeSet=set()
        for dirpath, dirnames, filenames in os.walk(path):
            i=0
            for filename in filenames:
                if i==batchsize:#满足条件批量插入
                    i=0
                    fileObjList= self.__clearFileObjList(fileObjList, fileCodeSet)
                    FileDetailModelDao.addBatch(fileObjList)
                    fileObjList.clear()
                    fileCodeSet.clear()

                portion = os.path.splitext(filename)
                if portion[1] in videoType:
                    fullfilepath = os.path.join(dirpath, filename)

                    # DBModule.add
                    code=self.__mdavMD5(fullfilepath)
                    if os.path.isdir(fullfilepath):
                        isDir=1
                    else:
                        isDir=0
                    # dirpath  filename portion[1]
                    obj=FileDetailModel.FileDetailModel(hcode=code,isdir=isDir,path=dirpath,filename=filename,
                                        filetype=portion[1])
                    fileObjList.append(obj)
                    fileCodeSet.add(code)
                    i+=1

            if(fileObjList is not None and len(fileObjList)>0):
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

    def __showReault(self):
        for i in self.result.keys():
            if self.result[i].__len__()>1:
                logger.log.info("下列文件的重复文件(校验码{})：".format(i))
                self.__saveReault("\n\n\n下列文件的重复文件(校验码{})：".format(i))
                for j in self.result[i]:
                    logger.log.info(j)
                    self.__saveReault(j)

    #主流程
    def __main(self):
        #1.加载待扫描路径
        self.__getSearchHeavyPaths()
        # 2.开始扫描入库
        self.__findAllFileTree()
        #入库

        #es
        #写文件
        # self.__contrastCheckValue()
        # self.__showReault()
        # self.__removeFile()


    #相关的信息摘要算法
    def __mdavMD5(self, path):
        md5file = open(path, 'rb')
        md5 = hashlib.md5(md5file.read()).hexdigest()
        md5file.close()
        logger.log.info(md5)
        return md5

    def __mdavSHA1(self, path):
        sha1file = open(path, 'rb')
        sha1 = hashlib.sha1(sha1file.read()).hexdigest()
        sha1file.close()
        logger.log.info(sha1)
        return sha1

    def __mdavSHA128(self, path):
        sha1file = open(path, 'rb')
        sha128 = hashlib.shake_128(sha1file.read()).hexdigest()
        sha1file.close()
        logger.log.info(sha128)
        return sha128

    def _mdavSHA256(self,path):
        sha1file = open(path, 'rb')
        sha256 = hashlib.sha_256(sha1file.read()).hexdigest()
        sha1file.close()
        logger.log.info(sha256)
        return sha256


    def __mdavSHA512(self, path):
        sha512file = open(path, 'rb')
        sha512 = hashlib.sha512(sha512file.read()).hexdigest()
        sha512file.close()
        logger.log.info(sha512)
        return sha512

    def __getSearchHeavyPaths(self):#获取需要进行查重的文件夹目录
        self.searchHeavyPaths.add("D:\\360Download\\仓鼠管家\\")
        # self.searchHeavyPaths.add("V:\\")
        # self.searchHeavyPaths.add("W:\\")
        # self.searchHeavyPaths.add("X:\\")
        # self.searchHeavyPaths.add("H:\\done")
        # self.searchHeavyPaths.add("I:\\done")
        # self.searchHeavyPaths.add("J:\\done")
        # self.searchHeavyPaths.add("K:\\done")




if __name__ == '__main__':
    a=FileChecking()