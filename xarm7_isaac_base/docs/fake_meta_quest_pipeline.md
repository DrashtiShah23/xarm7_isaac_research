# Fake Meta Quest Pipeline

## Why fake data is being used

Fake Meta Quest data lets us verify the UDP receiver, logger, and Isaac marker mapping before using the real Quest headset. This keeps development safe: no real Quest app, no real robot motion, and no real gripper commands are required during early testing.

## How to run

Open three terminals from the project root:

### Terminal 1

```powershell
python scripts\quest\quest_udp_receiver.py
```

### Terminal 2

```powershell
python scripts\quest\fake_meta_quest_stream.py
```

### Terminal 3

```powershell
python scripts\quest\view_latest_quest_data.py
```

Optional marker planning check:

```powershell
python scripts\quest\quest_data_to_marker_plan.py
```

## Expected result

- The receiver prints incoming packets.
- `data\quest_logs\quest_udp_log.jsonl` grows with one JSON object per line.
- `view_latest_quest_data.py` prints the latest fake controller pose and converted Isaac marker position.
- `quest_data_to_marker_plan.py` prints a target marker position from the latest logged data.

## What this proves

- UDP pipeline works
- JSON format works
- Logging works
- Quest to Isaac coordinate mapping placeholder works

## What this does not prove

- Real Quest app connection
- Real robot control
- Real gripper control
- Final calibrated coordinate mapping

## Coordinate mapping placeholder

Right controller Quest position is converted to Isaac marker position using:

- `isaac_x = quest z`
- `isaac_y = -quest x`
- `isaac_z = quest y`

This is a placeholder mapping for pipeline testing only.

## Safety notes

- Do not use ROS for this pipeline.
- Do not move or command the real robot.
- Do not open or close the real G2 gripper.
- Do not delete existing Isaac Sim files.
