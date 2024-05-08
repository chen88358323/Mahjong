from test.util.cc.duplicateFIle.cc.model import FileDetailModelDup, FileDetailModel


#import FileDetailModelDao,FileDetailModel,FileDetailModelDup
#FileDetailModel 转换FileDetailModelDup 测试类
def modelconvert():
    # fobj=FileDetailModel()
    fobj = FileDetailModel.FileDetailModel('hcode', 0, 'pathstr', 'filename',
                                          'txt')

    objstr=fobj.__str__()
    print('objstr' + objstr)
    #str=unstructure(fobj)
    # print('序列化'+str(str))
    #fobjdup=structure(str,FileDetailModel.FileDetailModel)
    fobjdup= FileDetailModelDup.FileDetailModelDup(fobj.hcode, fobj.isdir, fobj.path, fobj.filename, fobj.filetype)
    print('fobjdup'+str(fobjdup))
#todo 手动赋值

if __name__ == '__main__':
    modelconvert()