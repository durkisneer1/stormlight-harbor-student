# Offline API excerpts

Extracted from the installed Kraken Engine 1.8.0 docstrings. Consult these when the website is unavailable. Upstream source: https://krakenengine.org/api/ .

## CharacterBody.move_and_slide

```text
move_and_slide(self, delta: float = -1.0) -> None

Perform movement and collision resolution for the character.

This method moves the character according to the velocity property and resolves
collisions by sliding along surfaces. It also updates the floor/ceiling/wall
contact states.

Args:
    delta (float, optional): The time step to use for movement.
                             Defaults to -1.0, which uses the frame delta.
```

## CharacterBody.is_on_floor

```text
is_on_floor(self) -> bool

Check if the character is currently in contact with the floor.

Returns:
    bool: True if the character is on the floor, False otherwise.
```

## Orchestrator

```text
Timeline animator for Transform objects.

Allows chaining effects to create complex animations that play over time.
Effects can run sequentially or in parallel.

Attributes:
    finalized (bool): Whether the orchestrator has been finalized.
    playing (bool): Whether the animation is currently playing.
    finished (bool): Whether the animation has completed.
    looping (bool): Whether the animation should loop when finished.

Methods:
    parallel(*effects): Add multiple effects to run in parallel.
    then(effect): Add a single effect to the timeline.
    finalize(): Finalize the orchestrator, preventing further edits.
    play(): Start playing the animation from the beginning.
    pause(): Pause the animation at the current position.
    resume(): Resume a paused animation.
    stop(): Stop the animation and reset to the beginning.
    rewind(): Reset the animation to the beginning without stopping.
```

## Orchestrator.parallel

```text
parallel(self, *effects: pykraken._pykraken.fx.Effect) -> pykraken._pykraken.Orchestrator

Add multiple effects to run in parallel.

Args:
    *effects: Variable number of Effect objects to run simultaneously.

Returns:
    Orchestrator: Self for method chaining.
```

## fx.move_to

```text
move_to(pos: pykraken._pykraken.Vec2, dur: float = 0.0, ease: collections.abc.Callable[[float], float] | None = None) -> pykraken._pykraken.fx.Effect

Create a move-to effect.

Args:
    pos (Vec2): Target position.
    dur (float): Duration in seconds.
    ease (callable): Easing function (t -> t).

Returns:
    Effect: The move-to effect.
```

## fx.scale_to

```text
scale_to(scale: pykraken._pykraken.Vec2, dur: float = 0.0, ease: collections.abc.Callable[[float], float] | None = None) -> pykraken._pykraken.fx.Effect

Create a scale-to effect.

Args:
    scale (Vec2): Target scale exact dimensions.
    dur (float): Duration in seconds.
    ease (callable): Easing function (t -> t).

Returns:
    Effect: The scale-to effect.
```

## fx.wait

```text
wait(dur: float) -> pykraken._pykraken.fx.Effect

Create a wait/delay effect.

Args:
    dur (float): Duration to wait in seconds.

Returns:
    Effect: The wait effect.
```

## mixer.load_sample

```text
load_sample(path: str | os.PathLike, predecode: bool = True) -> pykraken._pykraken.mixer.Sample

        Load an audio sample (SFX) from disk.

        Args:
            path (str | os.PathLike[str]): File path to load.
            predecode (bool): Whether to decode into memory now. Defaults to True.

        Returns:
            Sample: The loaded audio object.
```

## mixer.load_stream

```text
load_stream(path: str | os.PathLike, predecode: bool = False) -> pykraken._pykraken.mixer.Stream

        Load an audio stream (Music) from disk.

        Args:
            path (str | os.PathLike[str]): File path to load.
            predecode (bool): Whether to decode into memory now. Defaults to False.

        Returns:
            Stream: The loaded audio object.
```

## Stream.play

```text
play(self, fade_in: float = 0.0) -> None

            Start audio playback.

            Args:
                fade_in (float): Fade in duration in seconds. Defaults to 0.0.
```

## Workshop conventions

`player.velocity` is a Vec2. Read/write x and y. `player.pos` is in pixels. Set `player.capsule_shape` once. `music.looping` and `music.volume` are writable properties. `sample.play()` starts a short sound. `music.stop()` stops the stream. Keep objects alive in instance fields. `orch.finalize()` prepares the timeline; `orch.play()` rewinds and starts it. Orchestrators tick automatically during event polling.
