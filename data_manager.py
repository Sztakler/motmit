import csv
import os
from config import fieldnames  # Using the global fieldnames list from config.py
from constants import Side

class DataManager:
    """
    Handles trial-by-trial data logging to CSV.
    Uses the header structure defined in config.py.
    """
    def __init__(self, filename, user_form):
        self.filename = filename
        self.user_form = user_form
        self.fieldnames = fieldnames
        
        # Ensure the data directory exists
        directory = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        # Write header only if the file is being created for the first time
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()

    def save_trial_data(self, trial_config, result_data):
        """
        Maps trial results and configuration to the CSV field structure.
        """
        # Mapping side index to human-readable label
        side_map = {Side.LEFT: 'L', Side.RIGHT: 'R'}
        
        # Consolidate stimulus information into pipe-separated strings
        # to avoid breaking CSV columns with commas
        all_images = []
        if trial_config.trial_type.name == "MIT":
            for pair in trial_config.images_paths:
                all_images.append(os.path.basename(pair[0]))
                all_images.append(os.path.basename(pair[1]))
        # Only one path for MOT, since all images are identical in this task
        else:
            all_images.append(os.path.basename(trial_config.images_paths[0][0]))

        target_info = [f"Orb:{o.orbit_id}_Tidx:{o.target_idx}" for o in trial_config.active_orbits]

        if trial_config.trial_type.name == "MIT":
            if trial_config.probe_is_target:
                correct_val = trial_config.probe_orbit.image_pair[trial_config.probe_index]
            else:
                correct_val = "images/0a.png"
        else:
            # For MOT text information will suffice
            correct_val = "target" if trial_config.probe_is_target else "distractor"

        probe_orbit_id = trial_config.probe_orbit.orbit_id
        probe_item_idx = trial_config.probe_index
        clicked_orbit_id = result_data.get('clicked_orbit_id', 'N/A')
        clicked_item_idx = result_data.get('clicked_item_idx', 'N/A')
        status = result_data.get('status', 'unknown')
        raw_res = result_data.get('clicked_object')
        response = raw_res if raw_res else "N/A"

        with open(self.filename, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            
            # Prepare the row dictionary matching fieldnames exactly
            row_data = {
                    'UserID': self.user_form.id,
                    'Age': self.user_form.age,
                    'Sex': self.user_form.sex,
                    'Handedness': self.user_form.handedness,
                    'Trial Number': trial_config.trial_number,
                    'Block number': trial_config.block_number,
                    'Trial Type': trial_config.trial_type.name,
                    'Target Set Size': trial_config.target_set_size,
                    'Target Side': side_map.get(trial_config.target_side, 'N/A'),
                    'Probe_Orbit_ID': probe_orbit_id,
                    'Probe_Item_Idx': probe_item_idx,
                    'Clicked_Orbit_ID': clicked_orbit_id,
                    'Clicked_Item_Idx': clicked_item_idx,
                    
                    'Layout': trial_config.layout, 
                    'Highlighted Target': trial_config.probe_is_target,
                    'Response': response,
                    'Correct Response': correct_val,
                    'Correctness': 1 if result_data['is_correct'] else 0,
                    'Response Time': f"{result_data['response_time']:.3f}",
                    'Status': status,
                    'TrialID': trial_config.id,
                    'ConditionID': trial_config.condition_id,
                    'Images': "|".join(all_images),
                    'Targets': "|".join(target_info)
                }
            
            filtered_row = {k: v for k, v in row_data.items() if k in self.fieldnames}
            writer.writerow(filtered_row)
