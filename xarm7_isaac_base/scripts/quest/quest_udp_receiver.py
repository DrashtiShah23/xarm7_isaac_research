#!/usr/bin/env python3
"""Receive fake Meta Quest UDP JSON packets and append normalized JSONL logs."""

import importlib
import importlib.util
import json
import math
import socket
from pathlib import Path
from typing import Any


LISTEN_IP = "0.0.0.0"
PORT = 5005
SUMMARY_EVERY = 30
BUFFER_SIZE = 65535

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = PROJECT_ROOT / "data" / "quest_logs"
LOG_PATH = LOG_DIR / "quest_udp_log.jsonl"

VALIDATOR_MODULE_NAME = "quest_udp_message_validator"


def _load_external_validator() -> Any | None:
    if importlib.util.find_spec(VALIDATOR_MODULE_NAME) is None:
        return None
    return importlib.import_module(VALIDATOR_MODULE_NAME)


EXTERNAL_VALIDATOR = _load_external_validator()


def _coerce_float(value: Any, field_name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be a finite number")

    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a finite number") from exc

    if not math.isfinite(number):
        raise ValueError(f"{field_name} must be a finite number")
    return number


def _coerce_bool(value: Any, field_name: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int) and value in (0, 1):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
    raise ValueError(f"{field_name} must be a boolean")


def _coerce_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be an object")
    return value


def _clamp_unit(value: float) -> float:
    return max(0.0, min(1.0, value))


def _normalize_vector3(value: Any, field_name: str) -> dict[str, float]:
    vector = _coerce_mapping(value, field_name)
    return {
        "x": _coerce_float(vector.get("x"), f"{field_name}.x"),
        "y": _coerce_float(vector.get("y"), f"{field_name}.y"),
        "z": _coerce_float(vector.get("z"), f"{field_name}.z"),
    }


def _normalize_rotation(value: Any, field_name: str) -> dict[str, float]:
    rotation = _coerce_mapping(value, field_name)
    x = _coerce_float(rotation.get("x"), f"{field_name}.x")
    y = _coerce_float(rotation.get("y"), f"{field_name}.y")
    z = _coerce_float(rotation.get("z"), f"{field_name}.z")
    w = _coerce_float(rotation.get("w"), f"{field_name}.w")

    length = math.sqrt(x * x + y * y + z * z + w * w)
    if length == 0.0:
        return {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0}

    return {
        "x": x / length,
        "y": y / length,
        "z": z / length,
        "w": w / length,
    }


def _normalize_controller(
    value: Any,
    field_name: str,
    first_button: str,
    second_button: str,
) -> dict[str, Any]:
    controller = _coerce_mapping(value, field_name)
    return {
        "position": _normalize_vector3(
            controller.get("position"),
            f"{field_name}.position",
        ),
        "rotation": _normalize_rotation(
            controller.get("rotation"),
            f"{field_name}.rotation",
        ),
        "trigger": _clamp_unit(
            _coerce_float(controller.get("trigger"), f"{field_name}.trigger")
        ),
        "grip": _clamp_unit(
            _coerce_float(controller.get("grip"), f"{field_name}.grip")
        ),
        first_button: _coerce_bool(
            controller.get(first_button),
            f"{field_name}.{first_button}",
        ),
        second_button: _coerce_bool(
            controller.get(second_button),
            f"{field_name}.{second_button}",
        ),
    }


def _normalize_packet_fallback(packet: Any) -> dict[str, Any]:
    packet_data = _coerce_mapping(packet, "packet")
    source = packet_data.get("source")
    if not isinstance(source, str) or not source.strip():
        raise ValueError("source must be a non-empty string")

    return {
        "timestamp": _coerce_float(packet_data.get("timestamp"), "timestamp"),
        "source": source,
        "right_controller": _normalize_controller(
            packet_data.get("right_controller"),
            "right_controller",
            "button_a",
            "button_b",
        ),
        "left_controller": _normalize_controller(
            packet_data.get("left_controller"),
            "left_controller",
            "button_x",
            "button_y",
        ),
    }


def _normalize_packet_with_external_validator(packet: Any) -> dict[str, Any]:
    normalize_names = (
        "normalize_packet",
        "normalize_message",
        "normalize_quest_udp_message",
        "validate_and_normalize_packet",
    )
    validate_names = (
        "validate_packet",
        "validate_message",
        "validate_quest_udp_message",
    )

    for name in normalize_names:
        candidate = getattr(EXTERNAL_VALIDATOR, name, None)
        if callable(candidate):
            result = candidate(packet)
            if isinstance(result, tuple) and len(result) >= 2:
                is_valid, normalized = result[0], result[1]
                if not is_valid:
                    raise ValueError(f"external validator rejected packet: {normalized}")
                if isinstance(normalized, dict):
                    return normalized
                return _normalize_packet_fallback(packet)
            if isinstance(result, dict):
                return result
            if result is True:
                return _normalize_packet_fallback(packet)
            raise ValueError(f"external validator rejected packet: {result}")

    for name in validate_names:
        candidate = getattr(EXTERNAL_VALIDATOR, name, None)
        if callable(candidate):
            if not candidate(packet):
                raise ValueError("external validator rejected packet")
            return _normalize_packet_fallback(packet)

    return _normalize_packet_fallback(packet)


def normalize_packet(packet: Any) -> dict[str, Any]:
    if EXTERNAL_VALIDATOR is not None:
        return _normalize_packet_with_external_validator(packet)
    return _normalize_packet_fallback(packet)


def _format_position(position: dict[str, float]) -> str:
    return f"({position['x']:.4f}, {position['y']:.4f}, {position['z']:.4f})"


def _print_summary(packet_count: int, packet: dict[str, Any]) -> None:
    right_controller = packet["right_controller"]
    left_controller = packet["left_controller"]
    print(
        f"packet_count={packet_count} "
        f"source={packet['source']} "
        f"right_pos={_format_position(right_controller['position'])} "
        f"right_trigger={right_controller['trigger']:.4f} "
        f"right_grip={right_controller['grip']:.4f} "
        f"left_pos={_format_position(left_controller['position'])} "
        f"left_trigger={left_controller['trigger']:.4f} "
        f"left_grip={left_controller['grip']:.4f}"
    )


def main() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    packet_count = 0
    invalid_count = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_IP, PORT))

    print(f"Listening for Quest UDP packets on {LISTEN_IP}:{PORT}")
    print(f"Logging normalized packets to {LOG_PATH}")
    print("Press Ctrl+C to stop.")

    try:
        with LOG_PATH.open("a", encoding="utf-8") as log_file:
            while True:
                payload, address = sock.recvfrom(BUFFER_SIZE)

                try:
                    decoded = payload.decode("utf-8")
                    packet = json.loads(decoded)
                    normalized_packet = normalize_packet(packet)
                except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
                    invalid_count += 1
                    print(f"ignored invalid packet from {address[0]}:{address[1]}: {exc}")
                    continue

                log_file.write(json.dumps(normalized_packet, separators=(",", ":")))
                log_file.write("\n")
                log_file.flush()

                packet_count += 1
                if packet_count % SUMMARY_EVERY == 0:
                    _print_summary(packet_count, normalized_packet)
    except KeyboardInterrupt:
        print(
            f"\nStopped Quest UDP receiver after {packet_count} valid packets "
            f"and {invalid_count} invalid packets."
        )
    finally:
        sock.close()


if __name__ == "__main__":
    main()
