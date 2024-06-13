
## Queueing System Simulation 📊

This repository implements a two-server queueing system simulation to analyze performance metrics.

### Functionality 🛠️

The code performs two main analyses:

**Part A:  Average Number of Customers**

-   Runs multiple simulations for various combinations of:
    -   Arrival rates (lambda)
    -   Service rates (mu1, mu2)
    -   Simulation times (T)
-   Calculates the average number of customers in the system for each simulation run.
-   Compares the observed average to a theoretical value based on arrival and service rates.
-   Saves the results, including error percentages, to an Excel file for further analysis.

**Part B: Queue Lengths over Time**

-   Runs a single simulation with a specific parameter set and a large initial queue length at server 1 (q1).
-   Captures queue lengths (L1 and L2) for both servers at regular intervals throughout the simulation.
-   Generates informative plots visualizing the changes in L1 and L2 over time.
-   Saves the plots as PNG images for clear representation.

### Code Structure 🧩

The code is organized into well-defined functions for better readability and maintainability:

-   `theoretical_avg_customers`: Calculates the theoretical average number of customers based on arrival and service rates.
-   `calculate_error_percentage`: Computes the error percentage between the theoretical and observed average number of customers.
-   `determine_state`: Determines the next significant event (arrival, service completion) based on current time and service end times.
-   `take_snapshot`: Records the queue lengths at specific points in time.
-   `log_state`: Logs the system state (idle, arrival, service completion) and queue lengths to a file for potential debugging or further analysis.
-   `run_simulation`: Executes a single simulation for a given set of parameters, returning the average number of customers and a list of snapshots.
-   `Simulate_Part_A`: Manages simulations for all parameter combinations in Part A, calculates error percentages, and saves results to an Excel file.
-   `Simulate_Part_B`: Runs a single simulation for a specific parameter set in Part B, extracts queue lengths over time, and generates plots.
