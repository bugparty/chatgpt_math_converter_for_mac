# 本地测试安装脚本
# 用于在发布前测试包是否能正确安装

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   本地测试 chatgpt-math-converter" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否在项目根目录
if (-not (Test-Path "pyproject.toml")) {
    Write-Host "错误: 请在项目根目录运行此脚本" -ForegroundColor Red
    exit 1
}

# 步骤 1: 清理旧的构建文件
Write-Host "[1/5] 清理旧的构建文件..." -ForegroundColor Yellow
Remove-Item -Recurse -Force dist, build, src/*.egg-info -ErrorAction SilentlyContinue
Write-Host "✓ 完成" -ForegroundColor Green
Write-Host ""

# 步骤 2: 检查构建工具
Write-Host "[2/5] 检查构建工具..." -ForegroundColor Yellow
$useUv = $false
$uvVersion = uv --version 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 找到 uv: $uvVersion" -ForegroundColor Green
    $useUv = $true
} else {
    Write-Host "! 未找到 uv，尝试使用 build..." -ForegroundColor Yellow
    python -m build --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "错误: 未找到构建工具，请安装 uv 或 build" -ForegroundColor Red
        Write-Host "安装方法:" -ForegroundColor Cyan
        Write-Host "  uv: winget install --id astral-sh.uv" -ForegroundColor White
        Write-Host "  build: pip install build" -ForegroundColor White
        exit 1
    }
    Write-Host "✓ 找到 build" -ForegroundColor Green
}
Write-Host ""

# 步骤 3: 构建包
Write-Host "[3/5] 构建包..." -ForegroundColor Yellow
if ($useUv) {
    uv build
} else {
    python -m build
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ 构建失败" -ForegroundColor Red
    exit 1
}
Write-Host "✓ 构建成功" -ForegroundColor Green
Write-Host ""

# 步骤 4: 检查生成的文件
Write-Host "[4/5] 检查生成的文件..." -ForegroundColor Yellow
$wheelFile = Get-ChildItem dist/*.whl | Select-Object -First 1
$tarFile = Get-ChildItem dist/*.tar.gz | Select-Object -First 1

if ($wheelFile -and $tarFile) {
    Write-Host "✓ 找到 wheel 文件: $($wheelFile.Name)" -ForegroundColor Green
    Write-Host "✓ 找到 tar.gz 文件: $($tarFile.Name)" -ForegroundColor Green
} else {
    Write-Host "✗ 缺少构建文件" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 步骤 5: 创建测试环境并安装
Write-Host "[5/5] 测试安装..." -ForegroundColor Yellow
Write-Host "创建虚拟环境..." -ForegroundColor White

$testEnvPath = "test-install-env"
Remove-Item -Recurse -Force $testEnvPath -ErrorAction SilentlyContinue
python -m venv $testEnvPath

Write-Host "安装包..." -ForegroundColor White
& "$testEnvPath\Scripts\pip.exe" install --quiet $wheelFile.FullName

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ 安装失败" -ForegroundColor Red
    exit 1
}

# 测试命令是否存在
Write-Host "测试命令..." -ForegroundColor White
$testResult = & "$testEnvPath\Scripts\chatgpt-math-converter.exe" --help 2>&1
if ($LASTEXITCODE -eq 0 -or $testResult -match "chatgpt") {
    Write-Host "✓ 命令安装成功！" -ForegroundColor Green
} else {
    Write-Host "! 警告: 命令可能未正确安装" -ForegroundColor Yellow
    Write-Host "输出: $testResult" -ForegroundColor Gray
}

# 清理测试环境
Write-Host "清理测试环境..." -ForegroundColor White
Remove-Item -Recurse -Force $testEnvPath -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   ✓ 所有测试通过！" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步:" -ForegroundColor Yellow
Write-Host "1. 发布到 Test PyPI 测试:" -ForegroundColor White
if ($useUv) {
    Write-Host "   uv publish --publish-url https://test.pypi.org/legacy/ --token YOUR_TOKEN" -ForegroundColor Cyan
} else {
    Write-Host "   python -m twine upload --repository testpypi dist/*" -ForegroundColor Cyan
}
Write-Host ""
Write-Host "2. 发布到正式 PyPI:" -ForegroundColor White
if ($useUv) {
    Write-Host "   uv publish --token YOUR_TOKEN" -ForegroundColor Cyan
} else {
    Write-Host "   python -m twine upload dist/*" -ForegroundColor Cyan
}
Write-Host ""
Write-Host "详细说明请查看 CHECKLIST.md" -ForegroundColor Gray
