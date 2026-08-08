input_source.py
Purpose

This file defines where an input came from.

Today:

Voice
Text

Tomorrow:

Vision
Screen
Robot

Without changing the rest of EMMA.

Why Enum?

Instead of:

source = "voice"

Someone later writes:

source = "Voice"

or

source = "VOICE"

Now comparisons fail.

Enums eliminate this entire class of bugs.

File 2
input_event.py
Purpose

This is one of the most important classes in EMMA.

Every input becomes an InputEvent.

Nothing bypasses it.