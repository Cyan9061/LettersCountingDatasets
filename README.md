# LLMCountBench(Language Model Counting Benchmark Generator）)
*面向大模型测试的字母/单词计数数据集生成器*

## Motivation / 动机

Several recent papers (e.g., *Why Do Large Language Models (LLMs) Struggle to Count Letters?*, *The Case For Language Model Accelerated LIKE Predicate*) have highlighted that large language models face challenges when counting letter frequencies. For instance, experiments (late 2024) that involved counting the number of 'r's in "strawberry" caused significant issues for many LLMs. This motivated us to develop a dataset generator specifically designed for training and testing such capabilities.

最近的一些论文（例如 *Why Do Large Language Models (LLMs) Struggle to Count Letters?* 以及 *The Case For Language Model Accelerated LIKE Predicate*等）指出，大型语言模型在字母频率计数任务上存在困难。例如，2024 年底的一些民间实验中，统计 “strawberry” 中字母 ‘r’ 的数量就给许多模型带来了显著问题。这促使我们开发了一个专门用于训练和测试该能力的数据集生成器。

This tool generates datasets where each sample contains controlled-length texts with unique frequencies of a specified target substring.

该工具生成的数据集中，每个样本都是在受控文本长度内，包含目标子字符串的目标频率。

---

## Features / 特性

- **Compound Unit Generation**: Combines English words of varying lengths into compound units.(eg. elian_moskito_pbase_tlist_alexanderplatz_cityside)
- **Diverse Frequencies**: Ensures diversity in the target substring frequency across samples.
- **Controlled Text Length**: Avoids excessive text length inflation while preserving meaningful complexity.

- **复合单元生成**：通过组合不同长度的英语单词生成复合单元。(例如elian_moskito_pbase_tlist_alexanderplatz_cityside)
- **频率多样性**：确保样本中目标子字符串的频率具有多样性。
- **文本长度控制**：在保持文本复杂性的同时，避免文本长度过度膨胀。

---

## Algorithm Overview / 算法概览

1. **Word Loading / 单词加载**  
   - Reads the top `scan_max` most frequent English words from `count_1w.txt`.  
   - Precomputes the frequency of the target substring (`target_char`) for each word.  

   从 `count_1w.txt` 中读取前 `scan_max` 个最常见的英语单词，并预先计算每个单词中目标子字符串 (`target_char`) 的出现频率。

2. **Compound Unit Generation / 复合单元生成**  
   - Randomly selects between `min_words` and `max_words` words per iteration.  
   - Joins the selected words using underscores ("_") to form a compound unit.  
   - Computes the cumulative frequency of the target substring in the generated unit.

   每次迭代随机选择介于 `min_words` 和 `max_words` 之间的单词，并用下划线 ("_") 将它们连接成一个复合单元，同时计算该单元中目标子字符串的累计频率。

3. **Distinct Count Collection / 收集不同目标对象数目的复合单元**  
   - Continuously generates new compound units until achieving `target_distinct` unique target substring frequencies.  
   - Dynamically adjusts parameters if new unique frequencies are hard to obtain.

   持续生成新的复合单元，直到获得 `target_distinct` 个不同的目标子字符串频率；若新频率难以获取，则动态调整相关参数。

4. **Performance Monitoring / 性能监控**  
   - Logs progress every 1000 iterations.  
   - Terminates execution when either `target_distinct` unique counts are reached or the maximum allowed attempts (`max_attempts`) are exceeded.

   每 1000 次迭代记录一次进度，达到 `target_distinct` 个唯一计数或超过最大尝试次数 (`max_attempts`) 后终止执行。

---

## Complexity Analysis / 复杂度分析

### Time Complexity / 时间复杂度

- **Word Loading**: $O(\min(M, N))$  
  *M is the total number of lines in `count_1w.txt` and N is `scan_max`.*

- **Preprocessing Counts**: $O(N \cdot L)$  
  *L represents the average word length.*

- **Main Loop**: $O(T \cdot n)$  
  *T is the total number of iterations required to achieve `target_distinct` unique frequencies; n is the number of words chosen per iteration (ranging between `min_words` and `max_words`).*

总体时间复杂度为:  
$O(\min(M, N) + N \cdot L + T \cdot n)$

### Space Complexity / 空间复杂度

- **Word Storage**: $O(W)$  
- **Result Storage**: $O(D)$  
  *W is the space required for storing words, and D is the number of distinct frequency counts.*

---

## Project Structure / 项目结构

Below is an outline of the project directory structure:

下面是项目目录结构示例：

```
/LettersCountingDatasets/
├── GeneratedDatasets/         # Folder for generated CSV files.
│   ├── count_[TARGET_CHAR]_[DISTINCT].csv
│   └── ExcelOutputs/
│       └──count_[TARGET_CHAR]_[DISTINCT].xlsx      
├── Scripts/                   # Python scripts for the processing pipeline.
│   ├── dataset_generator.py   # Main script to generate compound units and counts.
│   ├── csv_to_excel.py        # Script to convert CSV files to Excel format.
│   └── count_letters.py       # Script for analyzing and displaying CSV results.
├── resources/                 # External resource files.
│   └── count_1w.txt           # File containing common English words.
└── README.md                  # This documentation file.
```

*Note*: Replace placeholders (e.g., `[TARGET_CHAR]`, `[DISTINCT]`) with actual configurations during testing.

注意：你需要用实际参数代替`[TARGET_CHAR]`, `[DISTINCT]`等参数。

---

## Usage Instructions / 使用说明

### Prerequisites / 先决条件

Ensure you have Python 3.x installed along with necessary libraries. Install required packages via pip:

确保安装 Python 3.x 和所需的库，使用以下命令安装：

```bash
pip install pandas openpyxl
```

### Running the Scripts / 运行脚本

1. **Clone the Repository / 克隆仓库**  
   ```bash
   git clone https://github.com/Cyan9061/LettersCountingDatasets.git
   ```

2. **Generate Datasets / 生成数据集**  
   Run the main script to generate compound units and save them as CSV files.(default:TARGET_CHAR = "r",TARGET_DISTINCT = 512)
   ```bash
   python ./Scripts/dataset_generator.py
   ```

3. **Convert CSV to Excel / 将 CSV 转换为 Excel**  
   Convert generated CSV files to Excel format.
   ```bash
   python ./Scripts/csv_to_excel.py
   ```

4. **Analyze Results / 分析结果**  
   Analyze and display the results from the CSV files. The default file is `count_r_512.csv`. To analyze a different file, modify the `filename` variable in `count_letters.py`.  
   Additionally, you can specify a different target character (e.g., 'r') by changing the `target_char` parameter in the function call:
   ```bash
   python ./Scripts/count_letters.py
   ```

5. **Review Outputs / 查看输出**  
   Check the generated CSV and Excel files in `/GeneratedDatasets` and `/GeneratedDatasets/ExcelOutputs`.

---

## Data Resource / 数据资源

The dataset is based on the original natural language corpus data:

数据基于以下原始自然语言语料库数据：

> Peter Norvig. 2009. Natural language corpus data. *Beautiful Data*, 219–242.

---

## License / 许可证

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

该项目采用 MIT 许可证 —— 详情请参阅 [LICENSE](LICENSE) 文件。
