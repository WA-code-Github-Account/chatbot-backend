from groq import AsyncGroq
from config.settings import settings
from typing import List, Dict, Any
import logging


logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.groq_api_key)
        self.default_model = "llama3-70b-8192"  # Using a powerful model for better responses

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding for the provided text using an appropriate model.
        Note: Groq doesn't provide embedding APIs directly, so we'll need to use an alternative approach.
        For now, returning a mock implementation. In a real application, you might use a different service for embeddings.
        """
        # For this implementation, I'll return a mock embedding
        # In a real implementation, you would use an embedding service
        import hashlib
        
        # Create a hash-based mock embedding
        hash_object = hashlib.sha256(text.encode())
        hex_dig = hash_object.hexdigest()
        
        # Convert hex to a list of floats (simplified approach for demo)
        embedding = []
        for i in range(0, len(hex_dig), 2):
            val = int(hex_dig[i:i+2], 16)
            embedding.append((val / 255.0) * 2 - 1)  # Normalize between -1 and 1
        
        # Ensure we have the expected number of dimensions (truncate or pad)
        embedding = embedding[:768]  # Assuming 768 dimensions
        while len(embedding) < 768:
            embedding.append(0.0)
        
        return embedding

    async def generate_response(self, prompt: str, context: str = "", language: str = "en") -> str:
        """
        Generate a response using the LLM based on the prompt and context
        """
        try:
            # Determine the language for the response
            if language == "ur":
                language_instruction = "Urdu"
            elif language == "en":
                language_instruction = "English"
            else:
                language_instruction = language  # Default to the provided language name

            # Construct the full prompt with context
            full_prompt = f"Context: {context}\n\nQuestion: {prompt}\n\nPlease provide a detailed answer based solely on the provided context. If the context doesn't contain the information needed to answer the question, state that clearly. Response should be in {language_instruction}."

            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": full_prompt,
                    }
                ],
                model=self.default_model,
                max_tokens=500,  # Limiting response length
                temperature=0.3,  # Lower temperature for more consistent responses
                # Note: In a full implementation, you might want to adjust other parameters based on language
            )

            response = chat_completion.choices[0].message.content
            return response
        except Exception as e:
            logger.error(f"Error generating response from LLM: {str(e)}")
            raise

    async def validate_response_accuracy(self, response: str, source_context: str) -> float:
        """
        Validate the accuracy of the response against the source context
        This is a simplified implementation - in a real system, you'd use more sophisticated techniques
        """
        # For this implementation, we'll use a simple keyword overlap approach
        response_words = set(response.lower().split())
        context_words = set(source_context.lower().split())
        
        if not context_words:
            return 0.0
        
        overlap = len(response_words.intersection(context_words))
        accuracy = overlap / len(context_words)
        
        # Ensure accuracy is between 0 and 1
        return min(1.0, accuracy)