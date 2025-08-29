# -*- coding: utf-8 -*-
"""处理CAD网格以获取MuJoCo所需的顶点信息。"""

import trimesh
import numpy as np

# 加载STL文件中的网格数据
mesh = trimesh.load_mesh("cubelet.stl")

# 将网格尺寸从毫米缩放至米
mesh.apply_scale(0.001)

# 将网格中心平移至坐标原点
mesh.apply_translation(-mesh.centroid)

# 打印处理后的顶点坐标
print("顶点坐标:")
vertex_str = ""
for vertex in mesh.vertices:
    vertex_str += f"{vertex[0]:.6g} {vertex[1]:.6g} {vertex[2]:.6g} "
print(vertex_str.strip())

# 打印面信息（三角形面）
print("\n面信息:")
face_str = ""
for face in mesh.faces:
    face_str += f"{face[0]} {face[1]} {face[2]} "
print(face_str.strip())

print(f"\n顶点数量: {len(mesh.vertices)}")
print(f"面数量: {len(mesh.faces)}")

# 确认立方体尺寸是否为0.019米
# 使用numpy的断言函数检查网格范围是否在三个维度上都等于0.019
np.testing.assert_equal(mesh.extents, [0.019] * 3)
