#!/usr/bin/env python3
"""Validate fake Meta Quest UDP message shape and Isaac mapping."""

import math
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
QUEST_DIR = PROJECT_ROOT / "scripts" / "quest"
sys.path.insert(0, str(QUEST_DIR))

from fake_meta_quest_stream import build_packet  # noqa: E402
from view_latest_quest_data import quest_to_isaac  # noqa: E402


REQUIRED_TOP_LEVEL = ("timestamp", "source", "right_controller", "left_controller")
CONTROLLER_FIELDS = (
    "position",
    "rotation",
    "trigger",
    "grip",
)
POSITION_FIELDS = ("x", "y", "z")
ROTATION_FIELDS = ("x", "y", "z", "w")


class QuestMessageValidationTests(unittest.TestCase):
    def test_build_packet_has_required_structure(self) -> None:
        packet = build_packet(1.5)

        for field in REQUIRED_TOP_LEVEL:
            self.assertIn(field, packet)
        self.assertEqual(packet["source"], "fake_meta_quest")

    def test_controller_fields_and_ranges(self) -> None:
        packet = build_packet(2.0)

        for side in ("right_controller", "left_controller"):
            controller = packet[side]
            for field in CONTROLLER_FIELDS:
                self.assertIn(field, controller)

            for axis in POSITION_FIELDS:
                self.assertIn(axis, controller["position"])
                self.assertIsInstance(controller["position"][axis], (int, float))

            for axis in ROTATION_FIELDS:
                self.assertIn(axis, controller["rotation"])
                self.assertIsInstance(controller["rotation"][axis], (int, float))

            self.assertGreaterEqual(controller["trigger"], 0.0)
            self.assertLessEqual(controller["trigger"], 1.0)
            self.assertGreaterEqual(controller["grip"], 0.0)
            self.assertLessEqual(controller["grip"], 1.0)

    def test_right_motion_formulas(self) -> None:
        t = 1.0
        packet = build_packet(t)
        pos = packet["right_controller"]["position"]

        self.assertAlmostEqual(pos["x"], 0.25 * math.sin(t), places=3)
        self.assertAlmostEqual(pos["y"], 1.1 + 0.05 * math.sin(0.5 * t), places=3)
        self.assertAlmostEqual(pos["z"], 0.45 + 0.25 * math.cos(t), places=3)

    def test_left_motion_formulas(self) -> None:
        t = 2.0
        packet = build_packet(t)
        pos = packet["left_controller"]["position"]

        self.assertAlmostEqual(pos["x"], -0.25 + 0.1 * math.sin(0.7 * t), places=3)
        self.assertAlmostEqual(pos["y"], 1.0 + 0.04 * math.cos(0.5 * t), places=3)
        self.assertAlmostEqual(pos["z"], 0.40 + 0.1 * math.cos(0.7 * t), places=3)

    def test_button_fields_exist(self) -> None:
        packet = build_packet(0.0)

        self.assertIn("button_a", packet["right_controller"])
        self.assertIn("button_b", packet["right_controller"])
        self.assertIn("button_x", packet["left_controller"])
        self.assertIn("button_y", packet["left_controller"])
        self.assertIsInstance(packet["right_controller"]["button_a"], bool)
        self.assertIsInstance(packet["left_controller"]["button_y"], bool)

    def test_quest_to_isaac_mapping(self) -> None:
        quest_pos = {"x": 0.25, "y": 1.1, "z": 0.45}
        isaac_pos = quest_to_isaac(quest_pos)

        self.assertAlmostEqual(isaac_pos["x"], 0.45)
        self.assertAlmostEqual(isaac_pos["y"], -0.25)
        self.assertAlmostEqual(isaac_pos["z"], 1.1)


if __name__ == "__main__":
    unittest.main()
