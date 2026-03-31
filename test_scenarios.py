from scenarios_generator import generate_base_pool, get_full_experiment

def test_generation():
    # 1. Generate the base pool of trials
    pool = generate_base_pool()
    print(f"Base pool generated: {len(pool)} unique trials.")

    # 2. Create an experiment with 2 blocks
    experiment = get_full_experiment(pool, num_blocks=2)
    print(f"Total trials in experiment: {len(experiment)}\n")

    # 3. Test a sample trial (e.g., the first one, since they're already randomized)
    sample = experiment[0]
    
    print("--- SAMPLE TRIAL DATA ---")
    print(f"Trial ID:      {sample.id}")
    print(f"Block/Number:  {sample.block_number} / {sample.trial_number}")
    print(f"Type:          {sample.trial_type.name}")
    print(f"Condition ID:  {sample.condition_id}")
    print(f"Target Side:   {sample.target_side.name}")
    print(f"Set Size:      {sample.target_set_size}")
    print(f"Probe:         {'Target' if sample.highlight_probe else 'Distractor'}")
    print(f"Correct Ans:   {sample.correct_answer}")
    
    # Check if images are assigned correctly
    print(f"\nAll Object Pairs:")
    for i in range(len(sample.all_objects[:3])):
        obj = sample.all_objects[i]
        role = "TARGET" if obj.is_target else "DISTRACTOR"
        print(f"  Orbit {obj.orbit_id} ({role}): {obj.image_pair}")

    print(f"  =========================================================")
    
    for i in range(3, 3 + len(sample.all_objects[3:])):
        obj = sample.all_objects[i]
        role = "TARGET" if obj.is_target else "DISTRACTOR"
        print(f"  Orbit {obj.orbit_id} ({role}): {obj.image_pair}")

if __name__ == "__main__":
    test_generation()
