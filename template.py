# template.py
from daytona import Image

APT_PACKAGES = [
    "libreoffice",  # soffice --headless --convert-to pdf/docx/pptx
    "poppler-utils",  # pdftoppm
]

PIP_PACKAGES = [
    "PyYAML",  # import yaml
    "python-docx",
    "python-pptx",
]

_APT_INSTALL = (
    "apt-get update "
    f"&& apt-get install -y --no-install-recommends {' '.join(APT_PACKAGES)} "
    "&& rm -rf /var/lib/apt/lists/*"
)

image = (
    Image.debian_slim("3.12")
    .run_commands(_APT_INSTALL)
    .pip_install(PIP_PACKAGES)
    .workdir("/home/daytona")
)
