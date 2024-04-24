import random
import numpy as np

def generate_poisson(N=120, lam=3):
    rng = np.random.default_rng()
    return rng.poisson(lam=lam, size=N)

def simulate_mm1(arrival_rate, service_rate, simulation_time):
  """
  Simulates an M/M/1 queue for a given simulation time.

  Args:
      arrival_rate: The arrival rate (lambda) of packets.
      service_rate: The service rate (mu) of packets.
      simulation_time: The total simulation time.

  Returns:
      A dictionary containing average waiting time and system utilization.
  """
  event_list = []
  server_busy = False
  total_waiting_time = 0
  num_customers = 0
  system_idle_time = 0

  # Schedule the first arrival event
  event_list.append((generate_poisson(arrival_rate), "arrival"))
  current_time = 0

  while event_list and current_time and any(event[0] <= simulation_time for event in event_list) <= simulation_time:
    # Find the event with the earliest time (within simulation time)
    filtered_events = [event for event in event_list if event[0] <= simulation_time]
    if not filtered_events:
      # No events within simulation time, add artificial departure
      filtered_events.append((current_time, "departure"))
    min_time = min(event[0] for event in filtered_events)

    for i, event in enumerate(event_list):
      if event[0] == min_time:
        current_event = event_list.pop(i)
        break

    current_time, event_type = current_event

    if event_type == "arrival":
      # New packet arrives
      print(f"Packet arrived at time {current_time}")
      if server_busy:
        num_customers += 1
      else:
        server_busy = True
        service_time = random.expovariate(service_rate)
        event_list.append((current_time + service_time, "departure"))
      event_list.append((current_time + random.expovariate(arrival_rate), "arrival"))
      # Sort the list based on event time (first element of the tuple)
      event_list.sort()

    else:
      # Packet finishes service
      print(f"Packet departed at time {current_time}")
      if num_customers > 0:
        total_waiting_time += (current_time - event_list[0][0])
        num_customers -= 1
        # Schedule departure event for the next waiting customer (if any)
        if num_customers > 0:
          service_time = random.expovariate(service_rate)
          event_list.append((current_time + service_time, "departure"))
      else:
        server_busy = False
        system_idle_time += current_time - event_list[0][0]

    if not event_list:  # Check if event_list is empty
      break  # Terminate loop if no more events

  # Calculate performance metrics after loop termination
  average_waiting_time = total_waiting_time / num_customers if num_customers > 0 else 0
  system_utilization = 1 - (system_idle_time / simulation_time)

  return {
      "average_waiting_time": average_waiting_time,
      "system_utilization": system_utilization
  }

# Example usage
results = simulate_mm1(arrival_rate=2, service_rate=3, simulation_time=6)
print("Average waiting time:", results["average_waiting_time"])
print("System utilization:", results["system_utilization"])