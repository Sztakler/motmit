from psychopy import event, core
from logger import logger
from eyetracker import eyetracker

def wait_for_input(win):
    mouse = event.Mouse(win=win)
    # Wait until use depresses a mouse button (prevents ghosting of the mouse button event)
    logger.info("Waiting for mouse button release")
    while any(mouse.getPressed()):
        keys = event.getKeys(modifiers=True)
        for key, mods in keys:
            if key == 'escape':
                core.quit()
        core.wait(0.01)

    logger.info("Waiting for fresh click")
    while not any(mouse.getPressed()):
        keys = event.getKeys(modifiers=True)
        for key, mods in keys:
            if key == 'escape':
                core.quit()
            if key == 'r' and 'ctrl' in mods:
                logger.info("Manually recalibrated eyetracker")
                eyetracker.calibrate_and_start_recording()
        core.wait(0.01)
