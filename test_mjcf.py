# 导入所需的库
from dm_control import mjcf  # DeepMind Control Suite中的MJCF解析库
import numpy as np  # 用于数值计算的NumPy库
from absl.testing import absltest  # Abseil测试框架
from pathlib import Path  # 用于处理文件路径的Pathlib库

# 定义XML文件的路径，指向3x3x3魔方的模型文件
_XML_FILE = Path(__file__).parent / "cube_3x3x3.xml"


# 定义一个测试类，用于测试3x3x3魔方模型
class Cube3x3x3Test(absltest.TestCase):
    """Tests for the cube_3x3x3.xml model."""

    # 测试模型是否可以成功编译和步进
    def test_can_compile_and_step(self) -> None:
        """Tests that we can compile the model and step the physics."""
        # 从XML文件加载MJCF模型
        model = mjcf.from_path(str(_XML_FILE))
        # 基于加载的模型创建物理仿真环境
        physics = mjcf.Physics.from_mjcf_model(model)
        # 执行一个仿真步进
        physics.step()

    # 测试模型的总质量是否符合预期
    def test_mass(self) -> None:
        """Tests that the total mass of the cube is what we expect."""
        # 从XML文件加载MJCF模型
        model = mjcf.from_path(str(_XML_FILE))
        # 基于加载的模型创建物理仿真环境
        physics = mjcf.Physics.from_mjcf_model(model)
        # 预期的总质量
        expected_mass = 0.0685
        # 获取模型的实际总质量
        actual_mass = physics.bind(model.worldbody).subtreemass
        # 断言实际质量与预期质量在指定精度内几乎相等
        np.testing.assert_almost_equal(actual_mass, expected_mass, decimal=6)

    # 测试向模型中添加自由关节是否会引发错误
    def test_freejoint(self) -> None:
        """Tests that adding a freejoint to the cube does not throw an error."""
        # 从XML文件加载MJCF模型
        model = mjcf.from_path(str(_XML_FILE))
        # 找到名为"core"的body，并为其添加一个自由关节
        model.worldbody.find("body", "core").add("freejoint")
        # 基于修改后的模型创建物理仿真环境
        physics = mjcf.Physics.from_mjcf_model(model)
        # 执行一个仿真步进，检查是否会出错
        physics.step()


# 如果该脚本作为主程序运行，则执行测试
if __name__ == "__main__":
    absltest.main()
