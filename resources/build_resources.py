
import glob
import os

fl = []

target = os.path.join("menu", "*.png")
for file in glob.glob(target):
	b = os.path.basename(file)
	fl.append(f"<file alias=\"menu-{b}\">{file}</file>")

target = os.path.join("gui", "*.png")
for file in glob.glob(target):
	b = os.path.basename(file)
	fl.append(f"<file alias=\"gui-{b}\">{file}</file>")

target = os.path.join("misc", "*.*")
for file in glob.glob(target):
	b = os.path.basename(file)
	fl.append(f"<file alias=\"{b}\">{file}</file>")

target = os.path.join("fancy", "*.png")
for file in glob.glob(target):
	b = os.path.basename(file)
	fl.append(f"<file alias=\"fancy-{b}\">{file}</file>")

rfiles = "\n".join(fl)

out = f"""
<RCC>
<qresource>
{rfiles}
</qresource>
</RCC>
"""

print(out)
