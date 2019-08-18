import os, sys
import cv2


class Crop(object):
    def __init__(self, imagePathorName, rois):
        self.imagePathorName = imagePathorName
        if type(rois) is not list:
            rois = [rois, ]
        self.rois = rois

    def startTask(self):
        savePath = os.path.join(self.imagePathorName, 'output')
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        for imageName in os.listdir(self.imagePathorName):
            if not imageName.endswith('.jpg'):
                continue
            image = cv2.imread(os.path.join(self.imagePathorName, imageName))
            cv2.rectangle(image,)
            for index, roi in enumerate(self.rois):
                image_roi = image[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]
                cv2.imwrite(os.path.join(savePath, '{}_'.format(index) + imageName), image_roi)


if __name__ == '__main__':
    imagePathorName = r'C:\Users\27591\Desktop\sucai'
    rois = [[314, 96, 1154, 871],]
    crop = Crop(imagePathorName,rois)
    crop.startTask()
    pass
