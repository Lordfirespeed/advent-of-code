with open(r"Input\2020day13.txt") as inputfile:
    input_data = [line.strip() for line in inputfile.readlines()]

earliest_departure, bus_IDs = int(input_data[0]), [int(bus_id) for bus_id in input_data[1].split(",") if bus_id != "x"]

departures = {}

for bus_id in bus_IDs:
    wait_time = bus_id - (earliest_departure % bus_id)
    departures[wait_time] = bus_id

lowest_wait = min(departures.keys())

print(f"Earliest bus ID {departures[lowest_wait]}, wait {lowest_wait} minutes")
print(f"Product: {departures[lowest_wait] * lowest_wait}")
