# Isaac Sim Import Steps for xArm7 G2 Gripper

Use this pipeline for the xArm7 plus standard xArm G2 gripper URDF. This does not require ROS and does not command any hardware.

## Generated Files

- Source wrapper: `assets\urdf\xarm7_g2_gripper_wrapper.xacro`
- Generated URDF: `assets\urdf\xarm7_g2_gripper.urdf`
- Isaac-ready URDF: `assets\urdf\xarm7_g2_gripper_isaac.urdf`

## Official xArm Description Inputs

The arm path reuses the same Windows-friendly xArm7 files used for the bare import:

- `assets\urdf\xarm7_robot_macro_windows.xacro`
- `assets\urdf\xarm7.urdf_windows.xacro`
- `github_repos\xarm_ros2\xarm_description\urdf\xarm7\xarm7.transmission.xacro`
- `github_repos\xarm_ros2\xarm_description\urdf\xarm7\xarm7.gazebo.xacro`

The gripper path uses the official standard xArm gripper files:

- `github_repos\xarm_ros2\xarm_description\urdf\gripper\xarm_gripper.urdf.xacro`
- `github_repos\xarm_ros2\xarm_description\urdf\gripper\xarm_gripper.transmission.xacro`
- `github_repos\xarm_ros2\xarm_description\urdf\gripper\xarm_gripper.gazebo.xacro`

The G2 gripper is enabled with:

- `add_gripper="true"`
- `add_bio_gripper="false"`
- `gripper_version="G2"`

The official G2 mesh files used by `gripper_version="G2"` are:

- `base_link_g2.dae`
- `left_outer_knuckle_g2.dae`
- `left_finger_g2.dae`
- `left_inner_knuckle_g2.dae`
- `right_outer_knuckle_g2.dae`
- `right_finger_g2.dae`
- `right_inner_knuckle_g2.dae`

These live under `github_repos\xarm_ros2\xarm_description\meshes\gripper\xarm`.

## Regenerate

Run from the project root:

```powershell
python -m xacro -o assets\urdf\xarm7_g2_gripper.urdf assets\urdf\xarm7_g2_gripper_wrapper.xacro
```

Then convert mesh paths for Isaac Sim by replacing:

```text
../../github_repos/xarm_ros2/xarm_description/meshes
```

with the absolute project mesh path:

```text
C:/Users/Drashti/Downloads/xarm7_isaac_base/xarm7_isaac_base/github_repos/xarm_ros2/xarm_description/meshes
```

## Isaac Sim Import

When importing later, use `assets\urdf\xarm7_g2_gripper_isaac.urdf`.

Recommended importer settings:

- Fix Base: On
- Import as Articulation: On
- Self Collision: Off
- Merge Fixed Joints: On
- Convex Decomposition: On
- Import Inertia Tensor: On
- Create Physics Scene: On

Save any future imported robot as `assets\usd\xarm7_g2_gripper.usd`.
