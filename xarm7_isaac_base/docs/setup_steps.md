# Step by step setup

## Phase 1

1. Open Isaac Sim.
2. Create a new empty scene.
3. Add a ground plane.
4. Press Play once.
5. Stop the simulation.
6. Save the scene as scenes/xarm7_blank_scene.usd.

## Phase 2

1. Clone the official xArm ROS 2 repository into github_repos.
2. Find xArm7 description files inside the cloned repository.
3. Open the URDF importer in Isaac Sim.
4. Import xArm7.
5. Save the imported robot as assets/usd/xarm7.usd.

## Phase 3

1. Open assets/usd/xarm7.usd.
2. Check scale.
3. Check that the base is fixed.
4. Check that all seven joints exist.
5. Press Play.
6. Confirm the robot does not fall, explode, or jitter.
7. Take a screenshot and save it in screenshots.

## Phase 4

1. Create a reusable Isaac Sim scene.
2. Add ground plane.
3. Add lighting.
4. Add camera.
5. Add xArm7 USD asset.
6. Save as scenes/xarm7_basic_scene.usd.

## Phase 5

1. Create a simple simulated motion demo.
2. Move one joint by a small safe amount.
3. Log joint positions.
4. Save screenshots or video evidence.
