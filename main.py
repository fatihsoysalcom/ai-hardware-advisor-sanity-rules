import itertools

# --- 1. Define Available Hardware Components ---
# Each component has a name, cost, performance score (arbitrary units),
# and a 'tier' for balancing purposes.
CPUS = [
    {"name": "Intel i3-10100", "cost": 100, "performance": 30, "tier": 1},
    {"name": "AMD Ryzen 5 3600", "cost": 150, "performance": 50, "tier": 2},
    {"name": "Intel i7-12700K", "cost": 300, "performance": 80, "tier": 3},
    {"name": "AMD Ryzen 9 5900X", "cost": 400, "performance": 95, "tier": 4},
]

GPUS = [
    {"name": "NVIDIA GTX 1650", "cost": 150, "performance": 40, "tier": 1},
    {"name": "AMD RX 6600", "cost": 250, "performance": 60, "tier": 2},
    {"name": "NVIDIA RTX 3070", "cost": 500, "performance": 85, "tier": 3},
    {"name": "AMD RX 7900 XT", "cost": 800, "performance": 98, "tier": 4},
]

RAMS = [
    {"name": "8GB DDR4", "cost": 50, "performance": 20, "capacity_gb": 8},
    {"name": "16GB DDR4", "cost": 80, "performance": 40, "capacity_gb": 16},
    {"name": "32GB DDR4", "cost": 150, "performance": 70, "capacity_gb": 32},
]

# --- 2. Define Sanity Rules and Use Case Profiles ---
# These rules ensure recommendations are logical, compatible, and meet user needs.

def check_budget(total_cost, budget):
    """Sanity Rule: Total cost must not exceed the user's budget."""
    return total_cost <= budget

def check_performance_balance(cpu_tier, gpu_tier):
    """Sanity Rule: CPU and GPU tiers should be reasonably balanced.
    Prevents pairing a very weak CPU with a very strong GPU, or vice-versa.
    """
    return abs(cpu_tier - gpu_tier) <= 1 # Allow one tier difference

def check_use_case_requirements(config, use_case):
    """Sanity Rule: Configuration must meet minimum requirements for the specified use case."""
    cpu = config["cpu"]
    gpu = config["gpu"]
    ram = config["ram"]

    if use_case == "gaming":
        # Gaming needs a decent GPU and enough RAM
        return gpu["performance"] >= 60 and ram["capacity_gb"] >= 16
    elif use_case == "workstation":
        # Workstation needs strong CPU and plenty of RAM
        return cpu["performance"] >= 70 and ram["capacity_gb"] >= 32
    elif use_case == "basic":
        # Basic use is less demanding
        return cpu["performance"] >= 30 and ram["capacity_gb"] >= 8
    return True # Default for other cases

# --- 3. AI-Powered Hardware Advisor Logic ---

def find_best_hardware_config(budget, use_case):
    """
    Finds the best hardware configuration based on budget, use case, and sanity rules.
    This function "explores every path" by iterating through all combinations.
    """
    print(f"Searching for configurations for budget: ${budget}, use case: {use_case}...")
    possible_configs = []

    # "Her Yolu Yürüyen" - Exploring every possible combination
    # This simulates the AI analyzing a wide range of data.
    for cpu, gpu, ram in itertools.product(CPUS, GPUS, RAMS):
        total_cost = cpu["cost"] + gpu["cost"] + ram["cost"]
        total_performance = cpu["performance"] + gpu["performance"] + ram["performance"] # Simplified metric

        config = {"cpu": cpu, "gpu": gpu, "ram": ram, "cost": total_cost, "performance": total_performance}

        # Applying "Sanity Kuralları" - Validating recommendations
        # Each rule acts as a logical check to ensure the recommendation is sound.
        if not check_budget(total_cost, budget):
            continue # Fails budget sanity check

        if not check_performance_balance(cpu["tier"], gpu["tier"]):
            continue # Fails balance sanity check

        if not check_use_case_requirements(config, use_case):
            continue # Fails use case sanity check

        possible_configs.append(config)

    if not possible_configs:
        return None

    # Sort by performance (descending) and then cost (ascending) to find the "best"
    possible_configs.sort(key=lambda x: (x["performance"], -x["cost"]), reverse=True)

    return possible_configs[0] # Return the top recommendation

# --- 4. Main Execution ---
if __name__ == "__main__":
    print("AI-Powered Hardware Advisor")
    print("--------------------------")

    try:
        user_budget = int(input("Enter your budget (e.g., 1000): $"))
        user_use_case = input("Enter your primary use case (gaming, workstation, basic): ").lower()
        if user_use_case not in ["gaming", "workstation", "basic"]:
            print("Invalid use case. Please choose from 'gaming', 'workstation', 'basic'.")
            exit()
    except ValueError:
        print("Invalid budget. Please enter a number.")
        exit()

    recommended_config = find_best_hardware_config(user_budget, user_use_case)

    print("\n--- Recommendation ---")
    if recommended_config:
        print(f"CPU: {recommended_config['cpu']['name']}")
        print(f"GPU: {recommended_config['gpu']['name']}")
        print(f"RAM: {recommended_config['ram']['name']}")
        print(f"Total Cost: ${recommended_config['cost']}")
        print(f"Estimated Performance Score: {recommended_config['performance']}")
    else:
        print("No suitable configuration found within your budget and requirements.")
