import shutil
import os

def copy_folder(source_folder, target_folder):
    """
    递归复制整个文件夹及其内容到目标文件夹。
    :param source_folder: 源文件夹路径
    :param target_folder: 目标文件夹路径
    """
    try:
        # 如果目标文件夹已经存在，先删除
        if os.path.exists(target_folder):
            shutil.rmtree(target_folder)
            print(f"已存在的目标文件夹 {target_folder} 已被删除。")

        # 复制整个文件夹及其内容
        shutil.copytree(source_folder, target_folder)
        print(f"文件夹 {source_folder} 已成功复制到 {target_folder}。")
    except FileNotFoundError:
        print(f"错误：源文件夹 {source_folder} 未找到。")
    except Exception as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    # 示例：将 source_folder 复制到 target_folder
    source_folder = "/root/autodl-tmp/Oriented-DETR/data/OHD-SJTU/ohd2017/test/"  # 源文件夹路径
    target_folder = "/root/autodl-tmp/Oriented-DETR/data/OHD-SJTU/ohdcoco/test2017/"  # 目标文件夹路径

    copy_folder(source_folder, target_folder)