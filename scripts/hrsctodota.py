import xml.etree.ElementTree as ET
import os
import math
import cv2
import numpy as np
def get_label(xml_path):
    in_file = open(xml_path)
    tree=ET.parse(in_file)
    root = tree.getroot()
    labels = []
    for obj in root.iter('HRSC_Object'):
        difficult = obj.find('difficult').text
        class_id = 0 # 标签对应关系自行修改
        mbox_cx, mbox_cy, mbox_w, mbox_h, mbox_ang = (
            float(obj.find('mbox_cx').text),
            float(obj.find('mbox_cy').text),
            float(obj.find('mbox_w').text),
            float(obj.find('mbox_h').text),
            float(obj.find('mbox_ang').text)
        )
        labels.append([class_id, mbox_cx, mbox_cy, mbox_w, mbox_h, mbox_ang, int(difficult)])
    return labels
# 计算旋转框四个顶点的坐标
def get_rotated_box_vertices(labels, label_path):
    """
    根据旋转框的中心点、宽度、高度和角度，计算旋转框的四个顶点坐标，
    并将结果保存到 TXT 文件中。
    """
    with open(label_path, 'w') as f:
        for i in range(len(labels)):
            class_id, mbox_cx, mbox_cy, mbox_w, mbox_h, angle_rad, difficult = labels[i]  # 包含 difficult
            rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                                        [np.sin(angle_rad), np.cos(angle_rad)]])
            box_half_width = mbox_w / 2
            box_half_height = mbox_h / 2
            box_vertices = np.array([[-box_half_width, -box_half_height],
                                     [box_half_width, -box_half_height],
                                     [box_half_width, box_half_height],
                                     [-box_half_width, box_half_height]])
            rotated_vertices = np.dot(box_vertices, rotation_matrix.T)
            rotated_vertices[:, 0] += mbox_cx
            rotated_vertices[:, 1] += mbox_cy
            rotated_vertices = np.round(rotated_vertices).astype(np.int32)
            rotated_vertices = rotated_vertices.reshape(-1)
            # 写入文件时包含 difficult
            f.write(" ".join([str(a) for a in rotated_vertices]) + " " + "ship" + " " + str(difficult) + '\n')


# 定义 XML 文件和 TXT 文件的根目录
xml_root = r"/root/autodl-tmp/Oriented-DETR/data/HRSC-2016/HRSC2016/Train/Annotations/"
txt_root = r"/root/autodl-tmp/Oriented-DETR/data/HRSC-2016/HRSC2016/HRSC_COCO/trainval2017/labels/"

# 获取 XML 文件夹中的所有文件名
xml_name = os.listdir(xml_root)

# 遍历每个 XML 文件并处理
for i in range(len(xml_name)):
    xml_path = os.path.join(xml_root, xml_name[i])  # 构造 XML 文件的完整路径
    txt_path = os.path.join(txt_root, xml_name[i].split('.')[0] + '.txt')  # 构造对应的 TXT 文件路径
    get_rotated_box_vertices(get_label(xml_path), txt_path)  # 调用函数处理并保存结果