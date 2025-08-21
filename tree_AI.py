import tkinter as tk
from tkinter import messagebox
X = [
    [1, 0, 0],  #tâm trạng, thời tiết, sức khỏe
    [1, 1, 0],  
    [1, 0, 1],  
    [0, 0, 1],  
    [0, 1, 0],  
]
y = [1, 1, 0, 0, 0]

def best_split(X, y):
    best_attr = None
    best_score = -1
    n_features = len(X[0])

    for attr in range(n_features):
        groups = {}
        for i, row in enumerate(X):
            v = row[attr]
            if v not in groups:
                groups[v] = []
            groups[v].append(y[i])

        # Điểm = tổng số nhóm có cùng nhãn
        score = sum(1 for labels in groups.values() if len(set(labels)) == 1)

        if score > best_score:
            best_score = score
            best_attr = attr

    return best_attr

def build_tree(X, y):
    if len(set(y)) == 1:
        return y[0]  
    if len(X[0]) == 0:
        return max(set(y), key=y.count) 

    attr = best_split(X, y)
    if attr is None:
        return max(set(y), key=y.count)

    tree = {attr: {}}
    values = set(row[attr] for row in X)
    for v in values:
        X_sub = [row[:attr] + row[attr+1:] for i, row in enumerate(X) if row[attr] == v]
        y_sub = [y[i] for i, row in enumerate(X) if row[attr] == v]
        tree[attr][v] = build_tree(X_sub, y_sub)
    return tree



def predict(tree, sample):
    if not isinstance(tree, dict):
        return tree
    
    # Lấy thuộc tính gốc của nút
    attr = next(iter(tree))  
    
    # Lấy giá trị của sample tại thuộc tính đó
    v = sample[attr]
    
    # Nếu có nhánh đúng giá trị thì đi tiếp
    if v in tree[attr]:
        return predict(tree[attr][v], sample)
    return None

tree = build_tree(X, y)
print("Cây học được:", tree)
print(predict(tree, [1, 1, 0])) 
print(predict(tree, [1, 0, 1]))

root = tk.Tk()
root.title("Có nên đi học không?")
root.geometry("420x260")

mood_var = tk.IntVar(value=1)      
weather_var = tk.IntVar(value=0)   
health_var = tk.IntVar(value=0)

frame = tk.Frame(root, padx=12, pady=12)
frame.pack(fill=tk.BOTH, expand=True)

# Tâm trạng
tk.Label(frame, text="Tâm trạng:").grid(row=0, column=0, sticky='w')
tk.Radiobutton(frame, text="Tốt (0)", variable=mood_var, value=1).grid(row=0, column=1)
tk.Radiobutton(frame, text="Xấu (1)", variable=mood_var, value=0).grid(row=0, column=2)

# Thời tiết
tk.Label(frame, text="Thời tiết:").grid(row=1, column=0, sticky='w')
tk.Radiobutton(frame, text="Nắng (0)", variable=weather_var, value=0).grid(row=1, column=1)
tk.Radiobutton(frame, text="Mưa (1)", variable=weather_var, value=1).grid(row=1, column=2)

# Sức khỏe
tk.Label(frame, text="Sức khỏe:").grid(row=2, column=0, sticky='w')
tk.Radiobutton(frame, text="Khỏe (0)", variable=health_var, value=0).grid(row=2, column=1)
tk.Radiobutton(frame, text="Mệt (1)", variable=health_var, value=1).grid(row=2, column=2)

result_label = tk.Label(frame, text="Kết quả: (chưa có)", font=(None, 12, 'bold'))
result_label.grid(row=4, column=0, columnspan=3, pady=12)

def on_decide():
    sample = [mood_var.get(), weather_var.get(), health_var.get()]
    res = predict(tree, sample)
    if res is None:
        result_text = "Không rõ (dữ liệu không đủ)"
    else:
        result_text = "Đi học" if res == 1 else "Nghỉ học"
    result_label.config(text=f"Kết quả: {result_text}")

btn = tk.Button(frame, text="Quyết định", command=on_decide)
btn.grid(row=3, column=0, columnspan=3, pady=6)

root.mainloop()




