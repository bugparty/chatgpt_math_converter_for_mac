import os
import re
from .math_parser import markdown_normalize


# Legacy regex-based converter (kept for reference)
def convert_math_syntax_legacy(input_text):
    """
    Old regex-based conversion - kept for backward compatibility.
    WARNING: This has ambiguity issues with regular brackets.
    """
    # turn  \[...\] into $$...$$ format
    output_text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', input_text, flags=re.DOTALL)
    # turn  \(...\) into $...$ format
    output_text = re.sub(r'\\\((.*?)\\\)', r'$\1$', output_text, flags=re.DOTALL)
    # turn $ xxx $ into $xxx$ format
    output_text = re.sub(r'\$\s*(.*?)\s*\$', r'$\1$', output_text, flags=re.DOTALL)
    # turn [\n ... \n] into $$\n ... \n$$ format
    output_text = re.sub(r'\[\n(.*?)\n\]', r'$$\n\1\n$$', output_text, flags=re.DOTALL)
    # turn ( ... ) into $ ... $ format
    output_text = re.sub(r'\((.*?)\)', r'$\1$', output_text, flags=re.DOTALL)
    return output_text


# New improved converter
def convert_math_syntax(input_text):
    """
    Convert ChatGPT math syntax to standard MathJax format.
    Uses the improved converter from math_converter_v2.py
    """
    try:        
        return markdown_normalize(input_text)
    except Exception as e:
        # Fallback to legacy if new module not available or fails
        print("Warning: Using legacy regex-based converter (may have ambiguity issues)", e)
        return convert_math_syntax_legacy(input_text)

if __name__ == "__main__":
    for file in os.listdir("testcases"):
        if file.endswith(".txt"):
            with open(os.path.join("testcases", file), "r", encoding="utf-8") as f:
                input_text = f.read()
            output_text = convert_math_syntax(input_text)
            with open(os.path.join("testcases", "outputs", file), "w", encoding="utf-8") as f:
                f.write(output_text)