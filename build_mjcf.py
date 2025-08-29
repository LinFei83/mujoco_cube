"""构建一个 3x3 魔方的 MJCF 模型。"""

import itertools
from typing import Sequence
from dm_control import mjcf
from mujoco import viewer
from pathlib import Path
from lxml import etree
import re


# ================================ #
# 全局常量
# ================================ #
SAVE_DIR = Path(__file__).parent  # 定义保存模型的目录为当前文件所在目录
NAME = "Cube 3x3x3"  # 模型名称
XML_NAME = "cube_3x3x3.xml"  # 输出的 XML 文件名
PRECISION = 6  # XML 文件中浮点数的精度
ZERO_THRESHOLD = 1e-6  # 零值阈值，小于此值的浮点数将被视为零
ADD_ACTUATORS = True  # 是否添加执行器（马达）


def build() -> mjcf.RootElement:
    """构建魔方 MJCF 模型。"""
    root = mjcf.RootElement()
    root.model = NAME

    # ================================ #
    # 常量定义
    # ================================ #
    cube_mass = 0.0685  # 整个魔方的总质量（单位：千克）
    cubelet_dimension = 0.019  # 每个小方块的尺寸（单位：米）
    # 通过 `process_mesh.py` 脚本获取的小方块顶点坐标
    cubelet_vertices = """
        0.008075 0.0095 -0.008075
        -0.008075 0.0095 -0.008075
        0.008075 0.0095 0.008075
        -0.008075 0.0095 0.008075
        -0.0095 0.008075 -0.008075
        -0.0095 -0.008075 -0.008075
        -0.0095 0.008075 0.008075
        -0.0095 -0.008075 0.008075
        0.008075 -0.0095 -0.008075
        0.008075 -0.0095 0.008075
        -0.008075 -0.0095 -0.008075
        -0.008075 -0.0095 0.008075
        0.0095 0.008075 0.008075
        0.0095 -0.008075 0.008075
        0.0095 0.008075 -0.008075
        0.0095 -0.008075 -0.008075
        0.008075 0.008075 0.0095
        -0.008075 0.008075 0.0095
        0.008075 -0.008075 0.0095
        -0.008075 -0.008075 0.0095
        0.008075 -0.008075 -0.0095
        -0.008075 -0.008075 -0.0095
        0.008075 0.008075 -0.0095
        -0.008075 0.008075 -0.0095
    """
    axes = ("pX", "nX", "pY", "nY", "pZ", "nZ")  # 定义六个轴向：正X、负X、正Y、负Y、正Z、负Z
    # ================================ #

    # ================================ #
    # 编译器设置
    # ================================ #
    root.compiler.autolimits = True  # 自动设置关节限制
    root.compiler.angle = "radian"  # 角度单位为弧度
    root.compiler.texturedir = "assets"  # 纹理文件目录
    # ================================ #

    # ================================ #
    # 内存设置
    # ================================ #
    root.size.memory = "600K"  # 分配 600K 内存
    # ================================ #

    # ================================ #
    # 仿真选项设置
    # ================================ #
    root.option.timestep = 0.01  # 仿真步长
    root.option.integrator = "implicitfast"  # 使用快速隐式积分器
    # ================================ #

    # ================================ #
    # 渲染设置
    # ================================ #
    root.visual.headlight.diffuse = (0.6, 0.6, 0.6)  # 头灯的漫反射光
    root.visual.headlight.ambient = (0.3, 0.3, 0.3)  # 头灯的环境光
    root.visual.headlight.specular = (0, 0, 0)  # 头灯的镜面反射光
    getattr(root.visual, "global").azimuth = 180  # 全局视角的方位角
    getattr(root.visual, "global").elevation = -20  # 全局视角的仰角
    root.statistic.extent = 0.1  # 统计范围
    root.statistic.meansize = 0.0087  # 平均尺寸
    # ================================ #

    # ================================ #
    # 默认值设置
    # ================================ #
    root.default.geom.mass = cube_mass / 27  # 设置每个小方块的默认质量
    # 为小方块创建一个默认类
    cubelet_default = root.default.add("default", dclass="cubelet")
    cubelet_default.geom.type = "mesh"  # 几何体类型为网格
    cubelet_default.geom.mesh = "cubelet"  # 网格名称
    cubelet_default.geom.quat = (1, 0, 0, 1)  # 四元数表示的姿态
    cubelet_default.geom.condim = 1  # 接触维度
    cubelet_default.joint.type = "ball"  # 关节类型为球形关节
    cubelet_default.joint.armature = 1e-4  # 关节的电枢惯性
    cubelet_default.joint.damping = 5e-4  # 关节的阻尼
    cubelet_default.joint.frictionloss = 1e-3  # 关节的摩擦损失
    if ADD_ACTUATORS:
        root.default.motor.ctrlrange = (-0.05, 0.05)  # 如果添加执行器，设置默认的控制范围
    core_default = root.default.add("default", dclass="core")  # 为核心创建一个默认类
    core_default.geom.type = "sphere"  # 核心的几何体类型为球体
    core_default.geom.size = (0.01,)  # 核心的尺寸
    core_default.geom.contype = 0  # 接触类型
    core_default.geom.conaffinity = 0  # 接触亲和度
    core_default.geom.group = "4"  # 几何体组
    # ================================ #

    # ================================ #
    # 资源定义
    # ================================ #
    # 添加小方块的网格资源
    root.asset.add("mesh", name="cubelet", vertex=cubelet_vertices)
    # 添加天空盒纹理
    root.asset.add(
        "texture", type="skybox", builtin="gradient", height=512, width=512
    )

    # 颜色与方向的映射关系
    color2dir = {
        "white": "pZ",
        "yellow": "nZ",
        "red": "pX",
        "orange": "nX",
        "blue": "pY",
        "green": "nY",
    }
    dir2color = {v: k for k, v in color2dir.items()}  # 方向与颜色的映射关系
    # 方向与魔方面（Face）的映射关系
    dir2face = {
        "pX": "D",  # Down
        "nX": "U",  # Up
        "pY": "R",  # Right
        "nY": "L",  # Left
        "pZ": "F",  # Front
        "nZ": "B",  # Back
    }

    # 为单色面创建纹理和材质
    for color in color2dir:
        root.asset.add(
            "texture",
            file=f"{color}.png",
            gridsize="3 4",
            gridlayout=f".....{dir2face[color2dir[color]]}......",
            rgb1=(0, 0, 0),
        )
        root.asset.add("material", name=color, texture=color)

    # 为双色面（棱块）创建纹理和材质
    for color1, color2 in itertools.combinations(color2dir.keys(), 2):
        color1, color2 = sorted([color1, color2])
        # 过滤掉相对的面（如白和黄）
        if color1 == "white" and color2 == "yellow":
            continue
        if color1 == "red" and color2 == "orange":
            continue
        if color1 == "blue" and color2 == "green":
            continue
        root.asset.add(
            "texture",
            file=f"{color1}_{color2}.png",
            gridsize="3 4",
            gridlayout=(
                f".....{dir2face[color2dir[color1]]}"
                f"{dir2face[color2dir[color2]]}....."
            ),
            rgb1=(0, 0, 0),
        )
        root.asset.add(
            "material", name=f"{color1}_{color2}", texture=f"{color1}_{color2}"
        )

    # 为三色面（角块）创建纹理和材质
    for comb in itertools.combinations(color2dir.keys(), 3):
        # 过滤掉包含相对面的组合
        if "white" in comb and "yellow" in comb:
            continue
        if "red" in comb and "orange" in comb:
            continue
        if "blue" in comb and "green" in comb:
            continue
        color1, color2, color3 = sorted(comb)
        root.asset.add(
            "texture",
            file=f"{color1}_{color2}_{color3}.png",
            gridsize="3 4",
            gridlayout=(
                f".....{dir2face[color2dir[color1]]}"
                f"{dir2face[color2dir[color2]]}"
                f"{dir2face[color2dir[color3]]}...."
            ),
            rgb1=(0, 0, 0),
        )
        root.asset.add(
            "material",
            name=f"{color1}_{color2}_{color3}",
            texture=f"{color1}_{color2}_{color3}",
        )
    # ================================ #

    def dir2axis(d: str) -> Sequence[float]:
        s = -1 if d[0] == "n" else 1
        if d[1] == "X":
            return (s, 0, 0)
        elif d[1] == "Y":
            return (0, s, 0)
        elif d[1] == "Z":
            return (0, 0, s)
        else:
            raise ValueError(f"无效的方向: {d}")

    def dir2pos(ds: str) -> Sequence[float]:
        """根据方向字符串计算小方块的位置。"""
        p = [0.0] * 3
        for d in ds.split("_"):
            p = [p[i] + cubelet_dimension * a for i, a in enumerate(dir2axis(d))]
        return tuple(p)

    # ================================ #
    # 世界实体（Worldbody）定义
    # ================================ #
    root.worldbody.add("light", pos=(0, 0, 1))  # 添加一个光源

    # 添加核心实体
    core = root.worldbody.add("body", name="core", childclass="cubelet")
    core.add("geom", dclass="core")  # 为核心添加几何体

    # 创建中心块 (6个)
    for d in axes:
        body = core.add("body", name=d)
        body.add("joint", name=d, type="hinge", axis=dir2axis(d))  # 添加铰链关节
        if ADD_ACTUATORS:
            root.actuator.add("motor", name=dir2color[d], joint=d)  # 添加马达
        body.add(
            "geom", name=f"cubelet_{d}", material=dir2color[d], pos=dir2pos(d)
        )

    # 创建棱块 (12个)
    for d1, d2 in list(itertools.combinations(axes, 2)):
        if d1[1] == d2[1]:
            continue
        d = "_".join(sorted([d1, d2]))
        body = core.add("body", name=d)
        body.add("joint", name=d)  # 添加球形关节（默认）
        mat = "_".join(sorted([dir2color[d1], dir2color[d2]]))
        body.add("geom", name=f"cubelet_{d}", material=mat, pos=dir2pos(d))

    # 创建角块 (8个)
    for d1, d2, d3 in list(itertools.combinations(axes, 3)):
        if d1[1] == d2[1] or d1[1] == d3[1] or d2[1] == d3[1]:
            continue
        d = "_".join(sorted([d1, d2, d3]))
        body = core.add("body", name=d)
        body.add("joint", name=d)  # 添加球形关节（默认）
        mat = "_".join(sorted([dir2color[d1], dir2color[d2], dir2color[d3]]))
        body.add("geom", name=f"cubelet_{d}", material=mat, pos=dir2pos(d))
    # ================================ #

    return root


