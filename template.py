# template.py
from daytona import Image

APT_PACKAGES = [
    "libreoffice",  # soffice --headless --convert-to pdf/docx
    "poppler-utils",  # pdftoppm
]

_APT_INSTALL = (
    "apt-get update "
    f"&& apt-get install -y --no-install-recommends {' '.join(APT_PACKAGES)} "
    "&& rm -rf /var/lib/apt/lists/*"
)

image = (
    Image.debian_slim("3.12")
    .run_commands(_APT_INSTALL)
    .pip_install(["python-pptx"])
    .workdir("/home/daytona")
)
