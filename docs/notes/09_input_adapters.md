# Input Adapters

## Purpose

Input adapters convert different user input mechanisms into the common
EMMA `InputEvent` representation.

## Supported Inputs

### Text

`TextInput` receives commands typed by the user.

Flow:

Text
→ TextInput
→ InputEvent

### Voice

`AudioInput` receives transcripts produced by the speech-recognition
pipeline.

Flow:

Microphone
→ Audio Processing
→ Speech Recognition
→ AudioInput
→ InputEvent

## Important Design Principle

Input adapters do not execute commands.

They only normalize input into the common `InputEvent` format.

This allows the rest of EMMA to remain independent of the input source.

## Future Inputs

The architecture can later support:

- Camera
- Gesture
- Wake word
- External devices
- API events
- Mobile application input