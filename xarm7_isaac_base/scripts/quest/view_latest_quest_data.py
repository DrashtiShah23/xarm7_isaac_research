#!/usr/bin/env python3
"""Print the latest logged Meta Quest UDP packet and Isaac marker mapping."""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_PATH = PROJECT_ROOT / "data" / "quest_logs" / "quest_udp_log.jsonl"


def quest_to_isaac(position: dict) -> dict:
    return {
        "x": position["z"],
        "y": -position["x"],
        "z": position["y"],
    }


def load_latest_valid_record(log_path: Path) -> dict | None:
    if not log_path.exists():
        return None

    latest = None
    with log_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                latest = json.loads(line)
            except json.JSONDecodeError:
                continue
    return latest


def main() -> None:
    record = load_latest_valid_record(LOG_PATH)
    if record is None:
        print(
            "No Quest log found. Start quest_udp_receiver.py first, "
            "then run fake_meta_quest_stream.py."
        )
        return

    right = record["right_controller"]
    left = record["left_controller"]
    marker = quest_to_isaac(right["position"])

    print(f"timestamp: {record.get('timestamp')}")
    print(f"source: {record.get('source')}")
    print(
        "right controller position: "
        f"x={right['position']['x']}, y={right['position']['y']}, z={right['position']['z']}"
    )
    print(
        "right controller rotation: "
        f"x={right['rotation']['x']}, y={right['rotation']['y']}, "
        f"z={right['rotation']['z']}, w={right['rotation']['w']}"
    )
    print(f"right trigger: {right['trigger']}")
    print(f"right grip: {right['grip']}")
    print(
        "left controller position: "
        f"x={left['position']['x']}, y={left['position']['y']}, z={left['position']['z']}"
    )
    print(f"left trigger: {left['trigger']}")
    print(f"left grip: {left['grip']}")
    print(
        "converted Isaac marker position: "
        f"x={marker['x']}, y={marker['y']}, z={marker['z']}"
    )


if __name__ == "__main__":
    main()
