# 发布检查清单

在发布到 PyPI 之前，请按照这个清单检查：

## 📋 必须完成的步骤

### 1. 更新项目信息
- [ ] 编辑 `pyproject.toml`，将 `email = "your-email@example.com"` 改为你的真实邮箱
- [ ] 确认 `version = "0.1.0"` 是否正确
- [ ] 确认 `name = "chatgpt-math-converter"` 在 PyPI 上没有被占用

### 2. 注册账号
- [ ] 在 [PyPI](https://pypi.org/account/register/) 注册账号
- [ ] 在 [Test PyPI](https://test.pypi.org/account/register/) 注册账号（用于测试）
- [ ] 验证邮箱

### 3. 获取 API Token
- [ ] 登录 [PyPI](https://pypi.org/)，进入 Account Settings > API tokens
- [ ] 点击 "Add API token"，选择 "Entire account" 或创建项目后选择具体项目
- [ ] 复制生成的 token（格式：`pypi-...`），妥善保存
- [ ] 对 [Test PyPI](https://test.pypi.org/) 重复相同步骤

### 4. 选择发布工具

#### 选项 A: 使用 uv（推荐，更现代）
```powershell
# 安装 uv
winget install --id astral-sh.uv
```
- [ ] 安装完成后重启 PowerShell
- [ ] 运行 `uv --version` 确认安装成功
- [ ] 阅读 `PUBLISHING.md` 文档

#### 选项 B: 使用传统工具（build + twine）
```powershell
pip install build twine
```
- [ ] 安装完成
- [ ] 阅读 `PUBLISHING_TRADITIONAL.md` 文档

## 🧪 测试步骤

### 5. 本地测试包构建

#### 使用 uv:
```powershell
cd c:\Users\bowman\sources\chatgpt_math_converter_for_mac
uv build
```

#### 使用传统方式:
```powershell
cd c:\Users\bowman\sources\chatgpt_math_converter_for_mac
python -m build
```

- [ ] 构建成功，生成 `dist/` 目录
- [ ] 检查生成的文件：
  - `chatgpt_math_converter-0.1.0-py3-none-any.whl`
  - `chatgpt_math_converter-0.1.0.tar.gz`

### 6. 发布到 Test PyPI（强烈推荐）

#### 使用 uv:
```powershell
uv publish --publish-url https://test.pypi.org/legacy/ --token pypi-YOUR_TEST_TOKEN
```

#### 使用传统方式:
```powershell
python -m twine upload --repository testpypi dist/*
# Username: __token__
# Password: pypi-YOUR_TEST_TOKEN
```

- [ ] 发布成功
- [ ] 访问 https://test.pypi.org/project/chatgpt-math-converter/ 查看

### 7. 从 Test PyPI 测试安装

```powershell
# 创建新的虚拟环境
python -m venv test-env
test-env\Scripts\activate

# 从 Test PyPI 安装
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ chatgpt-math-converter

# 在 Windows 上安装依赖
pip install pywin32

# 测试命令
chatgpt-math-converter
```

- [ ] 安装成功
- [ ] 命令可以运行
- [ ] 功能正常工作
- [ ] 停止程序（Ctrl+C）
- [ ] 退出虚拟环境：`deactivate`

## 🚀 正式发布

### 8. 发布到正式 PyPI

#### 使用 uv:
```powershell
uv publish --token pypi-YOUR_PYPI_TOKEN
```

#### 使用传统方式:
```powershell
python -m twine upload dist/*
# Username: __token__
# Password: pypi-YOUR_PYPI_TOKEN
```

- [ ] 发布成功
- [ ] 访问 https://pypi.org/project/chatgpt-math-converter/ 确认

### 9. 验证正式安装

```powershell
# 新的虚拟环境
python -m venv verify-env
verify-env\Scripts\activate

# 从 PyPI 安装
pip install chatgpt-math-converter
pip install pywin32  # Windows

# 测试
chatgpt-math-converter
```

- [ ] 安装成功
- [ ] 功能正常
- [ ] 退出：`deactivate`

## 📝 发布后任务

### 10. 创建 Git 标签和 Release

```powershell
git add .
git commit -m "Prepare for v0.1.0 release"
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin master
git push origin v0.1.0
```

- [ ] 代码已提交
- [ ] 标签已创建
- [ ] 已推送到 GitHub

### 11. 在 GitHub 创建 Release

- [ ] 访问 https://github.com/bugparty/chatgpt_math_converter_for_mac/releases/new
- [ ] 选择标签 `v0.1.0`
- [ ] 填写 Release 标题和描述（可以从 CHANGELOG.md 复制）
- [ ] 发布 Release

### 12. 更新文档

- [ ] 确认 README.md 中的安装说明正确
- [ ] 添加 PyPI 徽章到 README（可选）：
  ```markdown
  ![PyPI](https://img.shields.io/pypi/v/chatgpt-math-converter)
  ![Python](https://img.shields.io/pypi/pyversions/chatgpt-math-converter)
  ```

## 🎉 完成！

恭喜！你的包已经成功发布到 PyPI。

现在任何人都可以通过以下方式安装：
```bash
pip install chatgpt-math-converter
```

## 📈 后续版本发布

当你需要发布新版本时：

1. 修改代码
2. 更新 `CHANGELOG.md`
3. 更新 `pyproject.toml` 中的版本号
4. 清理旧构建：`Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue`
5. 重新构建和发布
6. 创建新的 Git 标签和 Release

## ⚠️ 注意事项

- PyPI 不允许覆盖已发布的版本
- 如果发布错误，只能发布新版本
- 保护好你的 API Token，不要提交到 Git
- Test PyPI 的数据会定期清理，不要依赖它作为永久存储
