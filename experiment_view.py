import numpy as np
from psychopy import visual
from config import scale, image_radius, images_orbit_radius, orbiting_speed, mot_target_color, mit_target_color

class ExperimentView:
    def __init__(self, win, trial_config, base_switch_time=1.0):
        self.win = win
        self.config = trial_config
        self.orbit_radius = images_orbit_radius * scale
        self.base_switch_time = base_switch_time # Time when the direction change window starts
        
        # Positions of 6 orbit centers (matching orbit_id 0-5)
        x_d = 400 
        y_d = 300 

        self.offsets = [
            (-x_d, y_d), (-x_d, 0), (-x_d, -y_d), # Left column
            (x_d, y_d),  (x_d, 0),  (x_d, -y_d)   # Right column
        ]

        # Movement parameters
        self.directions = [np.random.choice([-1, 1]) for _ in range(6)]
        self.initial_angles = [np.random.uniform(0, 2*np.pi) for _ in range(6)]
        
        # Randomize direction change within the 0.75s window
        self.switch_offsets = [np.random.uniform(0, 0.75) for _ in range(6)]
        self.has_reversed = [False] * 6
        
        # Visual assets
        self.color = mot_target_color if trial_config.trial_type.name == "MOT" else mit_target_color
        self.stims = [] # Will hold pairs of (ImageStim_A, ImageStim_B)
        self.borders = [] # Highlighting circles

        for i, target_data in enumerate(trial_config.all_orbits):
            # Create two images for each orbit
            img_pair = [
                visual.ImageStim(win, image=target_data.image_pair[0], size=image_radius*scale),
                visual.ImageStim(win, image=target_data.image_pair[1], size=image_radius*scale)
            ]
            self.stims.append(img_pair)
            
            # Create a border for each orbit (to be moved to circle 0 or 1 when needed)
            border = visual.Circle(win, radius=(image_radius+5)*scale, fillColor=None,  # type: ignore
                                   lineColor=self.color, lineWidth=6)
            self.borders.append(border)

    def update(self, t, show_targets=False, probe_only=False):
        """
        t: elapsed time from the start of the movement phase
        show_targets: if True, highlights ALL targets (cue phase)
        probe_only: if True, highlights only the final PROBE object
        """
        speed = orbiting_speed
        
        for i in range(6):
            target_switch_time = self.base_switch_time + self.switch_offsets[i]

            # Logic for direction reversal
            if t >= target_switch_time and not self.has_reversed[i]:
                # Calculate the exact angle at the moment of reversal to ensure continuity
                exact_angle_at_switch = (self.directions[i] * target_switch_time * speed) + self.initial_angles[i]
                self.initial_angles[i] = exact_angle_at_switch
                self.directions[i] *= -1
                self.has_reversed[i] = True

            # Calculate relative time since the last direction change
            t_rel = (t - target_switch_time) if self.has_reversed[i] else t
            
            # Calculate current orbital angle
            angle = (self.directions[i] * t_rel * speed) + self.initial_angles[i]
            
            # Update positions (Image A and Image B are 180 degrees apart)
            x1 = self.orbit_radius * np.cos(angle) + self.offsets[i][0]
            y1 = self.orbit_radius * np.sin(angle) + self.offsets[i][1]
            x2 = self.orbit_radius * np.cos(angle + np.pi) + self.offsets[i][0]
            y2 = self.orbit_radius * np.sin(angle + np.pi) + self.offsets[i][1]

            self.stims[i][0].pos = (x1, y1)
            self.stims[i][1].pos = (x2, y2)
            
            # Draw both stimuli for the current orbit
            self.stims[i][0].draw()
            self.stims[i][1].draw()

        # Handle Highlighting (CUE phase)
        if show_targets:
            for orbit_data in self.config.all_orbits:
                if orbit_data.has_target:
                    oid = orbit_data.orbit_id
                    target_idx = orbit_data.target_idx
                    self.borders[oid].pos = self.stims[oid][target_idx].pos
                    self.borders[oid].draw()
                    
        # Handle Probing (PROBE phase)
        if probe_only:
            oid = self.config.probe_orbit.orbit_id
            probe_idx = self.config.probe_index
            self.borders[oid].pos = self.stims[oid][probe_idx].pos
            self.borders[oid].draw()
