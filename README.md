# Intelligent Logistics Routing System

An Operating System based logistics management system that uses CPU scheduling,
resource allocation and routing concepts to manage delivery tasks efficiently.

## Problem Statement

In a logistics system, multiple delivery requests compete for limited resources
such as vehicles and drivers. Efficient scheduling and resource allocation are
required to decide which delivery should be processed first and which vehicle
should be assigned to it.

This project applies Operating System concepts to a real-world logistics
environment.

## Objectives

- Manage multiple delivery tasks
- Implement CPU scheduling algorithms
- Allocate vehicles to delivery tasks
- Calculate waiting time and turnaround time
- Find efficient delivery routes
- Demonstrate resource conflicts and synchronization
- Study deadlock detection and avoidance

## OS Concepts Used

- FCFS Scheduling
- SJF Scheduling
- Priority Scheduling
- Process Management
- Resource Allocation
- Synchronization
- Deadlock Detection and Avoidance
- Inter-Process Communication
- Graph-based Routing

## Current Implementation

The first prototype currently supports:

- Delivery task creation
- Task priority and burst time
- FCFS scheduling
- SJF scheduling
- Priority scheduling
- Waiting time calculation
- Turnaround time calculation
- Web-based dashboard

## Technology Stack

- Python
- Flask
- HTML
- CSS
- JavaScript
- Linux / Ubuntu
- Git & GitHub

## Project Structure

```text
intelligent-logistics/
│
├── app.py
├── templates/
│   └── index.html
├── .gitignore
└── README.md
