import os, sys
import re

'''
   暂时不支持paths_to
'''


class Summary(object):

    def __init__(self, paths, summaryNames, pattern=None, paths_to=None, recursive=True):
        self.paths = self.getList(paths)
        self.summaryNames = self.getList(summaryNames)
        self.paths_to = self.getList(paths_to)
        self.pattern = pattern
        self.recursive = recursive

    def startTask(self):
        for index, path in enumerate(self.paths):
            pathRecs = [path, ]
            number = 0
            with open(os.path.join(path, self.summaryNames[index]), 'w') as file:
                for pathRec in pathRecs:
                    for filename in os.listdir(pathRec):
                        filenamePath = os.path.join(pathRec, filename)
                        if self.recursive and os.path.isdir(filenamePath):
                            pathRecs.append(filenamePath)
                            continue
                        if self.pattern is None or re.search(self.pattern, pathRec) is not None:
                            if filename.endswith('.jpg'):
                                if self.paths_to is not None:
                                    filenamePath = re.sub(self.paths[index], self.paths_to[index], filenamePath)
                                file.write(filenamePath + '\n')
                                number += 1
            print('{}: {}'.format(self.summaryNames[index], number))

    def getList(self, file):
        if file is None:
            return file
        if type(file) is not list:
            return [file, ]
        else:
            return file


if __name__ == '__main__':
    path = [r'E:\DataSet\GJDataSet\overpass\val', ]
    name = ['train.txt', ]
    pattern = r'(train_org$)|(train_add1$)|(train_add2$)|(slide3x3((/+)|(\\+)).-.-0)'
    summary = Summary(path, name, pattern=pattern)
    summary.startTask()
    pass
