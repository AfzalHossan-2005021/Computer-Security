from math import floor

# Function to get the number of rounds for AES based on key length
def get_round_counts(key_length: int):
    # Determine the number of rounds based on key length
    if key_length == 128:
        round_counts = 10
    elif key_length == 192:
        round_counts = 12
    elif key_length == 256:
        round_counts = 14
    else:
        raise ValueError("Invalid key length. Must be 128, 192, or 256 bits.")
    return round_counts

# This function generates the round constants for AES key schedule.
def generate_round_constants(count: int):
    # Generate round constants
    constants = [0x01]
    for i in range(1, count):
        if constants[i-1] < 0x80:
            constants.append(constants[i-1] << 1)
        else:
            constants.append(((constants[i-1] << 1) ^ 0x11B) % 0x100)

    # Convert to round constants
    round_constants = []
    for i in range(count):
        round_constants.append([constants[i], 0, 0, 0])
    
    return round_constants
    

# Example usage
if __name__ == "__main__":
    #input key length from user
    key_length = int(input("Enter key length (128, 192, 256): "))
    round_count = get_round_counts(key_length)
    round_key_count = round_count + 1
    round_constants_count = floor(round_count * 4.0 / (key_length / 32.0))
    round_constants = generate_round_constants(round_constants_count)
    print(f"Number of rounds for AES with {key_length} bits key: {round_count}")
    print(f"Number of round keys: {round_key_count}")
    print(f"Number of round constants: {round_constants_count}")
    print(f"Round constants: ")
    for i in range(round_constants_count):
        print(f"{round_constants[i]}")