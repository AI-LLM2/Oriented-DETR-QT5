import os

def remove_columns(input_file, output_file):
    """
    从输入文件中去除第九列和第十列，并将结果保存到输出文件。
    
    :param input_file: 输入的标签文件路径
    :param output_file: 输出的标签文件路径
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # 按空格分割每一行
            columns = line.strip().split(' ')
            # 去除第九列和第十列（索引为8和9）
            del columns[8:10]
            # 将剩余的列重新组合成一行，并写入输出文件
            outfile.write(' '.join(columns) + '\n')

def process_folder(input_folder, output_folder):
    """
    处理输入文件夹中的所有 .txt 文件，去除第九列和第十列，并将结果保存到输出文件夹。
    
    :param input_folder: 输入文件夹路径
    :param output_folder: 输出文件夹路径
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)
            remove_columns(input_file, output_file)
            print(f"Processed {filename}")

# 示例用法
input_folder = '/root/autodl-tmp/Oriented-DETR/data/OHD-SJTU/OHD-SJTU-S/test/labelTxt/'  # 替换为你的输入文件夹路径
output_folder = '/root/autodl-tmp/Oriented-DETR/data/OHD-SJTU/ohd/test/labels/'  # 替换为你的输出文件夹路径

process_folder(input_folder, output_folder)