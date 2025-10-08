# 发布到 PyPI 指南

本指南将帮助你将 `chatgpt-math-converter` 发布到 PyPI，让用户可以通过 `pip install chatgpt-math-converter` 安装。

## 前置准备

### 1. 安装 uv (如果还没有安装)

```powershell
# Windows PowerShell
irm https://astral.sh/uv/install.ps1 | iex
```

或者

```bash
# 使用 pip 安装
pip install uv
```

### 2. 注册 PyPI 账号

1. 访问 [PyPI](https://pypi.org/) 并注册账号
2. 访问 [Test PyPI](https://test.pypi.org/) 并注册账号（用于测试）

### 3. 生成 API Token

1. 登录 [PyPI](https://pypi.org/)
2. 进入 Account Settings -> API tokens
3. 创建新的 API token（选择 "Entire account" 或特定项目）
4. 保存生成的 token（格式：`pypi-...`）

对 Test PyPI 重复相同步骤。

## 发布步骤

### Step 1: 更新项目信息

编辑 `pyproject.toml`，确保以下信息正确：

```toml
[project]
name = "chatgpt-math-converter"
version = "0.1.0"  # 每次发布需要更新版本号
authors = [
    {name = "你的名字", email = "your-email@example.com"}  # 更新为你的信息
]
```

### Step 2: 构建分发包

使用 uv 构建你的包：

```powershell
# 确保在项目根目录
cd c:\Users\bowman\sources\chatgpt_math_converter_for_mac

# 构建包
uv build
```

这将在 `dist/` 目录下生成两个文件：
- `chatgpt_math_converter-0.1.0-py3-none-any.whl` (wheel 包)
- `chatgpt_math_converter-0.1.0.tar.gz` (源码包)

### Step 3: 测试发布（推荐）

先发布到 Test PyPI 测试：

```powershell
# 使用 uv 发布到 Test PyPI
uv publish --publish-url https://test.pypi.org/legacy/ --token pypi-YOUR_TEST_PYPI_TOKEN
```

或者配置 token 后：

```powershell
# 设置环境变量
$env:UV_PUBLISH_TOKEN = "pypi-YOUR_TEST_PYPI_TOKEN"

# 发布
uv publish --publish-url https://test.pypi.org/legacy/
```

测试安装：

```powershell
# 从 Test PyPI 安装
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ chatgpt-math-converter

# 在 Windows 上需要额外安装依赖
pip install pywin32

# 测试命令
chatgpt-math-converter
```

### Step 4: 正式发布到 PyPI

确认测试无误后，发布到正式 PyPI：

```powershell
# 使用 token 发布
uv publish --token pypi-YOUR_PYPI_TOKEN
```

或者使用环境变量：

```powershell
$env:UV_PUBLISH_TOKEN = "pypi-YOUR_PYPI_TOKEN"
uv publish
```

### Step 5: 验证安装

```powershell
# 创建新的虚拟环境测试
uv venv test-env
test-env\Scripts\activate

# 安装你的包
pip install chatgpt-math-converter

# Windows 用户需要安装平台依赖
pip install pywin32

# macOS 用户需要安装平台依赖
pip install pyobjc

# 测试运行
chatgpt-math-converter
```

## 配置文件方式（推荐）

为了避免每次输入 token，可以创建配置文件：

### Windows

创建文件 `%APPDATA%\uv\uv.toml` 或 `~\.config\uv\uv.toml`：

```toml
[publish]
token = "pypi-YOUR_TOKEN"
```

### macOS/Linux

创建文件 `~/.config/uv/uv.toml`：

```toml
[publish]
token = "pypi-YOUR_TOKEN"
```

## 更新版本发布流程

1. **修改代码**
2. **更新版本号**：编辑 `pyproject.toml` 中的 `version = "0.1.1"`
3. **更新 CHANGELOG**（可选但推荐）
4. **重新构建**：`uv build`
5. **发布**：`uv publish`

## 常见问题

### Q: 如何删除已发布的版本？

PyPI 不允许删除已发布的版本，但可以 "yank" 它：

```powershell
# 需要使用 twine
pip install twine
twine upload --skip-existing dist/*
```

### Q: 如何更新包信息（描述、分类等）？

必须发布新版本。PyPI 不允许修改已发布版本的元数据。

### Q: 包名已被占用怎么办？

修改 `pyproject.toml` 中的 `name` 字段，例如：
- `chatgpt-math-converter-plus`
- `your-username-chatgpt-math-converter`

### Q: 如何查看构建结果？

```powershell
# 列出 dist 目录
ls dist/

# 查看 wheel 包内容
python -m zipfile -l dist/chatgpt_math_converter-0.1.0-py3-none-any.whl
```

## 最佳实践

1. **使用语义化版本**：`MAJOR.MINOR.PATCH`（如 1.0.0, 1.0.1, 1.1.0）
2. **维护 CHANGELOG**：记录每个版本的更改
3. **先测试后发布**：使用 Test PyPI
4. **添加 CI/CD**：自动化构建和发布流程
5. **保护 Token**：不要提交到 git
6. **添加 .gitignore**：排除 `dist/`, `*.egg-info/`, `build/` 等

## 用户安装和使用

发布成功后，用户可以这样使用：

```powershell
# 安装
pip install chatgpt-math-converter

# Windows 用户额外安装
pip install pywin32

# macOS 用户额外安装
pip install pyobjc

# 直接运行
chatgpt-math-converter
```

## 其他资源

- [PyPI 官方文档](https://packaging.python.org/)
- [uv 文档](https://docs.astral.sh/uv/)
- [语义化版本](https://semver.org/)
