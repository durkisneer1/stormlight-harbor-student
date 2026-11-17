# Stormlight Harbor: 90-minute workshop

Mission: cross the harbor, survive the Tide Warden, and relight the exit. Work in `student/`. Run `python play.py student` from the project folder. Close the game, save your changes, then rerun. You need Python basics (functions, conditions, variables) and Tiled installed.

## 0–8 minutes: investigate

Run the starter. Walk both directions. Try to jump. Press B to visit Boss Lab and hold J. Note three differences between your expectations and what happens. You can press R to return to the start. Read each TODO before editing.

## 8–18 minutes: fix two bugs

Open `student/movement.py`.

1. `horizontal_speed`: right is positive x; left is negative x. Fix left movement. Holding both directions should produce zero speed.
2. `can_take_hit`: a hit starts a one-second protection timer. Return true only when the timer has expired. Test by standing in the boss's body in Boss Lab. You should lose at most one heart per second, rather than all three immediately.

Explain the cause of each bug to your partner before changing it.

## 18–38 minutes: implement physics

Read [CharacterBody](https://krakenengine.org/api/) and [Vec2](https://krakenengine.org/api/). Use the API index to find each named class. Offline excerpts are supplied in `docs/API_NOTES.md`. The installed API is also available through `help(kn.physics.CharacterBody)`.

Replace the temporary implementation of `step`:

- Use the body's current y velocity; add acceleration `GRAVITY * dt`.
- Launch only when `jump_pressed` and `player.is_on_floor()` are both true, and the current y velocity is nonnegative. This avoids a stale floor flag just after takeoff.
- Up is negative y. Use `JUMP_SPEED`, not its absolute value.
- Cap falling speed at 450 pixels per second.
- Assign a `kn.Vec2` velocity with your horizontal speed and calculated vertical speed.
- Call `move_and_slide(dt)` and return whether a jump occurred.

The engine already supplies fixed steps, jump press detection, collision bodies, and respawning. CharacterBody resolves motion; this exercise supplies gravity explicitly. Do not also change `player.pos`, or multiply the velocity by dt a second time.

Check: left/right work; you fall when walking off an edge; a standing jump lands; holding Space does not make repeated jumps; pressing Space in midair does not double-jump. Estimate jump height with `speed² / (2 * gravity)` and flight time with `2 * speed / gravity`.

## 38–58 minutes: build the harbor in Tiled

Open `student/harbor.tmx`. Keep the map finite, orthogonal, with 18×18 tiles and CSV tile layer data (Map Properties → Tile Layer Format).

1. Select **Platforms** and paint islands between the start and boss arena. Every occupied tile on this layer is solid automatically. Erasing a tile removes its collision too.
2. Start with gaps of 2–3 tiles and upward steps of at most 2 tiles. The reference constants allow roughly 92 pixels of rise and 80 pixels of travel back to the same height; leave landing margin.
3. Paint plants and signs on **Scenery**, which has no collision.
4. Toggle **Build guide - editor only** for suggested landing rectangles. These are guides, not solid ground; paint actual tiles. The game never draws this layer.
5. Keep the **Markers** point objects named Spawn, Checkpoint, Boss and Exit. Move Checkpoint onto a safe island if your route changes. The default checkpoint is near x=1000, y=260.
6. Keep the supplied boss arena (x=1512 onward) and boss/exit positions for this lesson. Save and rerun. Test every jump in both directions.

[Tiled: editing tile layers](https://doc.mapeditor.org/en/stable/manual/editing-tile-layers/) explains the stamp brush, eraser, and selection tools. Use B for the stamp brush and E for the eraser while Tiled has focus.

## 58–73 minutes: animate the Warden

Read [Using the Orchestrator](https://krakenengine.org/guides/game-essentials/using-orchestrator/). Implement `build(target)` in `student/boss_animation.py`.

Create an Orchestrator attached to the supplied transform. Sequence a .8-second squash; a .2-second parallel lunge and stretch; a .3-second return to local position (0,0); a .5-second return to scale (1,1); and a 2.2-second recovery wait. These total four seconds, matching the combat cycle. Use at least one easing function. Finalize and return the object; the framework plays it each cycle.

The target is a visual offset, so a lunge goes to (-16,0), not to the world boss coordinates. Do not animate hitboxes or program new attacks. Effects are consumed by the timeline; create fresh effects for every step. Press B to test immediately. The boss should warn, lunge, recoil, and return to exactly its starting shape and position across several cycles.

## 73–83 minutes: samples and streams

Use `help(kn.mixer.load_sample)`, `help(kn.mixer.load_stream)`, and `help(kn.mixer.Stream)` or the [API index](https://krakenengine.org/api/) entries for mixer.Sample and mixer.Stream.

Implement `Audio` in `student/audio.py`. Load five short WAVs as Samples and retain them in a dictionary. Load `harbor.wav` as a Stream, retain it, set looping and volume, and start playback with a .5-second fade. Implement named sample playback and stop the stream in `close`. Load only once, never in the frame loop. The framework already calls each event.

Check: music loops; jump and shot effects overlap the music; M mutes everything; closing the window stops audio. The optional `assets/audio/harbor.mid` contains the score's notes for editing in a MIDI sequencer. The game streams the supplied WAV rendering, not the MIDI file.

## 83–90 minutes: playtest and explain

Trade places. Can your partner finish your route and beat the boss? Does the checkpoint work? Does the Warden give a clear warning? Review your changes against the checks above. Explain why acceleration uses dt, why hit protection needs a condition, and why long music uses a Stream. Save your work.
