# Module 05 - Base Service

## Overview

The Base Service defines the common lifecycle that every long-running
component inside EMMA must follow.

Rather than allowing every module to implement its own startup and
shutdown logic, EMMA standardizes all services using a single interface.

This makes the architecture predictable, scalable, and easier to manage.

---

# Purpose

The purpose of BaseService is to establish a common contract for every
service inside EMMA.

Examples of services include:

- AudioService
- MemoryService
- VisionService
- WakeWordService
- SpeechRecognitionService
- SpeakerService
- LLMService
- ActionService

Every service must implement the same lifecycle methods.

---

# Responsibilities

BaseService is responsible for defining the lifecycle interface.

It defines:

- initialize()
- start()
- stop()

It does NOT implement any functionality itself.

---

# What BaseService DOES NOT Do

BaseService does NOT:

- Read microphones
- Connect to APIs
- Load AI models
- Store memory
- Execute tools

It only defines how services should behave.

---

# Why We Need It

Without BaseService:

AudioService may have

start_audio()

VisionService may have

initialize_camera()

MemoryService may have

boot()

Everything becomes inconsistent.

Instead, every service follows the same lifecycle.

initialize()

↓

start()

↓

stop()

This allows LifecycleManager to control every service in the same way.

---

# Architecture

                   Application
                         │
                         ▼
                 Lifecycle Manager
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   AudioService     MemoryService    VisionService
        ▲                ▲                ▲
        └────────────────┼────────────────┘
                         │
                    BaseService

Every service inherits from BaseService.

---

# Lifecycle

Every service goes through three phases.

1. Initialize

Prepare resources.

Examples:

- Load model
- Open database
- Create directories

2. Start

Begin running.

Examples:

- Start microphone
- Start camera
- Start listening

3. Stop

Release resources.

Examples:

- Close microphone
- Save data
- Close database

---

# Methods

## initialize()

Purpose:

Prepare the service before it starts.

Example:

AudioService

- Detect microphone
- Allocate audio buffers

---

## start()

Purpose:

Begin the actual service.

Example:

Wake Word Service

- Start listening continuously

---

## stop()

Purpose:

Safely shut down the service.

Example:

Speaker Service

- Finish current speech
- Release audio device

---

# Why Abstract Base Class?

Python's Abstract Base Class (ABC) ensures every service implements
the required lifecycle methods.

Without them, Python raises an error.

This prevents incomplete services from entering the system.

---

# Current Services (Planned)

BaseService
│
├── AudioService
├── MemoryService
├── LLMService
├── VisionService
├── SpeakerService
├── WakeWordService
├── ComputerControlService
├── ToolService
├── RoboticsService
└── VehicleService

---

# Future Expansion

Later versions of BaseService may include

pause()

resume()

restart()

health_check()

status()

cleanup()

These methods will support advanced lifecycle management.

---

# Dependencies

Uses:

- abc.ABC
- abc.abstractmethod

No external libraries.

---

# Used By

Application

↓

LifecycleManager

↓

All EMMA Services

---

# Design Principles

Single Responsibility Principle

BaseService only defines the lifecycle.

Open/Closed Principle

New services can be added without changing BaseService.

Consistency

Every service behaves the same way.

Scalability

Supports dozens of services without architectural changes.

---

# Example

class AudioService(BaseService):

    async def initialize(self):
        ...

    async def start(self):
        ...

    async def stop(self):
        ...

LifecycleManager does not need to know what AudioService does.

It simply calls

initialize()

start()

stop()

for every registered service.

---

# Summary

BaseService is one of the foundational building blocks of EMMA.

It creates a consistent lifecycle for every component in the platform.

As EMMA expands into desktop assistants, AI glasses, robotics,
autonomous vehicles, and future AI products, every subsystem will
inherit from this common interface.