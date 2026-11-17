"""YOUR WORK: two bug fixes and one physics implementation. See docs/LESSON.md."""
import pykraken as kn
SPEED=110.0
GRAVITY=700.0
JUMP_SPEED=-255.0

def horizontal_speed(left, right):
    # BUG 1: left moves right; both directions should cancel each other.
    return (int(right)+int(left))*SPEED

def step(player, dt, left, right, jump_pressed):
    # TODO PHYSICS: replace the temporary horizontal-only movement.
    # Integrate vertical velocity using GRAVITY and dt. Launch a grounded
    # player on jump_pressed, with JUMP_SPEED (only if velocity.y >= 0).
    # Cap falling speed at 450.
    # Assign a Vec2 velocity, call move_and_slide(dt), return whether you jumped.
    player.velocity=kn.Vec2(horizontal_speed(left,right),0)
    player.move_and_slide(dt)
    return False

def can_take_hit(invulnerability):
    # BUG 2: standing in one hazard loses all three hearts immediately.
    # A hit should be allowed only after the protection timer has expired.
    return True
