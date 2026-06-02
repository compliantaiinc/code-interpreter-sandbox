import os
import time
from collections.abc import Callable
from pathlib import Path

from daytona import CreateSnapshotParams, Daytona, DaytonaConfig
from daytona.common.errors import DaytonaConflictError, DaytonaNotFoundError
from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parent

load_dotenv(_REPO_ROOT / ".env")
load_dotenv(_REPO_ROOT / ".env.local", override=True)

_DELETE_POLL_INTERVAL_S = 2.0
_DELETE_TIMEOUT_S = 600.0
_CREATE_RETRY_INTERVALS_S = (2.0, 4.0, 8.0, 16.0)


def get_daytona() -> Daytona:
    api_key = os.environ.get("DAYTONA_API_KEY")
    if not api_key:
        raise RuntimeError(
            "DAYTONA_API_KEY is not set. Copy .env.example to .env and add your key."
        )
    return Daytona(DaytonaConfig(api_key=api_key))


def _log(on_logs: Callable[[str], None] | None, message: str) -> None:
    if on_logs:
        on_logs(message)


def _wait_until_snapshot_gone(
    daytona: Daytona,
    name: str,
    *,
    on_logs: Callable[[str], None] | None = None,
    timeout: float = _DELETE_TIMEOUT_S,
) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            snapshot = daytona.snapshot.get(name)
        except DaytonaNotFoundError:
            return
        _log(on_logs, f"Waiting for {name!r} removal (state: {snapshot.state})...")
        time.sleep(_DELETE_POLL_INTERVAL_S)
    raise RuntimeError(
        f"Timed out after {timeout:.0f}s waiting for snapshot {name!r} to be deleted"
    )


def _delete_snapshot_if_exists(
    daytona: Daytona,
    name: str,
    *,
    on_logs: Callable[[str], None] | None = None,
) -> None:
    try:
        existing = daytona.snapshot.get(name)
    except DaytonaNotFoundError:
        return
    _log(on_logs, f"Snapshot {name!r} exists (state: {existing.state}); deleting...")
    daytona.snapshot.delete(existing)
    _wait_until_snapshot_gone(daytona, name, on_logs=on_logs)


def _create_snapshot_with_retries(
    daytona: Daytona,
    params: CreateSnapshotParams,
    *,
    on_logs: Callable[[str], None] | None = None,
    timeout: float | None = 0,
):
    intervals = (0.0, *_CREATE_RETRY_INTERVALS_S)
    last_error: DaytonaConflictError | None = None
    for attempt, delay in enumerate(intervals):
        if delay:
            _log(
                on_logs,
                f"Name {params.name!r} still reserved; retrying create in {delay:.0f}s "
                f"(attempt {attempt + 1}/{len(intervals)})...",
            )
            time.sleep(delay)
        try:
            return daytona.snapshot.create(
                params, on_logs=on_logs, timeout=timeout
            )
        except DaytonaConflictError as exc:
            last_error = exc
    assert last_error is not None
    raise last_error


def create_or_update_snapshot(
    daytona: Daytona,
    params: CreateSnapshotParams,
    *,
    on_logs: Callable[[str], None] | None = None,
    timeout: float | None = 0,
):
    """Create a snapshot, replacing an existing one with the same name if needed."""
    _delete_snapshot_if_exists(daytona, params.name, on_logs=on_logs)
    return _create_snapshot_with_retries(
        daytona, params, on_logs=on_logs, timeout=timeout
    )
