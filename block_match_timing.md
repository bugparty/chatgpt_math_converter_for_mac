# Block 元素的 match 方法触发时机

## 关键原则

**Block 元素的 match 方法只在行首被调用！**

如果文本已经在段落内部，不会再检查 block 元素，而是会被当作 inline 元素处理。

---

## 触发条件

Block 元素的 match 方法在以下情况被调用：

1. **解析器到达新的一行**
2. **这一行是潜在的块级元素开始**（不在其他 block 的内容中）
3. **从行首开始匹配**

---

## 示例分析

### 示例 1: 会触发 BlockMath.match()
```markdown
[
x = y
]
```
- `[` 在行首
- 独立的行
- **结果**: BlockMath.match() 被调用 ✓

---

### 示例 2: 不会触发 BlockMath.match()
```markdown
这是文本 [
x = y
]
```
- `[` 前面有文本 "这是文本 "
- 已经在段落内部
- **结果**: 整个内容被当作 Paragraph，[ 只是普通文本 ✗

---

### 示例 3: 会触发 BlockMath.match()
```markdown
段落文本

[
x = y
]
```
- 空行后，`[` 在新行的行首
- 段落已结束，开始新的 block
- **结果**: BlockMath.match() 被调用 ✓

---

### 示例 4: 你的测试文件情况
```markdown
[
x = $-1$^{s}\times \big$1.f\big$\times 2^{,E-\text{bias}}
]
```

这个看起来应该触发 BlockMath，但如果前面没有空行（在段落延续中），
可能已经被当作段落的一部分。

---

## 解决方案

如果你想让 `[ ... ]` 格式在行首被识别为 BlockMath：

### 1. 确保前面有空行
```markdown
## 标题

[
数学公式
]
```

### 2. 调整优先级
```python
class BlockMath(BlockElement):
    pattern = r'^\['
    priority = 10  # 提高优先级，超过 Paragraph (priority=5)
```

### 3. 查看测试文件格式
确保 `[` 前面有空行，不是段落的延续。

---

## Block vs Inline 的区别

### Block 元素（块级）
- 从**行首**开始匹配
- pattern 通常以 `^` 开头
- 例如: `^#` (标题), `^\[` (你的 BlockMath)

### Inline 元素（行内）
- 在**文本内部**查找
- 可以出现在任何位置
- 例如: `\$([^\$]+?)\$` (你的 InlineMath)

---

## 实际测试

你的 `testcases/001.txt` 中的 `[` 没有被识别为 BlockMath，是因为：

1. 检查 `[` 前一行是否有内容
2. 如果前一行有内容且没有空行，`[` 会被当作段落延续
3. 解决方法：在 `[` 前面加一个空行

```markdown
## 数值还原公式（normalized）

[                          <- 前面有空行，会触发 BlockMath
x = $-1$^{s}...
]
```

如果没有空行：
```markdown
## 数值还原公式（normalized）
[                          <- 前面没空行，是段落的一部分
x = $-1$^{s}...
]
```
