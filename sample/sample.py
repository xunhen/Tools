import os, sys
import cv2
import numpy as np
import copy


class Sampler(object):
    '''
    image_path_list:图片路径
    save_path_list：保存路径，和image_path_list一一对应
    start_index：保存名称开始值
    prefix：保存名称前缀
    bbox_black_threshold：删除无效像素占比达到阈值的bbox
    image_black_threshold：删除效像素占比达到阈值的image
    black_threshold：无效像素bgr
    sample_size_ratio：采样比例，如（3,3），为将原图等分3x3
    center_sample_size_ratio：中心点采样的尺度，中心点为所有bbox的中点
    scales：宽高变换
    '''

    def __init__(self, image_path_list, save_path_list, start_index=0, prefix='GJ', bbox_black_threshold=0.5,
                 image_black_threshold=0.6, black_threshold=(5, 5, 5),
                 sample_size_ratio=(3, 3), center_sample_size_ratio=[1 / 2, 2 / 3, 3 / 4], scales=[1, 3 / 4, 4 / 3],
                 center_scales=[1, 3 / 4, 4 / 3],
                 needSaveSelf=False):
        if type(image_path_list) is not list:
            self.image_path_list = [self.image_path_list, ]
        else:
            self.image_path_list = image_path_list
        if type(save_path_list) is not list:
            self.save_path_list = [self.save_path_list, ]
        else:
            self.save_path_list = save_path_list
        assert len(self.save_path_list) == len(self.image_path_list)
        self.start_index = start_index
        self.bbox_black_threshold = bbox_black_threshold
        self.sample_size_ratio = sample_size_ratio
        self.center_sample_size_ratio = center_sample_size_ratio
        self.scales = scales
        self.center_scales = center_scales
        self.prefix = prefix
        self.black_threshold = black_threshold
        self.image_black_threshold = image_black_threshold
        self.needSaveSelf = needSaveSelf
        pass

    def startTask(self):
        for index, image_path in enumerate(self.image_path_list):
            for fileName in os.listdir(image_path):
                if self.isExist(image_path, fileName):
                    fileName = fileName[:-4]
                    print('process image {} begin!!'.format(fileName))
                    self.sample(image_path, self.save_path_list[index], fileName)
                    print('process image {} end!!'.format(fileName))

    def sample(self, image_path, save_path, image_name):
        if not os.path.exists(save_path) or not os.path.isdir(save_path):
            os.makedirs(save_path)

        image = cv2.imread(image_path + '\\' + image_name + '.jpg')
        bboxs_org = []

        with open(image_path + '\\' + image_name + 'org.txt') as file:
            for line in file.readlines():
                line = line.split(' ')
                width = int(line[1])
                height = int(line[2])
                bboxs_org.append([int(line[3]), int(line[4]), int(line[5]), int(line[6]), int(line[0])])
        fullimage_rect = [0, 0, width, height]
        if self.sample_size_ratio is not None:
            width_unit = width // self.sample_size_ratio[0]
            height_unit = height // self.sample_size_ratio[1]

            for width_index in range(self.sample_size_ratio[0]):
                for height_index in range(self.sample_size_ratio[1]):

                    roi_rect = self.insect(fullimage_rect,
                                           [width_unit * width_index, height_unit * height_index,
                                            width_unit, height_unit])
                    center_width = roi_rect[0] + roi_rect[2] // 2
                    center_height = roi_rect[1] + roi_rect[3] // 2
                    for scale in self.scales:
                        rect_width = int(roi_rect[2] * scale)
                        rect_height = int(roi_rect[3] / scale)
                        roi_rect = self.insect(fullimage_rect,
                                               [center_width - rect_width // 2, center_height - rect_height // 2,
                                                rect_width,
                                                rect_height])
                        self.generate(image, bboxs_org, roi_rect, save_path)
        center = self.getCenter(bboxs_org)
        center[0] = max(min(center[0], width), 0)
        center[1] = max(min(center[1], height), 0)
        for center_sample_size_ratio in self.center_sample_size_ratio:
            width_unit = int(width * center_sample_size_ratio)
            height_unit = int(height * center_sample_size_ratio)
            roi_rect = [center[0] - width_unit // 2, center[1] - height_unit // 2, width_unit, height_unit]
            roi_rect = self.insect(fullimage_rect, roi_rect)
            center_width = roi_rect[0] + roi_rect[2] // 2
            center_height = roi_rect[1] + roi_rect[3] // 2
            for center_scale in self.center_scales:
                rect_width = int(roi_rect[2] * center_scale)
                rect_height = int(roi_rect[3] / center_scale)
                roi_rect = self.insect(fullimage_rect,
                                       [center_width - rect_width // 2, center_height - rect_height // 2,
                                        rect_width,
                                        rect_height])
                self.generate(image, bboxs_org, roi_rect, save_path)
        pass

    def getCenter(self, bboxs):
        center_x = 0
        center_y = 0
        for bbox in bboxs:
            center_x += bbox[0] + bbox[2] // 2
            center_y += bbox[1] + bbox[3] // 2
        return [center_x // len(bboxs), center_y // len(bboxs)]

    def generate(self, image, bboxs_org, roi_rect, save_path):
        x1, y1, w, h = roi_rect
        x2 = x1 + w
        y2 = y1 + h
        rect_width = w
        rect_height = h
        bboxs = []
        for i in range(len(bboxs_org)):
            tmp = self.insect(roi_rect, bboxs_org[i])
            bboxs.append([tmp[0] - x1, tmp[1] - y1, tmp[2], tmp[3], bboxs_org[i][-1]])

        image_sample = image[y1:y2, x1:x2, :]
        image_sample_copy = copy.deepcopy(image_sample)
        image_sample_name = self.prefix + str(self.start_index)
        bboxs = self.processImage(image_sample_copy, bboxs)
        if len(bboxs) > 0:
            with open(save_path + "//" + image_sample_name + '.txt', 'w') as txt:
                with open(save_path + '//' + image_sample_name + 'org.txt', 'w') as orgtxt:
                    for i in range(len(bboxs)):
                        orgtxt.write(
                            "{} {} {} {} {} {} {}\n".format(bboxs[i][-1], rect_width, rect_height, bboxs[i][0],
                                                            bboxs[i][1],
                                                            bboxs[i][2],
                                                            bboxs[i][3]))
                        txt.write(
                            "{} {} {} {} {}\n".format(bboxs[i][-1], (bboxs[i][0] + bboxs[i][2] / 2) / rect_width,
                                                      (bboxs[i][1] + bboxs[i][3] / 2) / rect_height,
                                                      bboxs[i][2] / rect_width, bboxs[i][3] / rect_height))
            # 写图片
            cv2.imwrite(save_path + "//" + image_sample_name + '.jpg', image_sample_copy)
            self.start_index += 1
        pass

    def insect(self, full_rect, bbox):
        x1 = min(max(full_rect[0], bbox[0]), full_rect[0] + full_rect[2])
        y1 = min(max(full_rect[1], bbox[1]), full_rect[1] + full_rect[3])

        x2 = max(min(full_rect[2] + full_rect[0], bbox[2] + bbox[0]), x1)
        y2 = max(min(full_rect[3] + full_rect[1], bbox[3] + bbox[1]), y1)

        return [x1, y1, x2 - x1, y2 - y1]

    # 处理图片
    def processImage(self, image, bboxs):
        flag = True
        bboxs_result = copy.deepcopy(bboxs)
        while flag:
            flag = False
            bboxs = bboxs_result
            bboxs_result = []
            for bbox in bboxs:
                if self.needDeleteSomeBBox(image, bbox):
                    flag = True
                    self.drawBlack(image, bbox)
                else:
                    bboxs_result.append(bbox)
        if len(bboxs_result) > 0 and self.needDeleteImage(image):
            bboxs_result = []
        return bboxs_result

    def needDeleteImage(self, image):
        total = 0
        threshold_total = self.image_black_threshold * image.shape[0] * image.shape[1]
        for x in range(0, image.shape[1]):
            for y in range(0, image.shape[0]):
                if image[y][x][0] <= self.black_threshold[0] and image[y][x][1] <= self.black_threshold[1] and \
                        image[y][x][2] <= self.black_threshold[2]:
                    total += 1
                    if total > threshold_total:
                        return True
        return False

    def isVaild(self, image, bbox):
        if bbox[0] < 0 or bbox[1] < 0 or bbox[0] + bbox[2] > image.shape[1] \
                or bbox[1] + bbox[3] > image.shape[0]:
            return False
        return True

    # 需要删除的bbox,返回true
    def needDeleteSomeBBox(self, image, bbox):
        if bbox[0] <= 0 or bbox[1] <= 0 or bbox[0] + bbox[2] >= image.shape[1] \
                or bbox[1] + bbox[3] >= image.shape[0]:
            return True
        total = 0
        threshold_total = self.bbox_black_threshold * bbox[2] * bbox[3]
        for x in range(max(bbox[0], 0), min(bbox[0] + bbox[2], image.shape[1])):
            for y in range(max(bbox[1], 0), min(bbox[1] + bbox[3], image.shape[0])):
                if image[y][x][0] <= self.black_threshold[0] and image[y][x][1] <= self.black_threshold[1] and \
                        image[y][x][2] <= self.black_threshold[2]:
                    total += 1
                    if total > threshold_total:
                        return True
        return False

    # 在box的区域上涂黑
    # box=[x,y,width,height]
    def drawBlack(self, image, bbox):
        for x in range(bbox[0], bbox[0] + bbox[2]):
            for y in range(bbox[1], bbox[1] + bbox[3]):
                image[y][x][0] = 0
                image[y][x][1] = 0
                image[y][x][2] = 0

    def isExist(self, dataPath, fileName):
        if os.path.isfile(os.path.join(dataPath, fileName)) and fileName.endswith('.jpg'):
            fileName = fileName[:-4]
            if os.path.isfile(os.path.join(dataPath, fileName + '.txt')) and os.path.isfile(
                    os.path.join(dataPath, fileName + 'org.txt')):
                return True
        return False


if __name__ == '__main__':
    PATH = [r'F:\PostGraduate\DataSet\LowPosition\train_add', ]
    SAVE_PATH = [r'F:\PostGraduate\DataSet\LowPosition\train_add\sample_add', ]
    sampler = Sampler(PATH, SAVE_PATH, start_index=16737, prefix='LP', bbox_black_threshold=0.4,
                      sample_size_ratio=(2, 2),
                      center_sample_size_ratio=[2 / 3, 3 / 4],
                      scales=[1, 3 / 4, 4 / 3],
                      center_scales=[1, 3 / 4, 4 / 3, 1 / 2, 2])
    sampler.startTask()
    pass
