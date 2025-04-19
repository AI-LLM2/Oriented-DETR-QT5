import json
import os
import cv2
import numpy as np
pi = 3.141592
def regular_theta(theta, mode='180', start=-pi/2):
    """
    limit theta ∈ [-pi/2, pi/2)
    """
    assert mode in ['360', '180']
    cycle = 2 * pi if mode == '360' else pi

    theta = theta - start
    theta = theta % cycle
    return theta + start

def poly2angle(poly):
    poly=np.array(poly)
    poly = np.float32(poly.reshape(4, 2))
    (x, y), (w, h), angle = cv2.minAreaRect(poly)  # θ ∈ [0， 90]
    angle = -angle  # θ ∈ [-90， 0]
    theta = angle / 180 * pi  # 转为pi制

    # trans opencv format to longedge format θ ∈ [-pi/2， pi/2]
    if w != max(w, h):
        w, h = h, w
        theta += pi / 2
    theta = regular_theta(theta)  # limit theta ∈ [-pi/2, pi/2)
    angle = (theta * 180 / pi) + 90  # θ ∈ [0， 180)
    return x, y, w, h, angle

def yolo2coco(image_dir_path, save_file_name):
    total = {}
    # add Class Names
    # DOTA 使用这个
    class_Names = ['plane', 'baseball-diamond', 'bridge', 'ground-track-field', 'small-vehicle',
        'large-vehicle', 'ship', 'tennis-court', 'basketball-court', 'storage-tank',
        'soccer-ball-field', 'roundabout', 'harbor', 'swimming-pool', 'helicopter']
        # 'container-crane']
    #dior 使用这个
    #class_Names = ['airplane', 'airport', 'baseballfield', 'basketballcourt', 'bridge', 'chimney',
    #            'dam', 'Expressway-Service-area', 'Expressway-toll-station', 'golffield', 'groundtrackfield', 
    #            'harbor', 'overpass', 'ship', 'stadium', 'storagetank', 'tenniscourt', 'trainstation', 'vehicle', 'windmill']
    
    count_ID = 1
    class_name2id = {}
    for id,name in enumerate(class_Names):
        class_name2id[name]=id+1
    # make categories
    category_list = []
    infoCoco = {'id': None, 'name': None, 'supercategory': 'None'}

    for elem in class_Names:
        infoCoco['id'] = count_ID
        infoCoco['name'] = elem
        category_list.append(infoCoco.copy())
        count_ID += 1

    total['categories'] = category_list

    image_list = os.listdir(image_dir_path)
    print('image length : ', len(image_list))
    #label_list = os.listdir(label_dir_path)
    #print('label length : ', len(label_list))
    print('Converting.........')
    image_dict_list = []
    label_dict_list = []
    count = 1
    num= 1
    label_count= 1
    for image_name in image_list:
        if image_name.endswith(".zip") or image_name.endswith(".json"):
            continue
        print(image_dir_path + image_name)
        img = cv2.imread(image_dir_path + image_name)
        # print(img.shape[1])

        image_dict = {
            'id': count,
            'file_name': image_name,
            'width': img.shape[1],
            'height': img.shape[0],
        }
        image_dict_list.append(image_dict)
        label_count += 1
        count += 1
        print("{} is ok".format(count))

    total['annotations'] = label_dict_list
    total['images'] = image_dict_list
    with open(save_file_name, 'w', encoding='utf-8') as make_file:
        json.dump(total, make_file, ensure_ascii=False, indent='\t')


if __name__ == '__main__':
    # 修改对应路径
    image_dir_path = "/root/autodl-tmp/Oriented-DETR/data/DOTA/DOTAV1_0_SS_SPLIT/test2017_split_rate1.0_subsize1024_gap200/images/"
    save_file_name = '/root/autodl-tmp/Oriented-DETR/data/DOTA/DOTA_SS_SPLIT_COCO/annotations/instances_test2017.json'

    yolo2coco(image_dir_path, save_file_name)