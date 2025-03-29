import os
import glob
import pandas as pd
project_root = os.path.dirname(os.path.abspath(__file__))

# Define the directory containing generated datasets and the output directory for Excel files
# 定义包含生成数据集的目录和Excel文件的输出目录
generated_datasets_dir = os.path.join(project_root, "..", "GeneratedDatasets")
excel_output_dir = os.path.join(project_root, "..", "GeneratedDatasets/ExcelOutputs")

# Create the target folder if it does not exist
# 创建目标文件夹（如果不存在）
os.makedirs(excel_output_dir, exist_ok=True)

# Use relative paths to match CSV files
# 使用相对路径匹配CSV文件
for csv_path in glob.glob(os.path.join(generated_datasets_dir, "*.csv")):
    try:
        # Read the CSV file (automatically parse numbers)
        # 读取CSV文件（自动解析数值）
        df = pd.read_csv(csv_path)

        # Construct the output path
        # 构建输出路径
        base_name = os.path.basename(csv_path)
        excel_name = os.path.splitext(base_name)[0] + ".xlsx"
        excel_path = os.path.join(excel_output_dir, excel_name)

        # Save as Excel (force numeric types)
        # 保存为Excel（强制数值类型）
        df.to_excel(excel_path, index=False, engine="openpyxl")
        print(f"Converted {base_name} to Excel: {excel_name}")
    except Exception as e:
        print(f"Error processing file {csv_path}: {e}")

print(f"All CSV files converted! Files saved in: {excel_output_dir}")