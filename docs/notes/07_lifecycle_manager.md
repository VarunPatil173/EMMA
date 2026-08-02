# Module 07 - Lifecycle Manager

## Overview

The Lifecycle Manager is responsible for coordinating the startup and
shutdown of every service in EMMA.

It works together with the Service Registry but has a different
responsibility.

---

# Purpose

Provide a single place that manages:

- Service initialization
- Service startup
- Service shutdown

---

# Responsibilities

- Initialize services
- Start services
- Stop services
- Maintain startup order
- Maintain shutdown order

---

# Does NOT

- Create services
- Store services
- Execute AI logic

---

# Workflow

Application

↓

Lifecycle Manager

↓

Service Registry

↓

Services

---

# Why Reverse Shutdown?

Dependencies are usually created from bottom to top.

Stopping them in reverse prevents dependent services from failing.

---

# Future Expansion

- Dependency graph
- Parallel startup
- Health monitoring
- Restart failed services
- Startup priorities
- Shutdown timeout
- Graceful cancellation

---

# Design Principles

- Single Responsibility Principle
- Separation of Concerns
- Predictable Lifecycle
- Scalability

---

# Summary

The Lifecycle Manager is the runtime coordinator of EMMA.

It ensures every service starts and stops in a controlled and
predictable manner.