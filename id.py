def encode_conditions(trial_type, target_side, set_size, layout):
    trial_type_map = {"mot": "0", "mit": "1"}
    target_side_map = {"l": "0", "r": "1"}
    set_size_map = {"2": "0", "3": "1"}
    if layout == [0, 1, 2]:
        layout_encoded = "0"
    elif layout == [0, 1]:
        layout_encoded = "1"
    elif layout == [1, 2]:
        layout_encoded = "2"
    elif layout == [0, 2]:
        layout_encoded = "3"
    else:
        layout_encoded = "Invalid"

    # Encode each condition
    trial_type_encoded = trial_type_map.get(trial_type, "Invalid")
    target_side_encoded = target_side_map.get(target_side, "Invalid")
    set_size_encoded = set_size_map.get(set_size, "Invalid")

    # Check for invalid inputs
    if "Invalid" in (trial_type_encoded, target_side_encoded, set_size_encoded, layout_encoded):
        return "Error: Invalid input"

    # Combine the binary encoding
    return trial_type_encoded + target_side_encoded + set_size_encoded + layout_encoded


# Example usage
if __name__ == "__main__":
    print(encode_conditions("mot", "l", "2", [0, 1, 2]))  # Output: 0000
    print(encode_conditions("mit", "r", "3", [1, 2]))  # Output: 1112