import os
import xml.etree.ElementTree as ET

def convert_xml_to_txt(input_folder, output_folder):
    """
    将输入文件夹中的 XML 标注文件转换为文本格式的标注文件。
    :param input_folder: 包含 XML 标注文件的文件夹路径。
    :param output_folder: 转换后的 .txt 文件将保存到这个文件夹。
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历输入文件夹中的所有 XML 文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.xml'):
            xml_path = os.path.join(input_folder, filename)
            print(f'convert {filename}')

            try:
                # 解析 XML 文件
                tree = ET.parse(xml_path)
                root = tree.getroot()

                # 创建用于存储文本数据的列表
                text_data = []

                # 遍历 XML 元素并提取所需的信息
                for obj in root.findall('.//object'):
                    bndbox = obj.find('bndbox')
                    if bndbox is not None:
                        x0 = bndbox.find('x0').text
                        y0 = bndbox.find('y0').text
                        x1 = bndbox.find('x1').text
                        y1 = bndbox.find('y1').text
                        x2 = bndbox.find('x2').text
                        y2 = bndbox.find('y2').text
                        x3 = bndbox.find('x3').text
                        y3 = bndbox.find('y3').text
                        name = obj.find('name').text
                        difficult = obj.find('difficult').text

                        # 将提取的信息格式化并添加到文本数据列表中
                        text_line = f"{x0} {y0} {x1} {y1} {x2} {y2} {x3} {y3} {name} {difficult}\n"
                        text_data.append(text_line)

                # 创建输出文件路径
                output_path = os.path.join(output_folder, filename.replace('.xml', '.txt'))

                # 将文本数据写入输出文件
                with open(output_path, 'w') as output_file:
                    output_file.writelines(text_data)

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print("转换完成！")

# 输入文件夹路径和输出文件夹路径
input_folder = '/root/autodl-tmp/Oriented-DETR/data/OHD-SJTU/ohd/trainval/labelxml/'
output_folder = '/root/autodl-tmp/Oriented-DETR/data/OHD-SJTU/ohd2017/trainval/labels/'

# 调用函数进行转换
convert_xml_to_txt(input_folder, output_folder)