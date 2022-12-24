from screeninfo import get_monitors, Enumerator
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Monitor(object):
    name: str
    primary: bool
    screen_coordinates: [int]
    width: int
    height: int
    size: [int]


def list_active_monitors():
    active_monitors = get_monitors(Enumerator.Windows)
    return list(map(lambda monitor: _map_monitor(monitor), active_monitors))


def _map_monitor(monitor):
    return Monitor(name=monitor.name, primary=monitor.is_primary, screen_coordinates=[monitor.x, monitor.y],
                   width=monitor.width, height=monitor.height, size=[monitor.width_mm, monitor.height_mm])
