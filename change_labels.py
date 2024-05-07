import os
from pathlib import Path

def change_class_ids(directory):
    path = Path(directory)
    files = path.glob('*.txt')
    
    id_map = {
        0: 0,
        1: 0,
        2: 0,
        3: 1,
        4: 1,
        5: 1,
        6: 0
    }
    
    for file in files:
        with open(file, 'r') as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            parts = line.split()
            class_id = int(parts[0])
            if class_id in id_map:
                print(f"Original ID: {parts[0]} -> New ID: {id_map[class_id]}")  # 추가된 로그
                parts[0] = str(id_map[class_id])
            new_line = ' '.join(parts)
            new_lines.append(new_line)
        
        with open(file, 'w') as f:
            for line in new_lines:
                f.write(line + '\n')

# 사용 예시
directory = r"C:\Users\82107\Desktop\manga-bubble-detect.v2i.yolov5pytorch\test\labels"
change_class_ids(directory)
