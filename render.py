# 导入所需的库
from dm_control import mjcf, mujoco  # dm_control 用于与 MuJoCo 物理引擎交互
from PIL import Image  # PIL (Pillow) 用于图像处理

# 设置渲染分辨率
res = (480, 640)  # 定义渲染图像的尺寸 (高度, 宽度)

# 指定模型文件路径
xml_file = "cube_3x3x3.xml"

# 从 XML 文件加载 MJCF 模型
model = mjcf.from_path(xml_file)

# 确保离屏渲染缓冲区的大小支持所需的分辨率
# 这对于生成正确尺寸的图像至关重要
getattr(model.visual, "global").offheight = res[0]
getattr(model.visual, "global").offwidth = res[1]

# 基于 MJCF 模型创建物理模拟实例
physics = mjcf.Physics.from_mjcf_model(model)

# 创建一个可移动的相机用于渲染
# 相机的高度和宽度与渲染分辨率保持一致
camera = mujoco.MovableCamera(physics, height=res[0], width=res[1])

# 渲染模型并围绕它平移相机，以生成一系列帧
frames = []  # 用于存储渲染出的每一帧图像
rot = 360.0  # 相机旋转的总角度 (360度)
delta = 10.0  # 每一步相机旋转的角度增量

# 循环渲染，每次改变相机的方位角
for i in range(int(rot / delta)):
    camera._render_camera.azimuth = i * delta  # 设置相机的水平方位角
    frames.append(Image.fromarray(camera.render()))  # 渲染当前视角并存入帧列表

# 将捕获的帧保存为 GIF 动画文件
frames[0].save(
    "cube3x3x3.gif",  # 输出文件名
    format="GIF",  # 文件格式
    append_images=frames[1:],  # 将剩余的帧附加到动画中
    save_all=True,  # 确保所有帧都被保存
    loop=0,  # 设置 GIF 无限循环播放
    duration=100,  # 每一帧的持续时间 (毫秒)
)
