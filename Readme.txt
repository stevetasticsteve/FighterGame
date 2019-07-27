Steve's first Pygame game - Flyover

version 1.01
A playable experience. Tests totally broken after refactor, but not really needed anymore.

Ways to improve current version:
-Add background music
-Be able to press 2 buttons at once
-Fix and expand tests

The game will be about flying a fighter jet around and shooting down as many other planes as possible before you are shot down yourself or the time runs out. It will be top down 2D where the plane flies over a tiled map. Planes will have cannon shells, missiles and fuel that can be replenished at an airfield.
Controls will be to speed up and slow down (there's always constant forward motion), rotate and fire.

A large map will be generated and the camera will place the player at the center as they fly around the map looking for enemy planes.

Intended features: (x means (minimally) done)
x Tiled map.
x Player plane stays central in screen and map scrolls underneath.
- Player health.
- High score system.
x 64 pixel sprites and tiles.
- Throttle, speed up or slow down your plane. Higher speeds use more fuel and also limit turning speed.
- Consumable ammo supply.
- Refuel and rearm at your side's airfield.
- UI showing health, throttle ammo and fuel.
x Enemy planes that move semi randomly.
x Sound effects.
x Player can't fly off the map edge into infinity.

Extra bonus features:
- Radar mini-map
- Missile installations by your own airfield (on your side) and enemy missile installations