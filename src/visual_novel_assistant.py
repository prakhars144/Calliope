from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel, Field, root_validator
from langchain.memory import ConversationBufferMemory
from typing import List
from utils import get_env_variable
from base_prompts import VISUAL_NOVEL_PROMPT  # Import the prompt template


class ResponseModel(BaseModel):
    action: str = Field(description="Description of the action to be taken.")
    dialogue: str = Field(description="Dialogue spoken by the character.")
    facial_expression: str = Field(description="Possible next actions available.")
    persuation_percentage: str = Field(description="Persuation percentage.")


class VisualNovelAssistant:
    def __init__(self):
        # Load the prompt template from base_prompts
        self.prompt_template = VISUAL_NOVEL_PROMPT

        # Initialize the memory to retain conversation history
        self.memory = ConversationBufferMemory(memory_key="chat_history")

        # Initialize the parser
        self.parser = PydanticOutputParser(pydantic_object=ResponseModel)

        # Initialize the ChatOpenAI model using the correct api_key and model_name
        model_name = get_env_variable("MODEL_NAME", "gpt-4o-mini")
        open_api_key = get_env_variable("OPEN_API_KEY", "")
        if not open_api_key.strip():
            # If open_api_key is empty, raise an exception
            raise ValueError("OPEN_API_KEY is empty or not set.")
        self.chat_model = ChatOpenAI(
            api_key=open_api_key, model_name=model_name, temperature=0.7
        )

    def get_structured_response(self, difficulty, user_query):
        # Strip inputs for safety
        difficulty = difficulty.strip()
        user_query = user_query.strip()

        # Retrieve previous chat history from memory
        chat_history = self.memory.load_memory_variables({}).get("chat_history", "")
        chat_history = chat_history.strip()
        # Create the full prompt by including the memory (chat history)
        prompt = self.prompt_template.format(
            difficulty=difficulty, query=user_query, chat_history=chat_history
        )

        print("prompt:", prompt)

        # Get the response from the model using .predict() (LangChain method)
        response = self.chat_model.predict(prompt)

        # Parse the output using the specified parser
        structured_output = self.parser.parse(response)

        # Update the memory with the current interaction
        self.memory.save_context({"input": user_query}, {"output": response})

        return structured_output

    def clear_memory(self):
        # Clear the memory buffer
        self.memory.clear()
