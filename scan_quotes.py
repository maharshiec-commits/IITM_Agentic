import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\Maharshi\Documents\IITM_Agentic\build_expert_notebook.py', encoding='utf-8') as f:
    lines = f.readlines()
# find triple-quote lines after line 13
for i, line in enumerate(lines[13:], 14):
    if '"""' in line:
        print('Line', i, ':', line[:80].strip())
        break
