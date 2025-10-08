# 快速开始指南

如果你还没有安装 `uv`，请先安装：

```powershell
# 使用 winget 安装（推荐）
winget install --id astral-sh.uv

# 或使用 PowerShell 脚本安装
irm https://astral.sh/uv/install.ps1 | iex

# 或使用 pip 安装
pip install uv
```

安装后，重新打开 PowerShell 窗口，然后按照 PUBLISHING.md 的步骤进行。

## 不使用 uv 的替代方案

如果你不想使用 uv，也可以使用传统的 build + twine 方式：

```powershell
# 安装构建工具
pip install build twine

# 构建包
python -m build

# 上传到 Test PyPI（测试）
python -m twine upload --repository testpypi dist/*

# 上传到 PyPI（正式发布）
python -m twine upload dist/*
```

配置 `.pypirc` 文件（位于 `%USERPROFILE%\.pypirc`）：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TEST_TOKEN_HERE
```
