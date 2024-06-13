# 15.072-Queue-Modeling
Operations Research Lab concentrates on queuing model for 2 cascaded servers

This repository contains code for simulating a two-server queueing system and analyzing its performance.

Functionality
The code performs two main parts:

Part A: Analyzes average number of customers in the system.

Runs simulations for various arrival rates (lambda), service rates (mu1, mu2), and simulation times (T).
Calculates the average number of customers for each simulation.
Compares the observed average to a theoretical value.
Saves the results to an Excel file.
Part B: Plots queue lengths over time.

Runs a single simulation with a large initial queue length at server 1 (q1).
Extracts queue lengths (L1 and L2) for both servers over time.
Generates plots of L1 and L2 vs. time and saves them as PNG images.
