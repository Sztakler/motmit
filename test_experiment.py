import pytest
import re
from constants import Side, OrbitPosition, Layout, TrialType
from models import Orbit, TrialConfig
from scenarios_generator import generate_base_pool

# --- TARGET CLASS TESTS ---

def test_target_id_calculation():
    """Verify that orbit IDs are correctly calculated for each screen position."""
    # LEFT column: 0, 1, 2
    t1 = Orbit(OrbitPosition.TOP, Side.LEFT, True, "img.png")
    assert t1.orbit_id == 0
    
    t2 = Orbit(OrbitPosition.BOTTOM, Side.LEFT, True, "img.png")
    assert t2.orbit_id == 2
    
    # RIGHT column: 3, 4, 5
    t3 = Orbit(OrbitPosition.TOP, Side.RIGHT, True, "img.png")
    assert t3.orbit_id == 3
    
    t4 = Orbit(OrbitPosition.BOTTOM, Side.RIGHT, True, "img.png")
    assert t4.orbit_id == 5

def test_target_mirror_calculation():
    """Verify that the mirror ID always points to the opposite side of the screen."""
    # Top Left (0) -> Top Right (3)
    assert Orbit(OrbitPosition.TOP, Side.LEFT, True, "img.png").mirror_id == 3
    # Mid Right (4) -> Mid Left (1)
    assert Orbit(OrbitPosition.MIDDLE, Side.RIGHT, True, "img.png").mirror_id == 1

# --- GENERATOR AND BALANCE TESTS ---

@pytest.fixture
def base_pool():
    """Fixture providing the base pool of 48 trials for testing."""
    images = [f"img{i}.png" for i in range(11)]
    return generate_base_pool()

def test_pool_size(base_pool):
    """Ensure the generator creates exactly 48 unique scenarios."""
    assert len(base_pool) == 48

def test_balance_mot_mit(base_pool):
    """Check for equal distribution between MOT and MIT trials (24 vs 24)."""
    mots = [t for t in base_pool if t.trial_type == TrialType.MOT]
    mits = [t for t in base_pool if t.trial_type == TrialType.MIT]
    assert len(mots) == 24
    assert len(mits) == 24

def test_balance_target_size(base_pool):
    """Verify balance between different set sizes (2 targets vs 3 targets).
    Expected: 24 trials each, thanks to the Layout weighting logic.
    """
    size_2 = [t for t in base_pool if t.layout != Layout.ALL]
    size_3 = [t for t in base_pool if t.layout == Layout.ALL]
    assert len(size_2) == 24
    assert len(size_3) == 24

def test_trial_images_logic(base_pool):
    """Ensure MOT trials use identical images while MIT trials use unique ones."""
    for trial in base_pool:
        img_paths = [obj.image_pair for obj in trial.all_objects]
        if trial.trial_type == TrialType.MOT:
            # MOT: All 6 objects should share the same image path
            assert len(set(img_paths)) == 1
        else:
            # MIT: All 6 objects should have unique image paths
            assert len(set(img_paths)) == 6

def test_probe_logic(base_pool):
    """Verify that the probe object matches the 'highlight_target' requirement."""
    for trial in base_pool:
        if trial.highlight_probe:
            # If we probe a target, the probe_object must have is_target = True
            assert trial.probe_object.is_target is True
        else:
            # If we probe a distractor, it must have is_target = False
            assert trial.probe_object.is_target is False

def test_image_pairing_logic():
    """Verify that each orbit has a consistent number but different suffixes (a/b)."""
    pool = generate_base_pool()
    
    for trial in pool:
        for obj in trial.all_objects:
            path_a, path_b = obj.image_pair
            
            # Extract digits using regex
            num_a = re.search(r'(\d+)', path_a).group(1)
            num_b = re.search(r'(\d+)', path_b).group(1)
            
            assert num_a == num_b
            assert "a.png" in path_a
            assert "b.png" in path_b

def test_mit_uniqueness():
    """Verify that MIT trials use 6 different numbers for 6 orbits."""
    pool = generate_base_pool()
    mit_trials = [t for t in pool if t.trial_type == TrialType.MIT]
    
    for trial in mit_trials:
        nums = [re.search(r'(\d+)', obj.image_pair[0]).group(1) for obj in trial.all_objects]
        assert len(set(nums)) == 6

def test_pool_balance():
    """Check if the total number of trials is 48."""
    pool = generate_base_pool()
    assert len(pool) == 48
