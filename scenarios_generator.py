from constants import Side, TrialType, Layout
from models import TrialConfig
import random
import copy

def generate_base_pool():
    pool = []
    available_numbers = list(range(1, 12))

    for trial_type in [TrialType.MOT, TrialType.MIT]:
        for probe_is_target in [True, False]:
            for target_side in Side:
                for layout in Layout:
                    positions, weight = layout.value

                    for _ in range(weight):
                        if trial_type == TrialType.MOT:
                            # In MOT all objects look the same
                            n = random.choice(available_numbers)
                            letter = random.choice(['a', 'b'])
                            selected_images = [(f"images/{n}{letter}.png", f"images/{n}{letter}.png")] * 6
                        
                        else:
                            # In MIT images are distinct and mirrored across columns
                            chosen_side_nums = random.sample(available_numbers, 3)
                            full_6_nums = chosen_side_nums + chosen_side_nums
                            selected_images = [
                                (f"images/{n}a.png", f"images/{n}b.png") for n in full_6_nums
                            ]

                        pool.append(TrialConfig(
                                        trial_type=trial_type,
                                        probe_is_target=probe_is_target,
                                        layout=layout,
                                        target_side=target_side,
                                        image_pairs=selected_images
                                    ))

    return pool * 2

def get_full_experiment(base_pool, num_blocks):
    """
    Constructs the final experiment sequence as a 2D list: [block][trial].
    """
    full_experiment = []

    for block_index in range(1, num_blocks + 1):
        block_trials = copy.deepcopy(base_pool)
        random.shuffle(block_trials)

        for trial_index, trial in enumerate(block_trials, 1):
            trial.block_number = block_index
            trial.trial_number = trial_index

        full_experiment.append(block_trials)

    return full_experiment
