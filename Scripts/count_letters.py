import csv
import os
import re
#修改这个文件名
#modify this file_name
file_name = 'count_r_512.csv'

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
default_filename = os.path.join(script_dir, '..', 'GeneratedDatasets', file_name)

def extract_str_from_filename(file_name):
    match = re.match(r"count_([a-zA-Z]+)_\d+\.csv", file_name)
    if match:
        return match.group(1)
    return None  # 如果格式不匹配，返回 None



def count_substring(unit, target_char):
    """
    Counts the occurrences of a specific substring in a given unit.

    :param unit: The compound unit string.
                 整体单元字符串。
    :param target_char: The target substring to count.
                        需要计数的目标子字符串。
    :return: The count of the target substring in the unit.
             单元中目标子字符串的计数。
    """
    return unit.count(target_char)

def count_letters(filename, target_char='ing'):
    """
    Reads a CSV file containing compound units and their corresponding letter counts,
    then finds and prints the unit with the maximum count of a specific substring (target_char)
    and all units sorted by this count.

    读取包含整体单元及其对应字母计数的CSV文件，
    然后找到并打印指定子字符串(target_char)计数最高的整体单元以及所有按计数从高到低排序的整体单元。

    :param filename: Path to the input CSV file.
                     输入CSV文件的路径。
    :param target_char: The target substring to count.
                        需要计数的目标子字符串。
    """
    units = []

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                unit = row['compound_unit']
                # 计算目标子字符串出现的次数
                char_count = count_substring(unit, target_char)
                units.append((unit, char_count))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        return

    if not units:
        print("No valid data found in the file.")
        return

    # Find the unit with the maximum count of the target substring
    # 找到目标子字符串计数最高的整体单元
    max_unit = max(units, key=lambda x: x[1])
    print(f"Unit with the highest '{target_char}' count:")
    print(f"Compound Unit: {max_unit[0]}, '{target_char}' Count: {max_unit[1]}")

    print(f"\nAll units and their '{target_char}' counts (sorted from high to low):")
    for i, (unit, char_count) in enumerate(sorted(units, key=lambda x: x[1], reverse=True), start=1):
        print(f"{i}. '{target_char}' Count: {char_count}, Compound Unit: {unit}")

if __name__ == "__main__":
    target_char = extract_str_from_filename(file_name)
    count_letters(default_filename,target_char)