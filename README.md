# Visual Novel AI Assistant
## Overview
Visual Novel AI Assistant is an interactive visual novel game platform where users can create their own stories and engage with AI models like ChatGPT. Users take on various roles, and the AI dynamically responds to their choices and queries, making the storytelling experience more immersive and adaptive. The AI (powered by models like GPT-4) assumes the role of various characters in the story, allowing users to interact with it as they progress through the narrative.


![](https://github.com/prakhars144/calliope/blob/main/static/sample.png)


## How It Works
Story Setup
Users provide a world description and define the difficulty level of the interaction. The AI then assumes a role within the story and engages in a conversation with the user based on these settings.

For example, in a scenario where the user plays the role of a thief trying to convince the AI (the house owner) to let them inside, the AI dynamically generates dialogue and actions in response to the user's input.

## AI-Powered Interaction
The AI is powered by LangChain and OpenAI’s GPT models, and it is capable of:

1. Role-playing: Adapting responses based on its role in the story.
2. Decision-making: Determining how to react to the player's input and providing next possible actions.
3. 
## Example Workflow
The user provides a world description:

Example: The player is a thief trying to convince the AI, which plays the role of a house owner, to let them inside.
The user sets the difficulty (e.g., "medium").

The user starts interacting with the AI, posing as the thief. The AI responds with dialogue, actions, and possible next steps based on the interaction.

The conversation continues, with the AI adjusting its behavior dynamically based on the ongoing dialogue.

## Usage

1. Update your OEPN API key in `visual_novel_assistant.py`
2. Install dependencies using `requirements.txt`
3. Install ffmpeg using chocolatey
4. Launch the program using `python .\audio_to_text.py`

## Future plans

1. Provide SDK or a simple web server so that game engines can  interact with visual novel assistant
2. Provide example visual novel game using Godot Engine
