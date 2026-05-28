from e2b import Template, default_build_logger
from template import template


if __name__ == "__main__":
    Template.build(
        template,
        alias="stepscale-sandbox",
        cpu_count=2,
        memory_mb=4096,  # 4 GB RAM
        on_build_logs=default_build_logger()
    )
