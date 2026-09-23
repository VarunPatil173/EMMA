# EMMA

**EMMA** is an experimental Python project I built to explore how an AI assistant can be designed and engineered beyond a simple chatbot.

This repository is primarily a **learning and experimentation project**. It contains the architectural experiments, implementations, and engineering decisions I made while learning about AI assistants, Python systems, LLM integration, memory, perception, and service-based architecture.

## What I Learned

While developing EMMA, I explored and practiced:

* Python project structure and modular architecture
* Object-oriented programming and abstraction
* Pydantic and configuration management
* Environment variables and API key management
* Logging and application configuration
* Async programming and service lifecycles
* Dependency management
* Interface and adapter patterns
* Unit and integration testing with `pytest`
* SQLite and persistent data storage
* Memory storage and retrieval concepts
* LLM provider integration
* Local LLMs using Ollama
* Cloud LLM integration
* Model/provider abstraction
* Conversation and agent architecture
* Text input processing
* Voice input and speech-to-text
* Audio processing concepts
* Wake-word detection
* Text-to-speech
* Event-driven input concepts
* Separation of domain logic and infrastructure
* Designing components that can be tested independently

## Things I Explored

Some of the technologies and concepts explored in this project include:

* **Python 3.11**
* **Pydantic / Pydantic Settings**
* **SQLite**
* **Ollama**
* **Google Gemini API**
* **faster-whisper**
* **Edge TTS**
* **OpenWakeWord**
* **NumPy**
* **FAISS**
* **sounddevice**
* **soundfile**
* **WebRTC VAD**
* **pytest**
* **Ruff**
* **Black**

The goal was not to use every technology simply because it exists. Each was explored to understand how different parts of an AI assistant could be implemented and connected.

## Architecture Experiments

The project went through several iterations while I learned more about software architecture.

I experimented with separating different responsibilities such as:

```text
Input / Perception
       ↓
Application / Runtime
       ↓
Intelligence
       ↓
Memory
       ↓
Interfaces / Actions
```

I also explored concepts such as:

* Service lifecycle management
* Service registries
* Provider abstraction
* Persistent memory
* Input adapters
* Agent abstractions
* Runtime services
* Domain models
* Repository patterns
* Separation between AI reasoning and deterministic application logic

A major part of the project was learning **where abstractions are useful and where they simply create unnecessary complexity**.

## Why I Am Pausing the Project

I am intentionally pausing development of EMMA at this stage.

As the project grew, I realized that continuously adding features without first establishing a stronger overall architecture would make the codebase increasingly difficult to change and maintain.

Instead of continuing to add features to an architecture that I was still learning how to design, I decided to stop and treat this repository as a **completed learning/foundation experiment**.

This gives me the opportunity to apply what I learned here to future projects with better architectural decisions from the beginning.

## What This Repository Can Be Used For

This repository may be useful to someone who wants to:

* Study a small Python AI-assistant project
* Explore LLM provider integration
* Experiment with local and cloud AI models
* Understand basic AI assistant architecture
* Learn about persistent memory with SQLite
* Explore voice input pipelines
* Experiment with speech-to-text and text-to-speech
* Study Python service architecture
* Look at examples of testing an AI-related application
* Compare different architectural approaches
* Use parts of the implementation as a starting point for experimentation

It should be viewed as an **experimental/educational codebase**, rather than a finished production assistant.

## What I Took Away From the Project

The biggest lesson from EMMA was not a particular library or API.

It was learning that **building a system is different from simply making individual features work**.

Adding another feature is often easy. Designing the boundaries between features so that the system remains understandable, testable, and changeable is much harder.

That is the main reason I am preserving this repository rather than deleting it: it represents the engineering experiments and mistakes that helped me understand that difference.

## Status

**Development paused — repository preserved for learning and reference.**

The repository remains public as a record of the concepts I explored and the engineering lessons I gained while building it.
