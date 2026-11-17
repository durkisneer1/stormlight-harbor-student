"""YOUR WORK: read Using the Orchestrator and implement a 4-second animation."""
import pykraken as kn
from pykraken import fx

def build(target):
    # TODO ANIMATION: construct and return an Orchestrator targeting target.
    # Warning: squash over .8 s. Lunge: move left 16 px AND stretch over .2 s.
    # Recoil: return to (0,0) over .3 s. Settle: restore (1,1) scale over .5 s.
    # Wait 2.2 s for recovery. Finalize it; the game will call play each cycle.
    # Target coordinates are LOCAL offsets, not the boss's world position.
    # Attacks are already programmed. Do not implement attacks here.
    return None
