# xArm7 Isaac Sim Research Base

This repository is a starter workspace for xArm7 research using Isaac Sim, Isaac Lab, and later ROS 2.

## Main goal

Import xArm7 into Isaac Sim, save a reusable USD robot asset, validate articulation and physics, then build simple control demos.

## First milestone

Open Isaac Sim, create a blank scene, import the xArm7 robot model, save it as assets/usd/xarm7.usd, then save a reusable scene as scenes/xarm7_basic_scene.usd.

## Folder map

assets/usd stores converted Isaac Sim USD robot assets.

assets/urdf stores copied or generated URDF files.

assets/meshes stores copied mesh files if needed.

scenes stores Isaac Sim scene files.

screenshots stores proof images for the task tracker.

notes stores lab notes and setup notes.

docs stores step by step instructions.

scripts/python stores Python helper scripts.

scripts/windows stores Windows setup scripts.

scripts/ubuntu stores Ubuntu setup scripts.

github_repos stores cloned external repositories.

experiments stores logs and results.

## Fake Meta Quest pipeline

Use fake UDP packets to verify the Quest receiver, logger, and Isaac marker mapping before connecting a real Quest headset.

```powershell
python scripts\quest\quest_udp_receiver.py
python scripts\quest\fake_meta_quest_stream.py
python scripts\quest\view_latest_quest_data.py
```

See `docs/fake_meta_quest_pipeline.md` for full instructions.

## Official repositories to clone manually

https://github.com/xArm-Developer/xarm_ros2

https://github.com/xArm-Developer/xArm-Python-SDK
