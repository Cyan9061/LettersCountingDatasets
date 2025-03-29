import csv
import random
import time

# 设置随机种子以保证结果可复现
random.seed(42)

# 用户定义参数
TARGET_CHAR = "r"  # Modify here for the target counting object, e.g., "r", "ing".
SCAN_MAX = 333333  # Default scanning up to 100k lines; total of 333333 lines.
TARGET_DISTINCT = 512  # Collect TARGET_DISTINCT different counts.

"""
Motivation:
不少论文（例如 Why Do Large Language Models (LLMs) Struggle to Count Letters?，The Case For Language Model Accelerated LIKE predicate 等）指出大模型在统计字母数量方面存在难点。前些时间（2024年底）的“strawberry”中'r'数量统计实验也让很多大模型翻车。于是制作了面向大模型字母或短语统计的数据集生成程序。也可以适配其他的例如排序等任务。
"""


def generate_compound_units(target_char, scan_max=100000, target_distinct=64, min_words=5, max_words=500):
    """
    From a text file, generate compound units and count occurrences of the target character/string.

    从文本文件中生成整体单元（或者叫做复合单元），并统计目标字符/字符串出现的次数。

    :param target_char: Required. The target character or string to count.
                         必需。要统计的目标字符或字符串。
    :param scan_max: Maximum number of lines to scan, default is 100000.
                      扫描的最大行数，默认为100000。
    :param target_distinct: Number of distinct counts to collect, default is 64.
                             目标收集的不同计数值数量，默认为64。
    :param min_words: Minimum number of words in each compound unit, default is 5.
                       每个整体单元最少包含的单词数，默认为5。
    :param max_words: Maximum number of words in each compound unit, default is 500.
                       每个整体单元最多包含的单词数，默认为500。
    :return: A list containing compound units and their corresponding counts.
             包含整体单元及其对应计数值的列表。
    """

    def count_target(text, target=target_char):
        """Count occurrences of the target character/string in the given text (case-sensitive)."""
        return text.count(target)

    def compound_unit(word_list, word_counts, min_n=min_words, max_n=max_words):
        """
        Randomly select between min_n and max_n words from the word list, join them with underscores to form a compound unit.

        随机选择 min_n 到 max_n 个单词，并用下划线连接形成一个整体单元（或者叫做复合单元）。
        """
        n = random.randint(min_n, max_n)
        selected_indices = random.choices(range(len(word_list)), k=n)  # Allow repeated sampling
        selected_words = [word_list[i] for i in selected_indices]
        t_count = sum(word_counts[i] for i in selected_indices)
        unit = "_".join(selected_words)
        return unit, t_count

    # Step 1: Load the word list and precompute the occurrence count of the target character/string for each word.
    # 加载单词表并预计算每个单词中目标字符/字符串的出现次数。
    words = []
    word_counts = []
    try:
        with open("../ResourceData/count_1w.txt", "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= scan_max:
                    break
                parts = line.strip().split("\t")
                if parts:
                    word = parts[0]
                    words.append(word)
                    word_counts.append(count_target(word))
    except FileNotFoundError:
        raise Exception("File 'count_1w.txt' not found. Please verify the file path!")

    if not words:
        raise ValueError("No valid words loaded. Please check the input file content.")

    # Step 2: Start generating compound units and collecting statistics.
    # 开始生成整体单元（或者叫做复合单元）并统计数据。
    distinct_units = {}  # {target_count: compound_unit}
    seen_counts = set()  # Used to accelerate checking whether a specific count exists.
    iterations = 0
    max_attempts = 1e7  # Maximum attempts allowed before stopping.
    no_new_count_streak = 0  # Counter for consecutive failures to find new counts.

    while len(distinct_units) < target_distinct and iterations < max_attempts:
        iterations += 1

        # Generate a new unit.
        # 生成新单元。
        unit, t_count = compound_unit(words, word_counts, min_words, max_words)

        # If a new count is found, save it.
        # 如果发现新的计数值，则保存它。
        if t_count not in seen_counts:
            distinct_units[t_count] = unit
            seen_counts.add(t_count)
            print(
                f"[INFO] Found new '{target_char}' count {t_count}, currently collected {len(distinct_units)} / {target_distinct}"
            )
            no_new_count_streak = 0  # Reset failure streak counter.
        else:
            no_new_count_streak += 1

        # Dynamically adjust parameters if too many consecutive failures occur.
        # 如果连续多次未能找到新计数值，则动态调整参数。
        if no_new_count_streak > 1000:
            min_words = max(2, min_words - 1)
            max_words = min(max_words + 1, SCAN_MAX)
            no_new_count_streak = 0
            print(
                f"[ADJUST] Adjusted parameters due to lack of new counts: min_words={min_words}, max_words={max_words}")

        # Print progress every 1000 iterations.
        # 每处理1000次打印进度信息。
        if iterations % 1000 == 0:
            print(f"[PROGRESS] Attempted {iterations} times, current distinct counts: {len(distinct_units)}")

    print(
        f"\nTotal attempts: {iterations}, successfully collected {len(distinct_units)} distinct '{target_char}' counts.\n")

    return [(unit, t_count) for t_count, unit in distinct_units.items()]


# Example usage
if __name__ == "__main__":
    # Record start time
    # 记录开始时间
    start_time = time.time()

    # Call main function
    # 调用主函数
    result = generate_compound_units(
        target_char=TARGET_CHAR,
        scan_max=SCAN_MAX,
        target_distinct=TARGET_DISTINCT,
        min_words=5,
        max_words=500
    )

    # Record end time
    # 记录结束时间
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Write results to CSV file
    # 将结果写入CSV文件
    OUTPUT_FILENAME = f"./GeneratedDatasets/count_{TARGET_CHAR}_{TARGET_DISTINCT}.csv"
    with open(OUTPUT_FILENAME, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["compound_unit", f"{TARGET_CHAR}_count"])  # Header row
        for unit, t_count in result:
            writer.writerow([unit, t_count])

    print(f"Generated file {OUTPUT_FILENAME}, containing {len(result)} distinct '{TARGET_CHAR}' counts.")
    print(f"Program runtime: {elapsed_time:.2f} seconds")