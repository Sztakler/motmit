import numpy as np
from psychopy import visual
from config import  image_radius, images_orbit_radius, orbiting_speed, mot_target_color, mit_target_color, mirror_color
import math

class ExperimentView:
    def __init__(self, win, trial_config, base_switch_time=1.0):
        self.win = win
        self.config = trial_config
        self.orbit_radius = images_orbit_radius
        self.base_switch_time = base_switch_time # Time when the direction change window starts

        radius_hex = 432
        shift = 108
        degree_shift = -60
        
        # Positions of 6 orbit centers (matching orbit_id 0-5)
        self.offsets = []
        for i in range(6):
            angle_deg = (i * 60) + degree_shift
            angle_rad = math.radians(angle_deg)
            
            x = radius_hex * math.cos(angle_rad)
            y = radius_hex * math.sin(angle_rad)
            
            # Column shifts
            if i < 3:
                x += shift
            else:
                x -= shift
                
            self.offsets.append((x, y))

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
        self.masks = [] # Black covers to hide images
        border_radius = image_radius * 0.5 + 5
        
        for i, target_data in enumerate(trial_config.all_orbits):
            # Create two images for each orbit
            img_pair = [
                visual.ImageStim(win, image=target_data.image_pair[0], size=image_radius),
                visual.ImageStim(win, image=target_data.image_pair[1], size=image_radius)
            ]
            self.stims.append(img_pair)
            
            # Create a border for each orbit (to be moved to circle 0 or 1 when needed)
            b_pair = [
                            visual.Circle(win, radius=border_radius, fillColor=None, lineColor=self.color, lineWidth=6),
                            visual.Circle(win, radius=border_radius, fillColor=None, lineColor=mirror_color, lineWidth=6)
                        ]
            self.borders.append(b_pair)

            m_pair = [
                visual.Circle(win, radius=border_radius, fillColor='black', lineColor='black'),
                visual.Circle(win, radius=border_radius, fillColor='black', lineColor='black')
            ]
            self.masks.append(m_pair)

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
            pos1 = (self.orbit_radius * np.cos(angle) + self.offsets[i][0], self.orbit_radius * np.sin(angle) + self.offsets[i][1])
            pos2 = (self.orbit_radius * np.cos(angle + np.pi) + self.offsets[i][0], self.orbit_radius * np.sin(angle + np.pi) + self.offsets[i][1])

            self.stims[i][0].pos = pos1
            self.stims[i][1].pos = pos2
            
            # Draw both stimuli for the current orbit
            self.stims[i][0].draw()
            self.stims[i][1].draw()

            if probe_only:
                self.masks[i][0].pos = pos1
                self.masks[i][1].pos = pos2
                self.masks[i][0].draw()
                self.masks[i][1].draw()

        # Handle Highlighting (CUE phase)
        if show_targets:
            for orbit_data in self.config.all_orbits:
                if orbit_data.has_target:
                    oid = orbit_data.orbit_id
                    t_idx = orbit_data.target_idx
                    
                    self.borders[oid][t_idx].pos = self.stims[oid][t_idx].pos
                    self.borders[oid][t_idx].lineColor = self.color
                    self.borders[oid][t_idx].draw()
                    
                    mirror_oid = oid + 3 if oid < 3 else oid - 3
                    
                    self.borders[mirror_oid][t_idx].pos = self.stims[mirror_oid][t_idx].pos
                    self.borders[mirror_oid][t_idx].lineColor = mirror_color
                    self.borders[mirror_oid][t_idx].draw()

        # Handle Probing (PROBE phase)
        if probe_only:
            oid = self.config.probe_orbit.orbit_id
            probe_idx = self.config.probe_index
            self.borders[oid][probe_idx].pos = self.stims[oid][probe_idx].pos
            self.borders[oid][probe_idx].lineColor = self.color
            self.borders[oid][probe_idx].draw()
