import time

# Crossroad layout (bi-directional for simplicity)
layout = {
    "seg1": ["seg2"],
    "seg2": ["seg1", "seg3", "seg4", "seg5"],
    "seg3": ["seg2"],
    "seg4": ["seg2"],
    "seg5": ["seg2"]
}

# Signals controlling each path
signals = {
    "siga": {"from": "seg2", "to": "seg3", "status": "red"},
    "sigb": {"from": "seg2", "to": "seg5", "status": "red"},
    "sigc": {"from": "seg4", "to": "seg2", "status": "red"},
    "sigd": {"from": "seg5", "to": "seg2", "status": "red"},
    "sige": {"from": "seg3", "to": "seg2", "status": "red"}
}

# Initial vehicle positions
vehicle_positions = {
    "car1": "seg1",
    "car2": "seg5",
    "car3": "seg3",
    "amb1": "seg4"
}

def read_plan(path="plan2.txt"):
    with open(path, "r") as file:
        lines = file.readlines()

    actions = []
    for line in lines:
        line = line.strip()
        if line.startswith(";") or not line:
            continue
        start = line.find("(")
        end = line.find(")")
        if start == -1 or end == -1:
            continue
        content = line[start + 1:end]
        parts = content.lower().split()
        action = parts[0]
        args = parts[1:]
        actions.append((action, args))
    return actions

def visualize_crossroad():
    print("\n=== ROAD LAYOUT ===")
    center = ""
    for v, loc in vehicle_positions.items():
        if loc == "seg2":
            center += f"[{v.upper()}]"
    center = center if center else "[    ]"
    print("     seg5")
    for v, loc in vehicle_positions.items():
        if loc == "seg5":
            print(f"    ({v} at seg5)")
    print(f"seg1 ← {center} → seg3")
    for v, loc in vehicle_positions.items():
        if loc == "seg1":
            print(f"    ({v} at seg1)")
    for v, loc in vehicle_positions.items():
        if loc == "seg3":
            print(f"    ({v} at seg3)")
    print("     ↓")
    print("    seg4")
    for v, loc in vehicle_positions.items():
        if loc == "seg4":
            print(f"    ({v} at seg4)")
    print("===================\n")

def change_signal(sig_name, new_status):
    old_status = signals[sig_name]["status"]
    signals[sig_name]["status"] = new_status
    status_change_time = time.strftime("%H:%M:%S", time.localtime())
    print(f"Signal {sig_name} changed from {old_status} to {new_status} at {status_change_time}.")

def move_vehicle(v_name, from_seg, to_seg):
    controlling_signal = None
    for sig, data in signals.items():
        if data["from"] == from_seg and data["to"] == to_seg:
            controlling_signal = sig
            break

    if controlling_signal:
        if signals[controlling_signal]["status"] != "green":
            if "amb" in v_name:
                print(f"{v_name} overrides {controlling_signal} to green.")
                change_signal(controlling_signal, "green")
            else:
                print(f"{v_name} waiting at red {controlling_signal}...")
                time.sleep(2)
                change_signal(controlling_signal, "green")
                time.sleep(1)

    print(f"{v_name} moving from {from_seg} to {to_seg}")
    vehicle_positions[v_name] = to_seg
    visualize_crossroad()
    time.sleep(1)

def simulate_plan(plan_actions):
    for action, args in plan_actions:
        if action == "change-signal":
            sig, _, new = args  # ignore current status
            change_signal(sig, new)
        elif action == "move-vehicle":
            v, s1, s2 = args
            move_vehicle(v, s1, s2)
        else:
            print(f"Unknown action: {action}")
        time.sleep(1)

def print_final_signal_state():
    print("\nFinal Signal States:")
    for sig, data in signals.items():
        print(f"  {sig}: {data['status']}")
    print("Simulation Complete.")

def main():
    print("Emergency Corridor Crossroad Simulation \n")
    visualize_crossroad()
    plan = read_plan("plan.txt")
    simulate_plan(plan)
    print_final_signal_state()

if __name__ == "__main__":
    main()
