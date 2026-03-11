from mot_response_handler import MOTResponseHandler
from mit_response_handler import MITResponseHandler
from psychopy import event, core
from utils.input import wait_for_input

def handle_response(win, trial_config, is_practice=False):
    """
    Manages the response phase and returns trial results.
    """
    win.mouseVisible = True # Ensure cursor is visible for selection

    clicked_orbit_id = "N/A"
    clicked_item_idx = "N/A"
    
    if trial_config.trial_type.name == "MOT":
        handler = MOTResponseHandler(win)
        handler.get_response()
        
        # We check if the participant correctly identified the probe as target/distractor
        is_correct = handler.check_correctness(
            is_target_probed=trial_config.probe_is_target
        )

        clicked_orbit_id = getattr(handler, 'clicked_orbit_id', "N/A")
        clicked_item_idx = getattr(handler, 'clicked_item_idx', "N/A")
    else:
        handler = MITResponseHandler(win)
        handler.get_response(trial_config.all_orbits)
        
        # For MIT, identify the specific image that was used as the probe
        probed_obj = trial_config.probe_orbit
        correct_path = probed_obj.image_pair[trial_config.probe_index]
        
        is_correct = handler.check_correctness(
            probe_image_path=correct_path,
            is_target_probed=trial_config.probe_is_target,
            is_practice=is_practice
        )

        clicked_orbit_id = handler.clicked_orbit_id
        clicked_item_idx = handler.clicked_item_idx

    response_time = handler.response_time
    clicked_val = handler.clicked_object

    # Show feedback based on the result
    handler.display_feedback()
    
    # Wait for acknowledgment to finish the trial
    # event.waitKeys(keyList=['mouse1', 'space'])
    wait_for_input(win)

    
    return is_correct, clicked_val, response_time, clicked_orbit_id, clicked_item_idx
