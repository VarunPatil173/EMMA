# Module 06 - Service Registry

## Overview

The Service Registry is the central catalog of all long-running services
inside EMMA.

It allows services to be registered, discovered, and retrieved without
creating tight coupling between modules.

---

# Purpose

Provide a single place where all EMMA services are stored.

The registry enables the Application and Lifecycle Manager to work with
services in a generic way rather than hardcoding references.

---

# Responsibilities

- Register services
- Retrieve services by name
- Check if a service exists
- Return all registered services

---

# Does NOT

- Start services
- Stop services
- Initialize services
- Execute business logic

Those responsibilities belong to the Lifecycle Manager and the services
themselves.

---

# Architecture

Application
      │
      ▼
Lifecycle Manager
      │
      ▼
Service Registry
      │
 ┌────┼────┐
 ▼    ▼    ▼
Audio Memory Vision

---

# Public Methods

## register(name, service)

Adds a service to the registry.

Raises an error if the name already exists.

---

## get(name)

Returns the requested service.

Raises an error if it is not registered.

---

## exists(name)

Returns True or False.

---

## all()

Returns every registered service.

---

# Design Principles

- Single Responsibility Principle
- Loose Coupling
- Scalability
- Centralized Service Discovery

---

# Future Expansion

Possible additions:

- unregister()
- replace()
- list_names()
- dependency validation
- service metadata
- health status
- startup priority

---

# Summary

The Service Registry is EMMA's inventory of active services.

It keeps the Application and Lifecycle Manager independent of concrete
service implementations, making the architecture easier to extend and
maintain.