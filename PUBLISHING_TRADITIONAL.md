# 使用传统 build + twine 方式发布（不需要 uv）

## 步骤 1: 安装构建工具

```powershell
pip install build twine
```

## 步骤 2: 更新版本号

编辑 `pyproject.toml`，修改 `version` 字段和 `authors` 信息。

## 步骤 3: 构建包

```powershell
# 确保在项目根目录
cd c:\Users\bowman\sources\chatgpt_math_converter_for_mac

# 清理旧的构建文件（如果存在）
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

# 构建
python -m build
```

这会在 `dist/` 目录生成：
- `chatgpt_math_converter-0.1.0-py3-none-any.whl`
- `chatgpt_math_converter-0.1.0.tar.gz`

## 步骤 4: 测试发布（推荐）

```powershell
# 发布到 Test PyPI
python -m twine upload --repository testpypi dist/*

# 提示输入用户名和密码时：
# Username: __token__
# Password: pypi-YOUR_TEST_PYPI_TOKEN（从 https://test.pypi.org/ 获取）
```

测试安装：

```powershell
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ chatgpt-math-converter
pip install pywin32  # Windows
chatgpt-math-converter
```

## 步骤 5: 正式发布

```powershell
# 发布到 PyPI
python -m twine upload dist/*

# 提示输入用户名和密码时：
# Username: __token__
# Password: pypi-YOUR_PYPI_TOKEN（从 https://pypi.org/ 获取）
```

## 配置文件方式（避免每次输入密码）

创建 `%USERPROFILE%\.pypirc` 文件（Windows）或 `~/.pypirc`（macOS/Linux）：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_PYPI_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TEST_PYPI_TOKEN_HERE
```

之后就可以直接运行：

```powershell
# 测试发布
python -m twine upload --repository testpypi dist/*

# 正式发布
python -m twine upload dist/*
```

## 验证

```powershell
# 正式 PyPI 安装
pip install chatgpt-math-converter
pip install pywin32  # Windows 用户
chatgpt-math-converter
```
