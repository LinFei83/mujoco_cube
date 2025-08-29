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
# 格式化输出每个顶点的x, y, z坐标，保留6位有效数字
for vertex in mesh.vertices:
    print(f"{vertex[0]:.6g} {vertex[1]:.6g} {vertex[2]:.6g}")

# 确认立方体尺寸是否为0.019米
# 使用numpy的断言函数检查网格范围是否在三个维度上都等于0.019
np.testing.assert_equal(mesh.extents, [0.019] * 3)