def prettify_xml_string(xml_string: str) -> str:
    """美化和清理 XML 字符串。"""
    root = etree.XML(xml_string, etree.XMLParser(remove_blank_text=True))

    # 确保 compiler 的 texturedir 属性正确设置
    compiler = root.find("compiler")
    compiler.set("texturedir", "assets")

    # 修正纹理文件路径
    pattern = r"^[a-zA-Z]+(_[a-zA-Z]+)*-\w+\.png"
    textures = root.findall(".//texture")
    for texture in textures:
        for attr, file_name in texture.attrib.items():
            match = re.match(pattern, file_name)
            if match:
                color = match.group(0).split("-")[0]
                texture.set(attr, f"{color}.png")
        # 移除自动生成的纹理名称
        if "name" in texture.attrib:
            texture.attrib.pop("name")

    # 移除自动生成的名称
    for light in root.findall(".//light"):
        light.attrib.pop("name")
    for geom in root.findall(".//geom"):
        if "name" in geom.attrib:
            geom.attrib.pop("name")

    # 移除根默认类 "/"
    default_elem = root.find("default").find(".//*[@class='/']")
    for child in default_elem.iterchildren():
        default_elem.getparent().append(child)
    default_elem.getparent().remove(default_elem)

    # 重新排序资源元素：纹理、材质、网格
    asset = root.find("asset")
    textures = asset.findall(".//texture")
    materials = asset.findall(".//material")
    meshes = asset.findall(".//mesh")
    asset.clear()
    for texture in textures:
        asset.append(texture)
    for material in materials:
        asset.append(material)
    for mesh in meshes:
        asset.append(mesh)

    # TODO(kevin): 研究如何在节与节之间添加换行符。

    # 返回美化后的 XML 字符串
    return etree.tostring(root, pretty_print=True).replace(b' class="/"', b"").decode()


def main() -> None:
    """主函数，构建模型，生成 XML 文件，并启动查看器。"""
    model = build()
    xml_string = model.to_xml_string(
        precision=PRECISION, zero_threshold=ZERO_THRESHOLD
    )
    pretty_xml_string = prettify_xml_string(xml_string)

    # 将生成的 XML 字符串写入文件
    with open(SAVE_DIR / XML_NAME, "w") as f:
        f.write(pretty_xml_string)

    # 启动 MuJoCo 查看器加载模型
    viewer.launch_from_path(str(SAVE_DIR / XML_NAME))


if __name__ == "__main__":
    main()
