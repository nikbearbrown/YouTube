import string
import random
import re
import argparse

# Set up argument parser for command line options
parser = argparse.ArgumentParser(description='Generate image prompts with various parameters')
parser.add_argument('--pvalue', type=str, help='Custom pvalue string')
parser.add_argument('--sref', type=str, help='Custom sref string')
parser.add_argument('--n', type=int, default=5, help='Number of batches to generate')
args = parser.parse_args()

# Reference lists - various style identifiers for image generation
# Each numerical value represents a different visual style
srefs = [
    "1613",          # Base style identifier
    "1400660455",    # Pastel Scribbles
    "71",            # Related to Pastel Scribbles
    # Many more style references...
    # Shortened for readability ... add your own codes - in actual code these would all remain
]

# Parameter values for controlling image generation characteristics
pvalues = [
    "5gbht4i",
    "5l34wh8", 
    "x9o4m9g",
    # More parameter values...
    # Shortened for readability ... add your own codes
]

# Character actions for dynamic posing
actions = [
    "Smiling",
    "Frowning",
    "Drinking",
    # More actions...
    # Shortened for readability ... add your own codes
]

# Character poses for image generation
poses = [
    "front view, arms at sides, neutral expression",
    "T-pose, arms outstretched, modeling pose",
    # More poses...
    # Shortened for readability ... add your own codes
]

# Character descriptions to use in prompts
prompts = [
    "Sherlock Holmes, a tall, thin man with sharp features, piercing gray eyes, and often wearing a deerstalker hat and smoking a pipe",
    "Harry Potter, a skinny man with messy black hair, round glasses, bright green eyes, and a lightning-shaped scar on his forehead",
    # More character descriptions...
    # Shortened for readability ... add your own codes
]

def generate_random_alphanumeric(length=5):
    """
    Generate a random alphanumeric string of specified length.
    
    Args:
        length (int): Length of the string to generate (default: 5)
    
    Returns:
        str: Random alphanumeric string used as a seed
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_pvalue_string():
    """
    Create a parameter value string either from command line input or randomly selected.
    
    Returns:
        str: Space-separated string of parameter values
    """
    if args.pvalue:
        # Use command-line provided value with any asterisks removed
        return args.pvalue.replace('*', '').strip()
    else:
        # Randomly select 1-5 parameter values
        num_values = random.randint(1, min(5, len(pvalues)))
        selected_values = random.sample(pvalues, num_values)
        return " ".join(selected_values)

def generate_sref_string():
    """
    Create a style reference string either from command line input or randomly selected.
    
    Returns:
        str: Space-separated string of style references
    """
    if args.sref:
        # Use command-line provided value with any asterisks removed
        return args.sref.replace('*', '').strip()
    else:
        # Randomly select 1-5 style references
        num_values = random.randint(1, min(5, len(srefs)))
        selected_values = random.sample(srefs, num_values)
        return " ".join(selected_values)

def generate_prompts_batch():
    """
    Generate a batch of prompts with consistent parameters.
    
    Returns:
        list: A list of formatted prompt strings ready for image generation
    """
    # Generate a random seed string for the batch
    random_string = generate_random_alphanumeric()
    
    # Select random character descriptions
    selected_prompts = random.sample(prompts, min(22, len(prompts)))
    
    # Randomly decide parameter style for this batch
    # 1: sref only, 2: pvalue only, 3: both
    param_style = random.randint(1, 3)
    
    # Generate parameter values based on selected style
    sref = generate_sref_string() if param_style in [1, 3] else ""
    pvalue = generate_pvalue_string() if param_style in [2, 3] else ""
    
    # Format each prompt with the chosen parameters
    formatted_prompts = []
    for prompt in selected_prompts:
        # Randomly decide if we'll include a pose (33% chance)
        pose = random.choice(poses) if random.random() < 0.33 else ""
        
        # Construct the prompt based on parameter style
        if param_style == 1:  # sref only
            pprompt = f"{random_string}, {prompt}, {pose} --sref {sref} --ar 9:16 --v 7.0"
        elif param_style == 2:  # pvalue only
            pprompt = f"{random_string}, {prompt}, {pose} --p {pvalue} --ar 9:16 --v 7.0"
        else:  # both sref and pvalue
            pprompt = f"{random_string}, {prompt}, {pose} --sref {sref} --p {pvalue} --ar 9:16 --v 7.0"
        
        # Clean up any excess spaces
        pprompt = re.sub(r'[ ]+', ' ', pprompt)
        formatted_prompts.append(pprompt)
    
    # Return a random subset of the formatted prompts
    return random.sample(formatted_prompts, min(11, len(formatted_prompts)))

# Main execution
if __name__ == "__main__":
    # Generate n batches of prompts (default: 5)
    n = args.n if args.n else 5
    for batch_num in range(n):
        print(f"# Batch {batch_num + 1}")
        batch = generate_prompts_batch()
        for prompt in batch:
            print(prompt)
        print("-" * 80)  # Separator between batches