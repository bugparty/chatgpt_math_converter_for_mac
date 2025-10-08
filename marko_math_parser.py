from marko import Markdown
from marko.inline import InlineElement
from marko.block import BlockElement
from marko.md_renderer import MarkdownRenderer

import re


# ========== Block Element ==========
class BlockMath(BlockElement):
    """Block-level math element (wrapped in [ ... ], occupies a line)
    
    Example:
    [
    x = y + z
    ]
    """
    # Define matching pattern - Note: do not use ^, expect_re already matches from line start
    pattern = r' {0,3}\['  # Allow up to 3 spaces indentation
    priority = 10  # Set high priority to ensure matching before Paragraph
    
    @classmethod
    def match(cls, source):
        """match method: Check if the current line matches this element
        
        Parameters:
            source: Source object, provides access to source text
            
        Returns:
            Match object (if matched) or None
            
        Key methods:
            - source.expect_re(pattern): Try to match current line with regex
            - source.pos: Current parsing position
            - source.match: Last match result
        """
        # Use expect_re method to match current line
        # If match succeeds, return Match object; otherwise return None
        return source.expect_re(cls.pattern)
    
    @classmethod
    def parse(cls, source):
        """parse method: Parse element content
        
        Called after match succeeds, responsible for:
        1. Consume (read and remove) source text
        2. Extract element data
        3. Return parameters for constructing the element
        
        Key methods:
            - source.next_line(): Get current line (without consuming)
            - source.consume(): Consume (remove) current line
            - source.exhausted: Check if reached the end
        """
        # Get and consume the starting [ line
        source.next_line()
        source.consume()
        
        # Collect math content
        lines = []
        # Keep reading until encountering ]
        while not source.exhausted:
            line = source.next_line()
            if line is None:
                break
            if line.strip() == ']':
                source.consume()  # Consume ] line
                break
            lines.append(line)
            source.consume()  # Consume this line
        
        # Return math content (use ''.join to preserve original format)
        math_content = ''.join(lines).strip()
        return math_content
    
    def __init__(self, math_content):
        """Constructor: Receive parameters returned by parse"""
        self.math_content = math_content
        self.children = []  # Block elements need children attribute


# ========== Inline Element Example ==========
# Define custom inline math element
class InlineMath(InlineElement):
    """Inline math element (wrapped in $ ... $)"""
    pattern = r'\$([^\$\n]+?)\$'  # Match $...$ format math, no cross-line
    parse_children = False  # Do not parse internal content
    priority = 7  # Set priority

    def __init__(self, match):
        self.math_content = match.group(1)  # Extract math content between $
class InlineBlockMath(InlineElement):
    pattern = r'\[(\n[^\[\]\n]+?\n)\]'  # Match [ ... ] format math, no cross-line
    parse_children = False  # Do not parse internal content
    priority = 8  # Set priority

    def __init__(self, match):
        self.math_content = match.group(1)  # Extract math content between [


# ========== Renderer Implementation ==========
class MathMarkdownRenderer(MarkdownRenderer):
    """Custom Markdown renderer, supports math formulas"""
    
    def render_block_math(self, element):
        """Render block-level math
        
        Render BlockMath element back to Markdown format:
        $$
        math content
        $$
        """
        # Block elements need blank lines before and after
        return f"$$\n{element.math_content}\n$$\n"
    
    def render_inline_math(self, element):
        """Render inline math
        
        Render InlineMath element back to Markdown format:
        $math content$
        """
        return f"${element.math_content}$"
    
    def render_inline_block_math(self, element):
        """Render inline block math
        
        Render InlineBlockMath element back to Markdown format:
        $$
        content
        $$
        """
        return f"$$\n{element.math_content}\n$$"

# Create an extension class
class MathExtension:
    """Math extension - supports both block and inline"""
    elements = [BlockMath, InlineMath, InlineBlockMath]  # List of elements to add
    parser_mixins = []  # Parser mixins
    renderer_mixins = [MathMarkdownRenderer]  # Renderer mixins


if __name__ == "__main__":
    print("=" * 80)
    # Create custom Markdown instance and register extension
    md = Markdown()  # Do not specify renderer here, let extension system handle
    md.use(MathExtension)  # Use use method to register extension

    # Test parsing
    with open("testcases/001.txt", "r", encoding="utf-8") as f:
        text = f.read()
        doc = md.parse(text)
        print("=== Document Structure ===")
        print(doc)
        print("\n=== Detailed Child Element Analysis ===")
        for i, child in enumerate(doc.children):
            print(f"\n[{i}] Type: {type(child).__name__}")
            print(f"Content Preview: {str(child)[:100]}")
            
            # Special handling for BlockMath
            if isinstance(child, BlockMath):
                print(f"  *** Block-level Math Formula ***")
                print(f"  Content: {child.math_content[:100]}")
            
            # If paragraph or list item, print its children
            if hasattr(child, 'children'):
                print(f"  Number of Children: {len(child.children)}")
                for j, subchild in enumerate(child.children):
                    print(f"    [{j}] {type(subchild).__name__}", end='')
                    # Check if contains our custom InlineMath element
                    if isinstance(subchild, InlineMath):
                        print(f" -> Inline Math: '{subchild.math_content}'")
                    else:
                        content_preview = str(subchild)[:50].replace('\n', '\\n')
                        print(f": {content_preview}")
            print("-" * 70)

    print("\n" + "=" * 80)
    print("Test Markdown Renderer")
    print("=" * 80)

    # Render back to Markdown
    rendered = md.render(doc)
    print("\nRendered Result (first 500 characters):")
    print("-" * 80)
    print(rendered[:500])
    print("-" * 80)
