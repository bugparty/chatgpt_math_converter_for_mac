# Marko 中 Block 和 Inline 元素的区别

## 1. 核心概念

### Block 元素 (块级元素)
- **占据完整的行或多行**
- 前后通常有空行分隔
- 可以包含其他 block 或 inline 元素
- 从源文本的开始位置逐行匹配

### Inline 元素 (行内元素)
- **在行内出现，不会换行**
- 嵌入在 block 元素内部
- 通常用于文本修饰
- 在一行文本内查找所有匹配

---

## 2. 实现方式区别

### Block 元素实现
```python
class MyBlockElement(BlockElement):
    # 定义匹配规则
    @classmethod
    def match(cls, source: Source) -> Any:
        """检查当前行是否匹配此元素"""
        return source.expect_re(pattern)
    
    @classmethod
    def parse(cls, source: Source) -> Any:
        """解析并消费源文本，返回元素"""
        # 可以消费多行
        # 可以解析嵌套的 inline 元素
        pass
```

### Inline 元素实现
```python
class MyInlineElement(InlineElement):
    # 定义正则表达式模式
    pattern = r'正则表达式'
    parse_children = False  # 是否解析内部内容
    priority = 5
    
    def __init__(self, match):
        """从正则匹配对象构造元素"""
        self.content = match.group(1)
```

---

## 3. Marko 内置的 Block 元素

| 元素名 | 描述 | Markdown 语法 |
|--------|------|---------------|
| `Document` | 文档根节点 | (根节点) |
| `Heading` | 标题 | `# ## ###` |
| `Paragraph` | 段落 | 普通文本段落 |
| `List` | 列表 | `* - +` 或 `1. 2.` |
| `ListItem` | 列表项 | 列表中的每一项 |
| `Quote` | 引用块 | `> 引用文本` |
| `CodeBlock` | 代码块 | 4空格缩进 |
| `FencedCode` | 围栏代码块 | ` ``` code ``` ` |
| `HTMLBlock` | HTML 块 | `<div>...</div>` |
| `ThematicBreak` | 分隔线 | `---` 或 `***` |
| `BlankLine` | 空行 | (空行) |
| `LinkRefDef` | 链接引用定义 | `[ref]: url` |
| `SetextHeading` | Setext 标题 | 下划线样式标题 |

---

## 4. Marko 内置的 Inline 元素

| 元素名 | 描述 | Markdown 语法 |
|--------|------|---------------|
| `RawText` | 普通文本 | 纯文本 |
| `Emphasis` | 斜体 | `*text*` 或 `_text_` |
| `StrongEmphasis` | 粗体 | `**text**` 或 `__text__` |
| `CodeSpan` | 行内代码 | `` `code` `` |
| `Link` | 链接 | `[text](url)` |
| `Image` | 图片 | `![alt](url)` |
| `AutoLink` | 自动链接 | `<url>` |
| `LineBreak` | 换行符 | 两个空格 + 换行 |
| `InlineHTML` | 行内 HTML | `<span>text</span>` |
| `Literal` | 字面文本 | `\*` 转义字符 |

---

## 5. 示例对比

### Markdown 文本
```markdown
## 这是标题 (Block: Heading)

这是一个**段落**(Block: Paragraph)，包含**粗体**(Inline: StrongEmphasis)
和`代码`(Inline: CodeSpan)以及[链接](url)(Inline: Link)。

* 列表项 1 (Block: List > ListItem)
* 列表项 2

```python
# 代码块 (Block: FencedCode)
print("hello")
```
```

### 解析结果结构
```
Document (Block)
├── Heading (Block)
│   └── RawText (Inline): "这是标题"
├── Paragraph (Block)
│   ├── RawText (Inline): "这是一个"
│   ├── StrongEmphasis (Inline)
│   │   └── RawText: "段落"
│   ├── RawText (Inline): "，包含"
│   ├── StrongEmphasis (Inline)
│   │   └── RawText: "粗体"
│   ├── RawText (Inline): "和"
│   ├── CodeSpan (Inline): "代码"
│   ├── RawText (Inline): "以及"
│   └── Link (Inline)
│       └── RawText: "链接"
└── List (Block)
    ├── ListItem (Block)
    │   └── Paragraph (Block)
    │       └── RawText (Inline): "列表项 1"
    └── ListItem (Block)
        └── Paragraph (Block)
            └── RawText (Inline): "列表项 2"
```

---

## 6. 你的 InlineMath 示例

### 为什么是 Inline 元素？

```python
class InlineMath(InlineElement):
    pattern = r'\$([^\$\n]+?)\$'  # 匹配 $...$ 格式
    parse_children = False
    priority = 7
    
    def __init__(self, match):
        self.math_content = match.group(1)
```

**InlineMath 是 Inline 元素的原因：**

✓ 使用正则表达式 `pattern` 匹配  
✓ 在文本行内匹配 `$...$` 格式  
✓ 不占据整行  
✓ 嵌入在段落等 block 元素中  
✓ 例如: `这是公式 $x^2$ 在段落中`

### 如果要创建 Block 数学公式？

如果你想要块级数学公式（独占一行或多行），应该创建 Block 元素：

```python
class BlockMath(BlockElement):
    """块级数学公式 (用 $$ ... $$ 或 [ ... ] 包裹)"""
    
    @classmethod
    def match(cls, source: Source):
        # 匹配 $$ 开头或 [ 开头的行
        return source.expect_re(r'^\$\$|^\[')
    
    @classmethod
    def parse(cls, source: Source):
        # 解析多行数学公式直到结束符
        start = source.match.group(0)
        lines = [source.forward()]
        
        if start == '$$':
            # 继续读取直到遇到 $$
            while not source.match(r'^\$\$'):
                lines.append(source.forward())
        elif start == '[':
            # 继续读取直到遇到 ]
            while not source.match(r'^\]'):
                lines.append(source.forward())
        
        return cls(lines)
    
    def __init__(self, lines):
        self.math_content = '\n'.join(lines)
```

---

## 7. 关键总结

| 特性 | Block 元素 | Inline 元素 |
|------|-----------|------------|
| 位置 | 独立的行/块 | 行内文本 |
| 换行 | 可以跨多行 | 通常单行内 |
| 实现 | `match()` + `parse()` | `pattern` (正则) + `__init__()` |
| 包含关系 | 可以包含 block/inline | 只能包含 inline |
| 例子 | 段落、标题、列表 | 粗体、链接、代码 |
| 你的例子 | BlockMath (`$$...$$`) | InlineMath (`$...$`) |

