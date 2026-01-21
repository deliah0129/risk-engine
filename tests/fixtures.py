def sample_events():
    """
    Fixed, deterministic event stream for consequence testing.
    """
    return [
        # Actor A: strong, aggressive
        {"turn": 6, "actor": "A", "ok": True,  "delta": 3.0, "cost": 1.0},
        {"turn": 7, "actor": "A", "ok": True,  "delta": 4.0, "cost": 1.2},
        {"turn": 8, "actor": "A", "ok": False, "delta": -1.0, "cost": 0.8},
        {"turn": 9, "actor": "A", "ok": True,  "delta": 5.0, "cost": 1.5},
        {"turn":10, "actor": "A", "ok": True,  "delta": 4.0, "cost": 1.3},

        # Actor B: declining, unstable
        {"turn": 6, "actor": "B", "ok": True,  "delta": 2.0, "cost": 0.5},
        {"turn": 7, "actor": "B", "ok": False, "delta": -2.0, "cost": 0.7},
        {"turn": 8, "actor": "B", "ok": False, "delta": -3.0, "cost": 0.6},
        {"turn": 9, "actor": "B", "ok": False, "delta": -2.5, "cost": 0.9},
        {"turn":10, "actor": "B", "ok": False, "delta": -3.5, "cost": 1.0},
    ]
