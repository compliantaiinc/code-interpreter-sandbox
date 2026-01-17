# template.py
from e2b import Template

template = (
    Template()
    .from_template("code-interpreter-v1")
    .apt_install([
        "libocct-data-exchange-dev",
        "libocct-draw-dev",
        "libocct-foundation-dev",
        "libocct-modeling-algorithms-dev",
        "libocct-modeling-data-dev",
        "libocct-ocaf-dev",
        "libocct-visualization-dev",
        "libboost-all-dev",
        "libxml2-dev",
        "libhdf5-dev"
    ])
    .pip_install(['ifcopenshell', 'python-pptx'])  # Install Python packages
)
