#!/usr/bin/env python3
"""创建一个 OBJ 格式的网格文件，用于 Isaac Sim 兼容性。"""

import trimesh
import numpy as np
from pathlib import Path

def create_obj_mesh():
    """从 STL 文件创建 OBJ 网格文件。"""
    # 加载 STL 文件
    mesh = trimesh.load_mesh("cubelet.stl")
    
    # 缩放和居中
    mesh.apply_scale(0.001)
    mesh.apply_translation(-mesh.centroid)
    
    # 导出为 OBJ 文件
    mesh.export("assets/cubelet.obj")
    print(f"已创建 OBJ 文件: assets/cubelet.obj")
    print(f"顶点数量: {len(mesh.vertices)}")
    print(f"面数量: {len(mesh.faces)}")
    
    # 验证尺寸
    np.testing.assert_equal(mesh.extents, [0.019] * 3)
    print("尺寸验证通过: 0.019m x 0.019m x 0.019m")

if __name__ == "__main__":
    create_obj_mesh()
