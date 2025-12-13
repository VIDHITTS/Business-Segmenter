#!/usr/bin/env python3
"""Fix indentation in app.py"""

with open('app.py', 'r') as f:
    lines = f.readlines()

# Fix lines 247-257 to have proper indentation
# These are inside the 'with tab1:' block
fixed_lines = []
for i, line in enumerate(lines):
    line_num = i + 1
    
    # Lines 248-257 should be part of tab1 block (4 spaces from with tab1:)
    if 248 <= line_num <= 257:
        # Remove all leading whitespace
        content = line.lstrip()
        if content:  # If not empty line
            # Add 4 spaces for tab1 block level
            fixed_lines.append('    ' + content)
        else:
            fixed_lines.append('\n')
    else:
        fixed_lines.append(line)

# Write fixed version
with open('app.py', 'w') as f:
    f.writelines(fixed_lines)

print("Fixed indentation in app.py")
