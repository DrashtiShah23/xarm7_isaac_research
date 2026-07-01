# Isaac Sim Import Validation Checklist

Use this checklist after importing `assets\urdf\xarm7_isaac.urdf` into Isaac Sim.

- [ ] Robot visible in viewport.
- [ ] Robot scale looks correct.
- [ ] Base stays fixed when pressing Play.
- [ ] Stage panel shows xArm7 robot.
- [ ] Links exist from base to link7.
- [ ] Seven revolute joints exist.
- [ ] Meshes are visible.
- [ ] No missing mesh errors in Output Log.
- [ ] Save robot USD to `assets\usd\xarm7.usd`.
- [ ] Save scene USD to `scenes\xarm7_basic_scene.usd`.
- [ ] Take evidence screenshots.

## Notes

- Import file: `assets\urdf\xarm7_isaac.urdf`
- Expected robot links: `link_base`, `link1`, `link2`, `link3`, `link4`, `link5`, `link6`, `link7`
- Expected revolute joints: `joint1` through `joint7`
- Store screenshots in `screenshots`
