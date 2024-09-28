from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel, Field, root_validator
from langchain.memory import ConversationBufferMemory
from typing import List

# TODO: Get it from environment variable
OPEN_API_KEY = ""
MODEL_NAME = "gpt-4o-mini"

class ResponseModel(BaseModel):
    action: str = Field(description="Description of the action to be taken.")
    dialogue: str = Field(description="Dialogue spoken by the character.")
    next_steps: List[str] = Field(description="Possible next actions available.")

    # Custom validation to ensure 'action' ends with a question mark
    @root_validator(pre=True)
    def validate_action(cls, values):
        action = values.get("action", "")
        if action == "":
            raise ValueError("The action must not be empty.")
        return values


class VisualNovelAssistant:
    def __init__(self):
        # Initialize the prompt template
        self.prompt_template = PromptTemplate(
            template=("You are the owner of a house in a visual novel. "
                      "A thief (the player) is trying to convince you to let them into the house. The theif will try to manipulate you into believing him."
                      "Note that you are not aware that the person visting your house has malicious intentions."
                      "For example, The theif might say that he came to offer that service you booked. Or he might say that he want to fix your pool for free."
                      "When you first see the player or theif, ask him questions about who is he, why he knocked on your door etc."
                      "Talk like having a normal interaction with a human."
                      "Try to role play with him. Ask clarifying questions based on the difficulty. Based on how well the theif responds let him in or deny the entry."
                      "Here is the world description:\n{world_description}\n"
                      "Difficulty Level: {difficulty}\n"
                      "Respond to the thief's query as the owner in the following JSON format:\n"
                      "{query}\n"
                      "Expected JSON structure:\n"
                      "{{\n"
                      "  \"action\": \"<string describing the action>\",\n"
                      "  \"dialogue\": \"<string containing what the house owner says>\",\n"
                      "  \"next_steps\": [\n"
                      "    \"<string describing next possible actions>\",\n"
                      "    \"<another possible action>\"\n"
                      "  ]\n"
                      "}}\n"),
            input_variables=["world_description", "difficulty", "query"]
        )

        self.memory = ConversationBufferMemory()
        # Initialize the parser
        self.parser = PydanticOutputParser(pydantic_object=ResponseModel)
        
        # Initialize the ChatOpenAI model using the correct api_key and model_name
        self.chat_model = ChatOpenAI(api_key=OPEN_API_KEY, model_name=MODEL_NAME)  # Correct model initialization

    def get_structured_response(self, world_description, difficulty, user_query):
        # Strip inputs for safety
        world_description = world_description.strip()
        difficulty = difficulty.strip()
        user_query = user_query.strip()

        # Create the full prompt
        prompt = self.prompt_template.format(
            world_description=world_description,
            difficulty=difficulty,
            query=user_query
        )
        print("prompt:", prompt)

        # Get the response from the model using .predict() (LangChain method)
        response = self.chat_model.predict(prompt)
        print("response:", response)

        # Parse the output using the specified parser
        structured_output = self.parser.parse(response)

        return structured_output
    
    def clear_memory(self):
        # Clear the memory buffer
        self.memory.clear()

