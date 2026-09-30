import os, subprocess
from pathlib import Path

WORKSPACE = Path(r"C:\Users\Maharshi\Documents\IITM_Agentic")
HTML_OUT = WORKSPACE / "IITM_Expert_Practical_Notebook.html"
PDF_OUT  = WORKSPACE / "IITM_Expert_Practical_Notebook.pdf"
EDGE     = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

print(f"HTML size: {HTML_OUT.stat().st_size:,} bytes")
print("Compiling PDF via Edge headless...")
r = subprocess.run([EDGE, "--headless", "--disable-gpu",
    f"--print-to-pdf={str(PDF_OUT)}",
    f"file:///{str(HTML_OUT).replace(os.sep, '/')}"],
    capture_output=True, text=True)
if PDF_OUT.exists():
    print(f"SUCCESS: {PDF_OUT.name} ({PDF_OUT.stat().st_size:,} bytes)")
else:
    print(f"Failed: {r.stderr[:300]}")
