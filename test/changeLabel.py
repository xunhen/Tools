import os, sys
import cv2
import numpy as np
import copy
import shutil


class ChangeLabel(object):
    def __init__(self, dataPathList, savePathList, labels_org, label_now, start_index=0, prefix='LP',
                 need_save_image=False):
        if type(dataPathList) is not list:
            dataPathList = [dataPathList, ]
        if type(savePathList) is not list:
            savePathList = savePathList
        assert len(dataPathList) == len(savePathList)
        assert len(labels_now) == len(labels_org)
        self.dataPathList = dataPathList
        self.savePathList = savePathList
        self.labels_org = labels_org
        self.labels_now = label_now
        self.need_save_image = need_save_image
        self.start_index = start_index
        self.prefix = prefix
        pass

    def startTask(self):
        for index, dataPath in enumerate(self.dataPathList):
            for fileName in os.listdir(dataPath):
                if self.isExist(dataPath, fileName):
                    fileName = fileName[:-4]
                    print('process image {} begin!!'.format(fileName))
                    saveFileName = fileName

                    self.changeLabel(dataPath, fileName, self.savePathList[index])
                    print('process image {} end!!'.format(fileName))
        pass

    def changeLabel(self, dataPath, fileName, savePath):
        if self.start_index is not None:
            saveFileName = self.prefix + str(self.start_index)
        if not os.path.exists(savePath) or not os.path.isdir(savePath):
            os.makedirs(savePath)
        bboxs_org = []
        with open(dataPath + '\\' + fileName + 'org.txt') as file:
            for line in file.readlines():
                line = line.split(' ')
                label = self.findLabel(int(line[0]))
                if label == -1:
                    continue
                width = int(line[1])
                height = int(line[2])
                bboxs_org.append([int(line[3]), int(line[4]), int(line[5]), int(line[6]), label])

        if len(bboxs_org) > 0:
            with open(savePath + "//" + saveFileName + '.txt', 'w') as txt:
                with open(savePath + '//' + saveFileName + 'org.txt', 'w') as orgtxt:
                    for i in range(len(bboxs_org)):
                        orgtxt.write(
                            "{} {} {} {} {} {} {}\n".format(bboxs_org[i][4], width, height, bboxs_org[i][0],
                                                            bboxs_org[i][1],
                                                            bboxs_org[i][2],
                                                            bboxs_org[i][3]))
                        txt.write(
                            "{} {} {} {} {}\n".format(bboxs_org[i][4], (bboxs_org[i][0] + bboxs_org[i][2] / 2) / width,
                                                      (bboxs_org[i][1] + +bboxs_org[i][3] / 2) / height,
                                                      bboxs_org[i][2] / width, bboxs_org[i][3] / height))
            if self.need_save_image:
                shutil.copyfile(os.path.join(dataPath, fileName + '.jpg'),
                                os.path.join(savePath, saveFileName + '.jpg'))
            if self.start_index is not None:
                self.start_index += 1
        pass

    def findLabel(self, label):
        for index, label_ in enumerate(self.labels_org):
            if label_ == label:
                return self.labels_now[index]
        return -1

    def isExist(self, dataPath, fileName):
        if os.path.isfile(os.path.join(dataPath, fileName)) and fileName.endswith('.jpg'):
            fileName = fileName[:-4]
            if os.path.isfile(os.path.join(dataPath, fileName + '.txt')) and os.path.isfile(
                    os.path.join(dataPath, fileName + 'org.txt')):
                return True
        return False


if __name__ == '__main__':
    dataPathList = [r'C:\Users\27591\Desktop\test\train']
    savePathList = [r'C:\Users\27591\Desktop\test\sample']
    labels_org = list(range(11))
    labels_now = [0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1]
    changeLabel = ChangeLabel(dataPathList=dataPathList, savePathList=savePathList, label_now=labels_now,
                              labels_org=labels_org, need_save_image=True)
    changeLabel.startTask()
    pass
