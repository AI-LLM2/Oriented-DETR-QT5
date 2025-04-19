import os
import shutil

# 源文件夹和目标文件夹路径
source_folder = '/root/autodl-tmp/Oriented-DETR/data/DIOR/dota_ann/'

trainval_target_folder = '/root/autodl-tmp/Oriented-DETR/data/DIOR/val2017/labelTxt/'
images_path = "/root/autodl-tmp/Oriented-DETR/data/DIOR/JPEGImages-trainval/"
target_image_dir = "/root/autodl-tmp/Oriented-DETR/data/DIOR/val2017/images/"

# 读取trainval.txt文件中的文件名列表
with open('/root/autodl-tmp/Oriented-DETR/data/DIOR/Main/val.txt', 'r') as file:
    file_names = file.read().splitlines()

# 遍历文件名列表并复制文件
total_trainval = 0
for file_name in file_names:
    source_file_path = os.path.join(source_folder, f"{file_name}.txt")
    target_file_path = os.path.join(trainval_target_folder, f"{file_name}.txt")
    

    # 使用shutil库进行文件复制
    if os.path.exists(source_file_path):
        total_trainval += 1
        shutil.copy(source_file_path, target_file_path)
        # print("->>",source_image_path)
        # print("->>",target_file_path)
        source_image_path = os.path.join(images_path, f"{file_name}.jpg")
        target_image_path = os.path.join(target_image_dir, f"{file_name}.jpg")
        shutil.copy(source_image_path, target_image_path)
        print(f"复制 {file_name}.txt 完成")
        
print("trainval 复制完成！")
