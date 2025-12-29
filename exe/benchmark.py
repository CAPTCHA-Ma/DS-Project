import subprocess
import statistics
import time
import sys
import os


EXE_PATH = "DS_Project.exe" 
RUN_COUNT = 1000

def run_benchmark():
    print(f"--- 开始性能基准测试 ---")
    print(f"目标程序: {EXE_PATH}")
    print(f"计划运行次数: {RUN_COUNT}")
    print("-" * 40)

    data_tree = []
    data_force = []
    data_astar = []
    data_total = []

    successful_runs = 0
    
    start_time = time.time()

    for i in range(1, RUN_COUNT + 1):
        try:
            # 调用 C++ 程序，传入 "bench" 参数
            # capture_output=True 捕获 stdout
            # text=True 将输出作为字符串处理
            result = subprocess.run([EXE_PATH, "bench"], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"[Error] 第 {i} 次运行失败，返回码: {result.returncode}")
                continue

            # 获取输出并去除空白符
            output = result.stdout.strip()
            
            # 解析 CSV (tree, force, astar, total)
            parts = output.split(',')
            if len(parts) != 4:
                print(f"[Warn] 第 {i} 次运行输出格式错误: {output}")
                continue

            # 将字符串转换为浮点数
            t_tree = float(parts[0])
            t_force = float(parts[1])
            t_astar = float(parts[2])
            t_total = float(parts[3])

            data_tree.append(t_tree)
            data_force.append(t_force)
            data_astar.append(t_astar)
            data_total.append(t_total)
            
            successful_runs += 1

            # 显示简略进度
            if i % 10 == 0:
                sys.stdout.write(f"\r进度: {i}/{RUN_COUNT} | 最近一次总耗时: {t_total:.2f}ms")
                sys.stdout.flush()

        except FileNotFoundError:
            print(f"\n[Fatal Error] 找不到文件: {EXE_PATH}")
            print("请确保你已经编译了C++代码，并且exe文件在当前目录下。")
            return
        except Exception as e:
            print(f"\n[Error] 发生异常: {e}")
            return

    total_real_time = time.time() - start_time
    print(f"\n\n--- 测试完成 (实际耗时: {total_real_time:.2f}s) ---")
    print(f"成功样本数: {successful_runs}/{RUN_COUNT}")

    if successful_runs == 0:
        print("没有成功获取任何数据。")
        return

    # 计算统计数据
    print("\n" + "="*50)
    print(f"{'阶段':<20} | {'平均耗时 (ms)':<12} | {'最小 (ms)':<10} | {'最大 (ms)':<10}")
    print("-" * 50)
    
    def print_row(name, data):
        avg_val = statistics.mean(data)
        min_val = min(data)
        max_val = max(data)
        print(f"{name:<20} | {avg_val:<12.4f} | {min_val:<10.2f} | {max_val:<10.2f}")

    print_row("1. 树结构生成", data_tree)
    print_row("2. 力导向模拟", data_force)
    print_row("3. 走廊生成 (A*)", data_astar)
    print("-" * 50)
    print_row(">>> 总生成时间", data_total)
    print("="*50)

if __name__ == "__main__":
    run_benchmark()