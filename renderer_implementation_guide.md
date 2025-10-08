# Marko 自定义元素的 Renderer 实现指南

## 概述

实现一个自定义 Markdown 元素需要三个部分：
1. **Element 类** - 定义元素结构和解析逻辑
2. **Renderer 类** - 定义如何将元素渲染回 Markdown
3. **Extension 类** - 将元素和渲染器组合成扩展

---

## 1. Renderer 类的基本结构

```python
from marko.md_renderer import MarkdownRenderer

class MathMarkdownRenderer(MarkdownRenderer):
    """自定义渲染器，继承 MarkdownRenderer"""
    
    def render_<element_name>(self, element):
        """渲染方法
        
        命名规则: render_ + 元素类名的小写蛇形命名
        例如: BlockMath -> render_block_math
             InlineMath -> render_inline_math
        """
        # 返回 Markdown 格式的字符串
        return "markdown text"
```

---

## 2. 渲染方法命名规则

| 元素类名 | 渲染方法名 |
|---------|----------|
| `BlockMath` | `render_block_math` |
| `InlineMath` | `render_inline_math` |
| `InlineBlockMath` | `render_inline_block_math` |
| `MyCustomElement` | `render_my_custom_element` |

**规则**: 将驼峰命名转换为小写下划线命名

---

## 3. 三个数学元素的 Renderer 实现

### 3.1 BlockMath Renderer

```python
class MathMarkdownRenderer(MarkdownRenderer):
    
    def render_block_math(self, element):
        """渲染块级数学公式
        
        输入: BlockMath 元素对象
        输出: Markdown 文本字符串
        
        格式:
        [
        math_content
        ]
        """
        # 块级元素需要前后换行
        return f"[\n{element.math_content}\n]\n"
```

**示例**:
- 输入元素: `BlockMath(math_content="E = mc^2")`
- 输出文本: 
  ```
  [
  E = mc^2
  ]
  ```

---

### 3.2 InlineMath Renderer

```python
class MathMarkdownRenderer(MarkdownRenderer):
    
    def render_inline_math(self, element):
        """渲染内联数学公式
        
        输入: InlineMath 元素对象
        输出: Markdown 文本字符串
        
        格式: $math_content$
        """
        # 行内元素不需要额外换行
        return f"${element.math_content}$"
```

**示例**:
- 输入元素: `InlineMath(math_content="x^2 + y^2")`
- 输出文本: `$x^2 + y^2$`

---

### 3.3 InlineBlockMath Renderer

```python
class MathMarkdownRenderer(MarkdownRenderer):
    
    def render_inline_block_math(self, element):
        """渲染行内的块级数学公式
        
        输入: InlineBlockMath 元素对象
        输出: Markdown 文本字符串
        
        格式: [content]
        """
        return f"[{element.math_content}]"
```

**示例**:
- 输入元素: `InlineBlockMath(math_content="\na + b\n")`
- 输出文本: `[\na + b\n]`

---

## 4. 完整的扩展配置

```python
class MathExtension:
    """数学公式扩展"""
    
    # 要添加的元素列表
    elements = [BlockMath, InlineMath, InlineBlockMath]
    
    # 解析器 mixins (如果需要自定义解析行为)
    parser_mixins = []
    
    # 渲染器 mixins (将自定义渲染器添加到这里)
    renderer_mixins = [MathMarkdownRenderer]
```

---

## 5. 使用扩展

```python
from marko import Markdown

# 创建 Markdown 实例
md = Markdown()

# 注册扩展
md.use(MathExtension)

# 解析
text = """
[
E = mc^2
]

这是 $x^2$ 公式。
"""
doc = md.parse(text)

# 渲染
rendered = md.render(doc)
print(rendered)
```

---

## 6. Renderer 的工作原理

### 6.1 渲染流程

```
Document
  └─> render(doc)
       └─> 遍历 doc.children
            └─> 对每个 child:
                 └─> 调用 render_<element_type>(child)
                      └─> 返回 Markdown 文本
```

### 6.2 递归渲染

对于有子元素的元素（如 Paragraph），可以使用 `self.render_children(element)`：

```python
def render_paragraph(self, element):
    # 渲染段落的所有子元素（inline 元素）
    children = self.render_children(element)
    return f"{self._prefix}{children}\n"
```

### 6.3 Context 和 Prefix

Renderer 维护一些状态：
- `self._prefix` - 当前行的前缀（用于列表缩进等）
- `self._second_prefix` - 后续行的前缀

---

## 7. 常见模式

### Block 元素渲染

```python
def render_my_block_element(self, element):
    # Block 元素通常需要：
    # 1. 前导换行（由上一个元素的 \n 提供）
    # 2. 元素内容
    # 3. 尾部换行
    return f"{element.content}\n"
```

### Inline 元素渲染

```python
def render_my_inline_element(self, element):
    # Inline 元素通常：
    # 1. 没有换行
    # 2. 直接返回内容
    return f"{element.content}"
```

### 带子元素的渲染

```python
def render_my_container_element(self, element):
    # 渲染所有子元素
    children = self.render_children(element)
    return f"<wrapper>{children}</wrapper>\n"
```

---

## 8. 往返转换测试

一个好的 renderer 应该能够实现往返转换：

```python
# 原始文本
original = "[\\nE = mc^2\\n]"

# 解析
doc = md.parse(original)

# 渲染
rendered = md.render(doc)

# 再次解析
doc2 = md.parse(rendered)

# 应该得到相同的 AST 结构
assert len(doc.children) == len(doc2.children)
```

---

## 9. 调试技巧

### 查看元素结构

```python
print(f"Element type: {type(element)}")
print(f"Element attributes: {vars(element)}")
```

### 查看渲染结果

```python
rendered = md.render(doc)
print(repr(rendered))  # 显示转义字符
```

### 对比渲染结果

```python
print("Original:")
print(repr(original_text))
print("\nRendered:")
print(repr(rendered_text))
```

---

## 10. 总结

**实现 Renderer 的步骤**:

1. ✓ 创建 Renderer 类，继承 `MarkdownRenderer`
2. ✓ 为每个自定义元素添加 `render_<element_name>` 方法
3. ✓ 在 Extension 的 `renderer_mixins` 中注册 Renderer
4. ✓ 使用 `md.use(Extension)` 注册扩展
5. ✓ 使用 `md.render(doc)` 渲染文档

**关键点**:
- Block 元素需要换行
- Inline 元素不需要换行
- 方法名要匹配元素类名（蛇形命名）
- 测试往返转换确保正确性

---

## 附录：完整示例代码

请参考 `math_renderer_demo.py` 文件中的完整实现。
