import random
import numpy as np
from utils import *

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
  event_queue = []
  server_busy = False
  total_waiting_time = 0
  total_queue_waiting_time = 0
  num_customers = 0
  system_idle_time = 0

  # Schedule the first arrival event
  event_list = [(0, "arrival")]
  current_time = 0

  # Main simulation loop
  while(event_list):
    # Read tuple from event list
    current_event = event_list.pop(0)
    # Update current time
    current_time = current_event[0]
    # Check if simulation time has been reached
    if(current_time > simulation_time):
      break
    # Check for type of event
    if(current_event[1] == "arrival"):
      # If arrival, add it to queue
      event_queue.append(current_event)
      # Generate a new packet arrival event
      next_event = (current_event[0] + generate_events(1, arrival_rate)[0], "arrival")
      event_list.append(next_event)
      #If the server is free and the queue is not empty, schedule a departure event
      if(not server_busy and not event_queue):
        continue
      else:
        # Take oldest packet from queue
        current_departure = event_queue.pop(-1)
        # Mark server as busy
        server_busy = True
        # Add departure event to list
        event_list.append((next_event[0] + generate_events(1, service_rate)[0], "departure"))
    else:
      # If departure, mark server as free
      server_busy = False
      # If the server is free and the queue is not empty, schedule a departure event
      if(not server_busy and not event_queue):
        continue
      else:
        # Take oldest packet from queue
        current_departure = event_queue.pop(-1)
        # Mark server as busy
        server_busy = True
        # Add departure event to list
        event_list.append((current_departure[0] + generate_events(1, service_rate)[0], "departure"))
  
  # Calculate performance metrics after loop termination
  average_waiting_time = total_waiting_time / num_customers if num_customers > 0 else 0
  average_time_in_queue = total_queue_waiting_time / num_customers if num_customers > 0 else 0
  system_utilization = (1 - (system_idle_time / simulation_time))*100

  return {
      "average_waiting_time": average_waiting_time,
      "average_time_in_queue": average_time_in_queue,
      "system_utilization": system_utilization
  }

# Example usage
results = simulate_mm1(arrival_rate=0.5, service_rate=0.25, simulation_time=10)
print("Average waiting time:", results["average_waiting_time"])
print("Average time in queue:", results["average_time_in_queue"])
print("System utilization:", results["system_utilization"])