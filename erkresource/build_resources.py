
import glob
import os

fl = []

for file in glob.glob("*.png"):
	fl.append(f"<file>{file}</file>")

# fl.append("<file>cnr.otf</file>")

# fl.append("<file>DejaVuSansMono.ttf</file>")
# fl.append("<file>DejaVuSansMono-Bold.ttf</file>")

# fl.append("<file>style.qss</file>")

rfiles = "\n".join(fl)

out = f"""
<RCC>
<qresource prefix="/core">
{rfiles}
</qresource>
</RCC>
"""

print(out)
