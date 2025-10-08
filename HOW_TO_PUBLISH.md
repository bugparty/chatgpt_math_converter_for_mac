# 📦 如何发布到 PyPI - 快速指南

## 🎯 目标

让用户可以通过 `pip install chatgpt-clipboard-latex-fixer` 安装你的软件，然后直接用 `chatgpt-clipboard-latex-fixer` 命令运行。

## ✅ 已完成的准备工作

你的项目已经配置好了！包括：

1. ✅ `pyproject.toml` - 项目配置文件
2. ✅ `src/chatgpt_math_converter/` - 标准包结构
3. ✅ 命令行入口点配置
4. ✅ 完整的发布文档

## 🚀 三步发布流程

### 第一步：选择工具并安装

**选项 A：uv（推荐，更快更现代）**
```powershell
winget install --id astral-sh.uv
```
重启 PowerShell 后继续

**选项 B：传统工具（build + twine）**
```powershell
pip install build twine
```

### 第二步：注册并获取 Token

1. 访问 https://pypi.org/account/register/ 注册
2. 访问 https://test.pypi.org/account/register/ 注册（测试用）
3. 在 PyPI 的 Account Settings > API tokens 生成 token
4. 保存你的 token（格式：`pypi-AgEIcHl...`）

### 第三步：构建并发布

**先测试（推荐）：**

使用 uv:
```powershell
cd c:\Users\bowman\sources\chatgpt_math_converter_for_mac
uv build
uv publish --publish-url https://test.pypi.org/legacy/ --token pypi-YOUR_TEST_TOKEN
```

使用传统工具:
```powershell
cd c:\Users\bowman\sources\chatgpt_math_converter_for_mac
python -m build
python -m twine upload --repository testpypi dist/*
```

**正式发布：**

使用 uv:
```powershell
uv publish --token pypi-YOUR_PYPI_TOKEN
```

使用传统工具:
```powershell
python -m twine upload dist/*
```

## 📚 详细文档

- **`CHECKLIST.md`** - 完整的发布检查清单（推荐先看这个）
- **`PUBLISHING.md`** - 使用 uv 的详细指南
- **`PUBLISHING_TRADITIONAL.md`** - 使用传统工具的详细指南
- **`PUBLISHING_SUMMARY.md`** - 项目结构和发布方式对比

## 🧪 本地测试

在发布前，可以运行本地测试脚本：

```powershell
.\test-local-install.ps1
```

这个脚本会：
- 清理旧的构建文件
- 构建包
- 在虚拟环境中测试安装
- 验证命令是否可用

## ⚠️ 发布前必做

1. **更新邮箱**：编辑 `pyproject.toml`，将 `your-email@example.com` 改为你的邮箱
2. **检查包名**：确认 `chatgpt-clipboard-latex-fixer` 在 PyPI 上没被占用
3. **版本号**：首次发布使用 `0.1.0`

## 🎉 发布后

用户就可以这样使用：

```bash
# 安装
pip install chatgpt-clipboard-latex-fixer

# Windows 用户
pip install pywin32

# macOS 用户
pip install pyobjc

# 运行
chatgpt-clipboard-latex-fixer
```

## 📞 需要帮助？

- 查看 `CHECKLIST.md` 获取完整步骤
- 查看对应的 PUBLISHING 文档获取详细说明
- 查看 PyPI 官方文档：https://packaging.python.org/

## 🔄 发布新版本

1. 修改代码
2. 更新 `pyproject.toml` 中的 `version`（如 0.1.0 → 0.1.1）
3. 更新 `CHANGELOG.md`
4. 清理并重新构建：
   ```powershell
   Remove-Item -Recurse -Force dist
   uv build  # 或 python -m build
   uv publish --token YOUR_TOKEN  # 或 python -m twine upload dist/*
   ```

---

**记住：PyPI 不允许覆盖已发布的版本，每次发布必须使用新的版本号！**
