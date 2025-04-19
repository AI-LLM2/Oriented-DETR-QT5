import os
import shutil

def merge_folders(source_folders, target_folder):
    """
    将多个源文件夹的内容合并到一个目标文件夹中。
    :param source_folders: 源文件夹列表
    :param target_folder: 目标文件夹路径
    """
    # 确保目标文件夹存在
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 遍历每个源文件夹
    for source_folder in source_folders:
        if not os.path.exists(source_folder):
            print(f"警告：源文件夹 {source_folder} 不存在，跳过。")
            continue

        # 遍历源文件夹中的所有文件和子文件夹
        for root, dirs, files in os.walk(source_folder):
            # 计算目标路径
            relative_path = os.path.relpath(root, source_folder)
            target_path = os.path.join(target_folder, relative_path)

            # 如果目标路径不存在，创建它
            if not os.path.exists(target_path):
                os.makedirs(target_path)

            # 复制文件
            for file in files:
                source_file_path = os.path.join(root, file)
                target_file_path = os.path.join(target_path, file)

                # 如果目标文件已存在，可以选择跳过或覆盖
                if os.path.exists(target_file_path):
                    print(f"警告：目标文件 {target_file_path} 已存在，跳过。")
                    continue

                shutil.copy2(source_file_path, target_file_path)  # copy2 保留元数据

    print(f"所有文件已成功合并到 {target_folder}。")


if __name__ == "__main__":
    # 定义源文件夹和目标文件夹
    source_folders = [
        "/root/autodl-tmp/Oriented-DETR/data/DOTA/DOTAV1_0_SS_SPLIT/train2017_split_rate1.0_subsize1024_gap200",
        "/root/autodl-tmp/Oriented-DETR/data/DOTA/DOTAV1_0_SS_SPLIT/val2017_split_rate1.0_subsize1024_gap200"
    ]
    target_folder = "/root/autodl-tmp/Oriented-DETR/data/DOTA/DOTAV1_0_SS_SPLIT/trainval2017_split_rate1.0_subsize1024_gap200"

    # 合并文件夹
    merge_folders(source_folders, target_folder)