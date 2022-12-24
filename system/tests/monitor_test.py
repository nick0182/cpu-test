from system.monitor import list_active_monitors


def test_get_monitors():
    active_monitors = list_active_monitors()
    print(str(active_monitors))
