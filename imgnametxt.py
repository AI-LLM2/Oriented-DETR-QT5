import os

# 设置文件夹路径
folder_path = '/root/autodl-tmp/Oriented-DETR/data/OHD-SJTU/ohdcoco/test2017/labels'
# 设置输出文件路径
output_file_path = '/root/autodl-tmp/Oriented-DETR/test.txt'

# 获取文件夹中的文件名
file_names = os.listdir(folder_path)

# 将文件名（不含后缀）写入txt文件
with open(output_file_path, 'w', encoding='utf-8') as f:
    for file_name in file_names:
        # 获取文件名（不含后缀）
        file_name_without_extension = os.path.splitext(file_name)[0]
        f.write(file_name_without_extension + '\n')

print(f'文件名（不含后缀）已保存到{output_file_path}')