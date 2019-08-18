import os, sys
import cv2


class DrawRoi(object):
    def __init__(self, imagePathorName,rois=None):
        self.imagePathorName = imagePathorName
        self.rois=rois

    def startTask(self):
        savePath = os.path.join(self.imagePathorName, 'output')
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        for imageName in os.listdir(self.imagePathorName):
            if not imageName.endswith('.jpg'):
                continue
            image = cv2.imread(os.path.join(self.imagePathorName, imageName))
            image_name = imageName[:-4]
            if self.rois is not None:
                for roi in self.rois:
                    cv2.rectangle(image, (int(line[3]), int(line[4])),
                                  (int(line[3]) + int(line[5]), int(line[4]) + int(line[6])), color=(255, 255, 0),
                                  thickness=2)
            if not os.path.exists(self.imagePathorName + '\\' + image_name + 'org.txt'):
                continue
            with open(self.imagePathorName + '\\' + image_name + 'org.txt') as file:
                for line in file.readlines():
                    line = line.split(' ')
                    cv2.rectangle(image, (int(line[3]),int(line[4])),(int(line[3])+int(line[5]), int(line[4])+int(line[6])),color=(0,255,255),thickness=2)
            cv2.imwrite(os.path.join(savePath, imageName), image)

if __name__ == '__main__':
    imagePathorName=r'C:\Users\27591\Desktop\sucai\roi'
    drawRoi=DrawRoi(imagePathorName)
    drawRoi.startTask()
