import re

def parse_input_line(line):
    vehicle_type = "ambulance" if "ambulance" in line.lower() else "car"
    if vehicle_type == "ambulance":
        name = f"amb{parse_input_line.amb_count}"
        parse_input_line.amb_count += 1
    else:
        name = f"car{parse_input_line.car_count}"
        parse_input_line.car_count += 1

    seg_m = re.search(r'segment(\d+)', line, re.IGNORECASE)
    segment = f"seg{seg_m.group(1)}" if seg_m else None

    sig_m = re.search(r'signal(\d+)', line, re.IGNORECASE)
    signal = f"sig{sig_m.group(1)}" if sig_m else None

    return vehicle_type, name, segment, signal

parse_input_line.car_count = 1
parse_input_line.amb_count = 1

# Read high-level input
with open("input.txt", "r") as file:
    lines = [l.strip() for l in file if l.strip()]

vehicles = []
segments = set()
signals = set()
init_conditions = []
occupied = set()

# Parse each line
for line in lines:
    vtype, name, seg, sig = parse_input_line(line)
    vehicles.append((name, vtype))
    segments.add(seg)
    occupied.add(seg)
    init_conditions.append(f"(at {name} {seg})")

    if sig:
        signals.add(sig)
        init_conditions.append(f"(signal_status {sig} red)")

# Define all segments you wish to include
all_segments = {"seg1", "seg2", "seg3", "seg4", "seg5"}
segments |= all_segments

# seg2 is the intersection
init_conditions.append("(intersection seg2)")

# Mark free only for non-intersection, non-occupied segments
for seg in sorted(all_segments):
    if seg != "seg2" and seg not in occupied:
        init_conditions.append(f"(free {seg})")

# Static connections
connections = [("seg1","seg2"),("seg2","seg3"),("seg4","seg2"),("seg5","seg2")]
for s1,s2 in connections:
    init_conditions.append(f"(connected {s1} {s2})")
    segments.add(s1); segments.add(s2)

# Signal placements
placements = [
    "(signal_between sig1 seg1 seg2)",
    "(signal_between sig2 seg2 seg3)",
    "(signal_between sig3 seg5 seg2)",
    "(signal_between sig4 seg3 seg2)"
]
for p in placements:
    init_conditions.append(p)
    _, sig, s1, s2 = p.strip("()").split()
    signals.add(sig)
    segments.add(s1); segments.add(s2)

# Write the PDDL problem file
with open("traffic_problem.pddl","w") as f:
    f.write("(define (problem traffic-problem)\n")
    f.write("  (:domain traffic-light)\n\n")

    # Objects
    f.write("  (:objects\n")
    for name,vtype in vehicles:
        role = "emergency" if vtype=="ambulance" else "vehicle"
        f.write(f"    {name} - {role}\n")
    for seg in sorted(segments):
        f.write(f"    {seg} - segment\n")
    for sig in sorted(signals):
        f.write(f"    {sig} - signal\n")
    f.write("    red green yellow\n")  # Untyped symbols
    f.write("  )\n\n")

    # Init
    f.write("  (:init\n")
    for cond in init_conditions:
        f.write(f"    {cond}\n")
    f.write("  )\n\n")

    # Goal: all vehicles at seg2
    f.write("  (:goal (and\n")
    for name,_ in vehicles:
        f.write(f"    (at {name} seg2)\n")
    f.write("  ))\n)\n")
