import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def theoretical_avg_customers(lam, meu1, meu2):
    rho1 = lam / meu1
    rho2 = lam / meu2
    return rho1 / (1 - rho1) + rho2 / (1 - rho2)

def calculate_error_percentage(theoretical, observed):
    return abs(theoretical - observed) / theoretical * 100

def determine_state(next_arrival, service1_end, service2_end, current_time):
    next_event_time = min(next_arrival, service1_end, service2_end)
    if next_event_time > current_time:
        return "Idle", next_event_time
    if next_event_time == next_arrival:
        return "Arrival", next_event_time
    if next_event_time == service1_end:
        return "Service-1 Finished", next_event_time
    if next_event_time == service2_end:
        return "Service-2 Finished", next_event_time

def take_snapshot(current_time, queue1_length, queue2_length, customers_in_system):
    customers_in_system.append((current_time, queue1_length, queue2_length))

def log_state(file, current_time, state, queue1_length, queue2_length):
    file.write(f"At time {current_time:.2f}: {state}, Queue 1 Length: {queue1_length}, Queue 2 Length: {queue2_length}\n")

def run_simulation(Number_of_simulations, lambda_input, meu1, meu2, Time_of_simulation, q1_initial_length, log_file):
    results = []
    all_customers_in_system = []
    with open(log_file, 'w') as file:
        for _ in range(Number_of_simulations):
            current_time = 0
            queue1_length = q1_initial_length
            queue2_length = 0
            customers_in_system = [(0, queue1_length, queue2_length)]
            test_next_arrival = current_time + np.random.exponential(1 / lambda_input)
            if test_next_arrival < Time_of_simulation:
                next_arrival = test_next_arrival
            else:
                next_arrival = float('inf')
            if queue1_length > 0:
                service1_end = current_time + np.random.exponential(1 / meu1)
            else:
                service1_end = float('inf')

            service2_end = float('inf')

            while current_time < Time_of_simulation:
                # Determine next event
                state, next_event_time = determine_state(next_arrival, service1_end, service2_end, current_time)

                # Collect data
                if state == "Idle":
                    take_snapshot(current_time, queue1_length, queue2_length, customers_in_system)
                current_time = next_event_time
                if state != "Idle":
                    log_state(file, current_time, state, queue1_length, queue2_length)

                # Handle arrival
                if state == "Arrival":
                    queue1_length += 1
                    test_next_arrival = current_time + np.random.exponential(1 / lambda_input)
                    if test_next_arrival < Time_of_simulation:
                        next_arrival = test_next_arrival
                    else:
                        next_arrival = float('inf')
                    if queue1_length == 1 and service1_end == float('inf'):
                        # Start service at server 1 for the entered customer
                        service1_end = current_time + np.random.exponential(1 / meu1)

                # Handle service completion at server 1
                if state == "Service-1 Finished":
                    queue1_length -= 1
                    queue2_length += 1
                    service1_end = current_time + np.random.exponential(1 / meu1) if queue1_length > 0 else float('inf')
                    if queue2_length == 1 and service2_end == float('inf'):
                        service2_end = current_time + np.random.exponential(1 / meu2)

                # Handle service completion at server 2
                if state == "Service-2 Finished":
                    queue2_length -= 1
                    service2_end = current_time + np.random.exponential(1 / meu2) if queue2_length > 0 else float('inf')

            # Compute the time-averaged number of customers in the system
            total_time_in_system = sum(((customers_in_system[i][1] + customers_in_system[i][2]) *
                                        (customers_in_system[i + 1][0] - customers_in_system[i][0])) for i in
                                       range(len(customers_in_system) - 1))
            average_customers = total_time_in_system / Time_of_simulation
            results.append(average_customers)
            all_customers_in_system.append(customers_in_system)
    return np.mean(results), all_customers_in_system

def Simulate_Part_A():
    # Parameters
    lambdas = [1, 5]
    mu1s = [2, 4]
    mu2s = [3, 4]
    Ts = [10, 50, 100, 1000]
    q1_initial_length = 0  # According to the lab requirements, q = 0 initially
    Number_of_simulations = 100
    results = []
    log_file = 'part_a_simulation_log.txt'

    for lambda_val in lambdas:
        for mu1 in mu1s:
            for mu2 in mu2s:
                for T in Ts:
                    avg_customers, all_customers = run_simulation(Number_of_simulations, lambda_val, mu1, mu2, T, q1_initial_length, log_file)
                    theoretical_value = theoretical_avg_customers(lambda_val, mu1, mu2)
                    error_percentage = calculate_error_percentage(theoretical_value, avg_customers)
                    results.append((lambda_val, mu1, mu2, T, avg_customers, theoretical_value, error_percentage))
                    print(
                        f"For T={T}, λ={lambda_val}, μ1={mu1}, μ2={mu2}, Average Number of Customers in System: {avg_customers:.2f}, Theoretical Value: {theoretical_value:.2f}, Error: {error_percentage:.2f}%")

    # Convert results to DataFrame
    df = pd.DataFrame(results, columns=['λ', 'μ1', 'μ2', 'T', 'Average Customers', 'Theoretical Value', 'Error %'])

    # Save results to Excel
    current_directory = os.getcwd()
    df.to_excel(os.path.join(current_directory, 'queue_simulation_results.xlsx'), index=False)
    print("Results saved to 'queue_simulation_results.xlsx' in the current working directory")

def Simulate_Part_B():

    # Parameters for part B
    lambdas = [1, 5]
    mu1s = [2, 4]
    mu2s = [3, 4]
    T = 2000
    q1_initial_length = 1000
    Number_of_simulations = 1  # We need data for plotting, so just one simulation run for plotting
    log_file = 'part_b_simulation_log.txt'

    # Run simulations for each combination and generate plots
    plot_number = 1
    current_directory = os.getcwd()
    for lambda_val in lambdas:
        for mu1 in mu1s:
            for mu2 in mu2s:
                average_customers, all_customers_in_system = run_simulation(Number_of_simulations, lambda_val, mu1, mu2, T, q1_initial_length, log_file)
                customers_in_system = all_customers_in_system[0]
                # Extract data for plotting
                times = [x[0] for x in customers_in_system]
                queue1_lengths = [x[1] for x in customers_in_system]
                queue2_lengths = [x[2] for x in customers_in_system]

                # Plot L1 and L2
                plt.figure(figsize=(12, 6))
                plt.plot(times, queue1_lengths, label='L1 (Queue Length for Server 1)')
                plt.plot(times, queue2_lengths, label='L2 (Queue Length for Server 2)')
                plt.xlabel('Time')
                plt.ylabel('Queue Length')
                plt.title(f'Queue Lengths over Time for λ={lambda_val}, μ1={mu1}, μ2={mu2}')
                plt.legend()
                plt.grid(True)
                plt.savefig(os.path.join(current_directory, f'queue_lengths_plot_{plot_number}.png'))
                plt.show()
                plot_number += 1

    # Print final message
    print(f"Simulation complete. Plots saved to current working directory with filenames 'queue_lengths_plot_1.png' to 'queue_lengths_plot_{plot_number - 1}.png'")

Simulate_Part_A()
Simulate_Part_B()
