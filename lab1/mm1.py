from utils import *
import logging
import matplotlib.pyplot as plt

def simulate_mm1(arrival_rate, service_rate, simulation_time=None, queue_size=None, max_events=None):
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
  total_queue_waiting_time = 0.0
  total_processing_time = 0.0
  packets_arrived = 0
  packets_processed = 0
  system_idle_time = 0.0
  max_queue_size = 0
  queue_size_over_time = []

  # Schedule the first arrival event
  event_list = [(0, "arrival")]
  current_time = 0.0
  server_idle_since = 0.0

  # Main simulation loop
  while(event_list):
    # 1. Read tuple from event list
    current_event = event_list.pop(0)

    # process the last departure event
    if simulation_time is not None and current_time > simulation_time and current_event[1] == "arrival":
      queue_size_over_time.append((current_event[0], len(event_queue)))
      continue

    # 2.
    if(current_event[1] == "arrival"):
      if max_events is None or packets_arrived < max_events:
        # Add to queue
        event_queue.append(current_event)
        max_queue_size = max(max_queue_size, len(event_queue))
        if queue_size is not None and len(event_queue) > queue_size:
          logging.error(f"Queue size exceeded at {simulation_time}")
          break
        packets_arrived += 1
        # Generate a new packet arrival event
        next_event = (current_event[0] + generate_events(1, arrival_rate)[0], "arrival")
        event_list.append(next_event)
        event_list = sorted(event_list, key=lambda x: x[0])
    # 3.
    else:
      logging.debug(f"Departure at {current_event[0]}")
      # If departure, mark server as free
      server_busy = False
      packets_processed += 1
      server_idle_since = current_event[0]

    # 4 .If the server is free and the queue is empty
    if(not server_busy and not event_queue):
      logging.debug(f"Server is idle at {current_event[0]}")
      current_time = current_event[0]
      queue_size_over_time.append((current_event[0], len(event_queue)))
      continue
    if(server_busy):
      current_time = current_event[0]
      queue_size_over_time.append((current_event[0], len(event_queue)))
      continue
    # 5. Process the packet in the queue
    queue_event = event_queue.pop(0)
    logging.debug(f"Processing packet at {current_event[0]}")
    server_busy = True

    if server_idle_since is not None:
      system_idle_time += current_event[0] - server_idle_since
      server_idle_since = None
      logging.debug(f"System idle time: {system_idle_time}")

    # Add departure event to list
    processing_duration = generate_events(1, service_rate)[0]
    event_list.append((processing_duration + current_event[0], "departure"))
    event_list = sorted(event_list, key=lambda x: x[0])
    logging.debug(f"Departure scheduled at {processing_duration+current_event[0]}")

    total_queue_waiting_time += current_event[0] - queue_event[0] # Tempo na fila
    total_processing_time += processing_duration                # Tempo q vai demorar a processar

    current_time = current_event[0]
    queue_size_over_time.append((current_time, len(event_queue)))

  end_simulation_time = current_time

  # Calculate performance metrics after loop termination
  total_waiting_time = total_queue_waiting_time + total_processing_time
  average_waiting_time = total_waiting_time / packets_processed if packets_processed > 0 else 0
  average_time_in_queue = total_queue_waiting_time / packets_processed if packets_processed > 0 else 0
  system_utilization = 1 - (system_idle_time / end_simulation_time)

  return {
      "average_waiting_time": average_waiting_time,
      "average_time_in_queue": average_time_in_queue,
      "system_utilization": system_utilization,
      "packets_processed": packets_processed,
      "packets_arrived": packets_arrived,
      "max_queue_size": max_queue_size,
      "end_simulation_time": end_simulation_time,
      "queue_size_over_time": queue_size_over_time,
  }

# log_level = logging.DEBUG
log_level = logging.INFO
logging.basicConfig(level=log_level)

arrival_rate = 999
service_rate = 1000
simulation_time = None
queue_size = None
max_events = 100

if arrival_rate >= service_rate:
  logging.warning("Arrival rate should be less than service rate to avoid infinite queue growth.")

results = simulate_mm1(arrival_rate, service_rate, simulation_time, queue_size, max_events)

Ws = 1/(service_rate - arrival_rate)
print(f"Average time in system: {results['average_waiting_time']} [Theoretical: {Ws}]")
Wq = arrival_rate/(service_rate*(service_rate-arrival_rate))
print(f"Average time in queue: {results['average_time_in_queue']} [Theoretical: {Wq}]")
ro = arrival_rate/service_rate
print(f"System utilization: {results['system_utilization'] * 100}% [Theoretical: {ro*100}%]")

average_queue_size = results['system_utilization']**2/(1-results['system_utilization'])
# if arrival_rate == service_rate:
#   Lq = 1
# else:
#   Lq = ro**2 / (1-ro) if ro != 1 else float('inf')
Lq = arrival_rate * Wq

print(f"Average queue size: {average_queue_size} [Theoretical: {Lq}]")
print(f"Packets processed: {results['packets_processed']}/{results['packets_arrived']}")
print(f"Max queue size reached: {results['max_queue_size']}")
print(f"End simulation time: {results['end_simulation_time']}")

# plot queue size
x = [float(k[0]) for k in results['queue_size_over_time']]
y = [k[1] for k in results['queue_size_over_time']]
plt.plot(x, y)
plt.xlabel('Time')
plt.ylabel('Queue size')
plt.title('Queue size over time')
plt.show()
