import random
import uuid
from constants import Side, OrbitPosition, TrialType

class Orbit:
    def __init__(self, position: OrbitPosition, side: Side, has_target: bool, image_pair: tuple):
        self.position = position
        self.side = side
        self.has_target = has_target
        self.image_pair = image_pair
        
        self.orbit_id = (self.side.value * 3) + self.position.value
        self.target_idx = random.choice([0, 1])
        self.distractor_idx = 1 - self.target_idx

        @property
        def target_image(self):
            return self.image_pair[self.target_idx]

        @property
        def distractor_image(self):
            return self.image_pair[self.distractor_idx]

class TrialConfig:
    def __init__(self, trial_type: TrialType, probe_is_target: bool, layout, target_side: Side, image_pairs: list):
        self.id = str(uuid.uuid4())[:8] # Short unique ID for the trial instance
        self.trial_type = trial_type # MOT or MIT
        self.probe_is_target = probe_is_target
        self.layout = layout
        self.target_side = target_side
        self.trial_number = 0 # To be set by the generator
        self.block_number = 0 # To be set by the generator
        self.condition_id = self.encode_conditions_binary()
        self.active_orbits = []
        self.all_orbits= []
        positions, _ = layout.value

        img_idx = 0

        for side in Side:
            for pos in OrbitPosition:
                has_target= (side == target_side and pos in positions)

                self.all_orbits.append(Orbit(
                                            position=pos,
                                            side=side,
                                            has_target=has_target,
                                            image_pair=image_pairs[img_idx]
                                        ))
                img_idx += 1

        # Selecting probe for highlighting
        self.active_orbits = [o for o in self.all_orbits if o.has_target]
        self.probe_orbit = random.choice(self.active_orbits)

        for o in self.active_orbits:
            print(o.target_idx)

        if self.probe_is_target:
            self.probe_index = self.probe_orbit.target_idx
            self.correct_answer = "target"
        else:
            self.probe_index = self.probe_orbit.distractor_idx
            self.correct_answer = "distractor"
        

    def encode_conditions_binary(self):
        """
        Encodes trial parameters into a numeric string for legacy data analysis.
        Mapping: TrialType (MOT:0, MIT:1), Side (L:0, R:1), SetSize (2:0, 3:1), Layout (specific: 0-3)
        """
        # 1. Map Trial Type
        type_map = {TrialType.MOT: "0", TrialType.MIT: "1"}
        type_enc = type_map.get(self.trial_type, "X")

        # 2. Map Target Side
        side_map = {Side.LEFT: "0", Side.RIGHT: "1"}
        side_enc = side_map.get(self.target_side, "X")

        # 3. Map Set Size and Layout
        # layout.value is a tuple: (positions_list, weight)
        positions, _ = self.layout.value
        size_enc = "0" if len(positions) == 2 else "1"

        # 4. Map Layout positions specifically
        # Comparing sorted lists to ensure order doesn't break the match
        pos_sorted = sorted(positions)
        if pos_sorted == [0, 1, 2]:
            lay_enc = "0"
        elif pos_sorted == [0, 1]:
            lay_enc = "1"
        elif pos_sorted == [1, 2]:
            lay_enc = "2"
        elif pos_sorted == [0, 2]:
            lay_enc = "3"
        else:
            lay_enc = "X" # Invalid

        return f"{type_enc}{side_enc}{size_enc}{lay_enc}"

    @property
    def target_set_size(self):
        positions, _ = self.layout.value
        return len(positions)

    @property
    def images_paths(self):
        # Helper for DataManager to get all image pairs used
        return [obj.image_pair for obj in self.all_orbits]
