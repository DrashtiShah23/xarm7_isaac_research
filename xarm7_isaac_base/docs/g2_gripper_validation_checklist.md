# G2 Gripper Import Validation Checklist

Use this checklist after generating `assets\urdf\xarm7_g2_gripper_isaac.urdf` and before any Isaac Sim import.

- [ ] `assets\urdf\xarm7_g2_gripper.urdf` exists.
- [ ] `assets\urdf\xarm7_g2_gripper_isaac.urdf` exists.
- [ ] Isaac URDF file size is larger than `assets\urdf\xarm7_isaac.urdf`.
- [ ] Isaac URDF link count is greater than the bare xArm7 URDF.
- [ ] Isaac URDF joint count is greater than the bare xArm7 URDF.
- [ ] Isaac URDF mesh filename count is greater than the bare xArm7 URDF.
- [ ] Missing mesh file count is zero.
- [ ] Remaining `$(find xarm_description)` occurrences are zero.
- [ ] Gripper links include `xarm_gripper_base_link`, `left_outer_knuckle`, `left_finger`, `left_inner_knuckle`, `right_outer_knuckle`, `right_finger`, `right_inner_knuckle`, and `link_tcp`.
- [ ] Gripper joints include `gripper_fix`, `drive_joint`, `left_finger_joint`, `left_inner_knuckle_joint`, `right_outer_knuckle_joint`, `right_finger_joint`, `right_inner_knuckle_joint`, and `joint_tcp`.
- [ ] G2 mesh filenames resolve to the official `*_g2.dae` files under `github_repos\xarm_ros2\xarm_description\meshes\gripper\xarm`.

Isaac Sim should not be opened until the file checks above pass.
