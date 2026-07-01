# Isaac Sim Import Steps for xArm7

Follow these steps to import the prepared xArm7 URDF into Isaac Sim and save the robot and scene assets.

## Prerequisites

- Valid Isaac-friendly URDF: `assets\urdf\xarm7_isaac.urdf`
- Mesh files under: `github_repos\xarm_ros2\xarm_description\meshes`
- Output folders ready: `assets\usd`, `scenes`, `screenshots`

## Import Procedure

1. Open Isaac Sim.
2. Create a new scene.
3. Add a Ground Plane.
4. Enable the URDF Importer from **Window > Extensions**.
5. Use **File > Import**.
6. Select `assets\urdf\xarm7_isaac.urdf`.
7. Use these import settings:
   - **Fix Base:** On
   - **Import as Articulation:** On
   - **Self Collision:** Off
   - **Merge Fixed Joints:** On
   - **Convex Decomposition:** On
   - **Import Inertia Tensor:** On
   - **Create Physics Scene:** On
8. Save the imported robot as `assets\usd\xarm7.usd`.
9. Create a reusable scene with:
   - Ground plane
   - Light
   - Camera
   - xArm7 robot
10. Save the scene as `scenes\xarm7_basic_scene.usd`.
11. Take screenshots and save them in `screenshots`.

## Full URDF Path

`C:\Users\Drashti\Downloads\xarm7_isaac_base\xarm7_isaac_base\assets\urdf\xarm7_isaac.urdf`

## Expected Output Files

- `assets\usd\xarm7.usd`
- `scenes\xarm7_basic_scene.usd`
- Screenshot images in `screenshots`

## Regenerate Isaac URDF from VS Code

If you regenerate `assets\urdf\xarm7.urdf`, rerun:

```powershell
.\scripts\windows\prepare_isaac_urdf.ps1
```
