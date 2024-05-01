from utils import *
import logging

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
  server_idle_since = 0

  # Main simulation loop
  while(event_list):
    # 1. Read tuple from event list
    current_event = event_list.pop(0)
    # 2.
    if(current_event[1] == "arrival"):
      # Add to queue
      event_queue.append(current_event)
      # Generate a new packet arrival event
      next_event = (current_event[0] + generate_events(1, arrival_rate)[0], "arrival")
      event_list.append(next_event)
      event_list = sorted(event_list, key=lambda x: x[0])
    # 3.
    else:
      logging.debug(f"Departure at {current_event[0]}")
      # If departure, mark server as free
      server_busy = False
      server_idle_since = current_event[0]

      total_waiting_time += current_event[0] - current_time # Tempo a processar

    # 4 .If the server is free and the queue is empty
    if(not server_busy and not event_queue):
      logging.debug(f"Server is idle at {current_event[0]}")
      current_time = current_event[0]
      continue
    if(server_busy):
      continue
    # 5. Process the packet in the queue
    current_event = event_queue.pop(0)
    logging.debug(f"Processing packet at {current_event[0]}")
    server_busy = True

    if server_idle_since is not None:
      system_idle_time += current_event[0] - server_idle_since
      server_idle_since = None
      logging.debug(f"System idle time: {system_idle_time}")

    # Add departure event to list
    departure_time = current_event[0] + generate_events(1, service_rate)[0]
    event_list.append((departure_time, "departure"))
    event_list = sorted(event_list, key=lambda x: x[0])
    logging.debug(f"Departure scheduled at {departure_time}")

    num_customers += 1
    total_queue_waiting_time += current_event[0] - current_time # Tempo na fila
    total_waiting_time += current_event[0] - current_time       # Tempo na fila

    current_time = current_event[0]
    # Check if simulation time has been reached
    if(current_time > simulation_time):
      break
  end_simulation_time = current_time

  # Calculate performance metrics after loop termination
  average_waiting_time = total_waiting_time / num_customers if num_customers > 0 else 0
  average_time_in_queue = total_queue_waiting_time / num_customers if num_customers > 0 else 0
  system_utilization = (1 - (system_idle_time / end_simulation_time))*100

  return {
      "average_waiting_time": average_waiting_time,
      "average_time_in_queue": average_time_in_queue,
      "system_utilization": system_utilization
  }

# log_level = logging.DEBUG
log_level = logging.INFO
logging.basicConfig(level=log_level)

results = simulate_mm1(arrival_rate=2, service_rate=2, simulation_time=50)

print("Average time in system:", results["average_waiting_time"])
print("Average time in queue:", results["average_time_in_queue"])
print("System utilization:", results["system_utilization"])
