import csv
import os
from config import fieldnames  # Using the global fieldnames list from config.py

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
        side_map = {0: 'L', 1: 'R'}
        
        # Consolidate stimulus information into pipe-separated strings
        # to avoid breaking CSV columns with commas
        all_images = [img for pair in trial_config.images_paths for img in pair]
        target_info = [f"Orb:{t.orbit_index}_Circ:{t.circle_index}" for t in trial_config.targets]

        with open(self.filename, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            
            # Prepare the row dictionary matching fieldnames exactly
            row_data = {
                'UserID': self.user_form.id,
                'First Name': self.user_form.first_name,
                'Last Name': self.user_form.last_name,
                'Age': self.user_form.age,
                'Sex': self.user_form.sex,
                'Handedness': self.user_form.handedness,
                'E-mail': self.user_form.email,
                'Trial Number': trial_config.trial_number,
                'Block number': trial_config.block_number,
                'Trial Type': trial_config.trial_type.name,
                'Target Set Size': trial_config.target_set_size,
                'Target Side': side_map.get(trial_config.targets_side, 'N/A'),
                'Layout': str(trial_config.layout),
                'Highlighted Target': trial_config.probe_object.is_target,
                'Response': result_data['clicked_object'],
                'Correct Response': result_data['correct_answer'],
                'Correctness': result_data['is_correct'],
                'Response Time': f"{result_data['rt']:.3f}",
                'TrialID': trial_config.id,
                'ConditionID': trial_config.condition_id,
                'Images': "|".join(all_images),
                'Targets': "|".join(target_info)
            }
            
            # Ensure we only write keys that exist in the config fieldnames
            filtered_row = {k: v for k, v in row_data.items() if k in self.fieldnames}
            writer.writerow(filtered_row)
