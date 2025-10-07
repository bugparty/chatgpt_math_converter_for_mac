import re


# conver chatgpt math syntax to common markdown
def convert_math_syntax(input_text):
    # turn [ ... ] into $$ ... $$ format
    input_text = re.sub(r'\[(.*?)\]', r'$$\1$$', input_text, flags=re.DOTALL)
    # turn  \[...\] into $$...$$ format
    output_text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', input_text, flags=re.DOTALL)
    # turn  \(...\) into $...$ format
    output_text = re.sub(r'\\\((.*?)\\\)', r'$\1$', output_text, flags=re.DOTALL)
    # turn $ xxx $ into $xxx$ format
    output_text = re.sub(r'\$\s*(.*?)\s*\$', r'$\1$', output_text, flags=re.DOTALL)
    
    return output_text
