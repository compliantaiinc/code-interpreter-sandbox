from daytona import CreateSnapshotParams, Resources

from daytona_client import create_or_update_snapshot, get_daytona
from template import image

SNAPSHOT_NAME = "stepscale-sandbox-dev"
SNAPSHOT_RESOURCES = Resources(cpu=2, memory=4, disk=4)


if __name__ == "__main__":
    daytona = get_daytona()
    create_or_update_snapshot(
        daytona,
        CreateSnapshotParams(
            name=SNAPSHOT_NAME,
            image=image,
            resources=SNAPSHOT_RESOURCES,
        ),
        on_logs=print,
        timeout=0,
    )
