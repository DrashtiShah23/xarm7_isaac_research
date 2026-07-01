#!/usr/bin/env python3
"""Send fake Meta Quest style UDP JSON packets for pipeline testing."""

import json
import math
import socket
import time


HOST = "127.0.0.1"
PORT = 5005
RATE_HZ = 30.0
SUMMARY_EVERY = 30


def _normalize_quaternion(x: float, y: float, z: float, w: float) -> dict:
    length = math.sqrt(x * x + y * y + z * z + w * w)
    if length == 0.0:
        return {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}
    return {
        "x": x / length,
        "y": y / length,
        "z": z / length,
        "w": w / length,
    }


def build_packet(elapsed: float) -> dict:
    right_position = {
        "x": 0.25 * math.sin(elapsed),
        "y": 1.1 + 0.05 * math.sin(0.5 * elapsed),
        "z": 0.45 + 0.25 * math.cos(elapsed),
    }
    left_position = {
        "x": -0.25 + 0.1 * math.sin(0.7 * elapsed),
        "y": 1.0 + 0.04 * math.cos(0.5 * elapsed),
        "z": 0.40 + 0.1 * math.cos(0.7 * elapsed),
    }

    right_rotation = _normalize_quaternion(
        0.08 * math.sin(elapsed),
        0.08 * math.cos(0.6 * elapsed),
        0.05 * math.sin(0.4 * elapsed),
        1.0,
    )
    left_rotation = _normalize_quaternion(
        0.06 * math.sin(0.8 * elapsed),
        0.06 * math.cos(0.5 * elapsed),
        0.04 * math.sin(0.3 * elapsed),
        1.0,
    )

    right_trigger = 0.5 + 0.5 * math.sin(elapsed)
    right_grip = 0.5 + 0.5 * math.cos(0.8 * elapsed)
    left_trigger = 0.5 + 0.5 * math.sin(0.9 * elapsed)
    left_grip = 0.5 + 0.5 * math.cos(0.6 * elapsed)

    return {
        "timestamp": round(elapsed, 3),
        "source": "fake_meta_quest",
        "right_controller": {
            "position": {k: round(v, 4) for k, v in right_position.items()},
            "rotation": {k: round(v, 4) for k, v in right_rotation.items()},
            "trigger": round(right_trigger, 4),
            "grip": round(right_grip, 4),
            "button_a": int(elapsed // 3) % 2 == 0,
            "button_b": int(elapsed // 4) % 2 == 1,
        },
        "left_controller": {
            "position": {k: round(v, 4) for k, v in left_position.items()},
            "rotation": {k: round(v, 4) for k, v in left_rotation.items()},
            "trigger": round(left_trigger, 4),
            "grip": round(left_grip, 4),
            "button_x": int(elapsed // 3) % 2 == 1,
            "button_y": int(elapsed // 5) % 2 == 0,
        },
    }


def main() -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    interval = 1.0 / RATE_HZ
    packet_count = 0
    start = time.monotonic()

    print(f"Sending fake Meta Quest UDP packets to {HOST}:{PORT} at {RATE_HZ:.0f} Hz")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            elapsed = time.monotonic() - start
            packet = build_packet(elapsed)
            payload = json.dumps(packet).encode("utf-8")
            sock.sendto(payload, (HOST, PORT))
            packet_count += 1

            if packet_count % SUMMARY_EVERY == 0:
                right_pos = packet["right_controller"]["position"]
                print(
                    f"fake packet count={packet_count} "
                    f"right_pos=({right_pos['x']}, {right_pos['y']}, {right_pos['z']}) "
                    f"right_trigger={packet['right_controller']['trigger']:.3f} "
                    f"right_grip={packet['right_controller']['grip']:.3f}"
                )

            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\nStopped after {packet_count} fake packets.")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
