import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys
import os

def visualize_layout(filename="layout_data.txt"):
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found.")
        return

    fig, ax = plt.subplots(figsize=(12, 10))
    
    color_map = {
        0: '#FF4500', # Elite (OrangeRed)
        1: '#FFD700', # Treasure (Gold)
        2: '#8A2BE2', # Trader (BlueViolet)
        3: '#00FF00', # Exit (Lime)
        4: '#808080', # Combat (Gray) - 普通房间
        5: '#00BFFF', # Start (DeepSkyBlue)
    }
    
    label_map = {
        0: 'Elite', 1: 'Treasure', 2: 'Trader', 
        3: 'Exit', 4: 'Normal', 5: 'Start'
    }

    # 用于计算整个图的边界，自动缩放
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')

    with open(filename, 'r') as f:
        lines = f.readlines()

    # 第一遍：绘制房间（矩形）
    for line in lines:
        parts = line.strip().split()
        if not parts: continue

        if parts[0] == 'R': # Room
            # 格式: R type minx miny maxx maxy
            rtype = int(parts[1])
            x1, y1 = float(parts[2]), float(parts[3])
            x2, y2 = float(parts[4]), float(parts[5])
            
            width = x2 - x1
            height = y2 - y1
            
            # 更新边界
            min_x = min(min_x, x1); min_y = min(min_y, y1)
            max_x = max(max_x, x2); max_y = max(max_y, y2)

            # 绘制矩形
            color = color_map.get(rtype, 'black')
            rect = patches.Rectangle((x1, y1), width, height, 
                                     linewidth=1, edgecolor='black', facecolor=color, alpha=0.6,
                                     label=label_map.get(rtype, 'Unknown'))
            ax.add_patch(rect)
            
            # 标记中心点
            cx, cy = x1 + width/2, y1 + height/2
            ax.text(cx, cy, label_map.get(rtype, '')[:2], ha='center', va='center', fontsize=8, color='white')

    # 第二遍：绘制路径（线条）
    for line in lines:
        parts = line.strip().split()
        if not parts: continue
        
        if parts[0] == 'P': # Path
            # 格式: P x1 y1 x2 y2 ...
            coords = list(map(float, parts[1:]))
            xs = coords[0::2] # 偶数索引是 X
            ys = coords[1::2] # 奇数索引是 Y
            
            # 绘制路径线
            ax.plot(xs, ys, color='black', linewidth=2, marker='.', markersize=4, alpha=0.7)
            
            # 更新边界以包含路径
            if xs:
                min_x = min(min_x, min(xs)); max_x = max(max_x, max(xs))
                min_y = min(min_y, min(ys)); max_y = max(max_y, max(ys))

    # 设置图例（去重）
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())

    # 设置坐标轴范围
    padding = 20
    ax.set_xlim(min_x - padding, max_x + padding)
    ax.set_ylim(min_y - padding, max_y + padding)
    
    ax.set_aspect('equal')
    plt.title("Dungeon Map Visualization")
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    
    output_img = "map_visualization.png"
    plt.savefig(output_img)
    print(f"Visualization saved to {output_img}")
    plt.show()

if __name__ == "__main__":
    visualize_layout()