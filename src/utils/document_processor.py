import re
from typing import List, Dict, Any
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace


class DocumentProcessor:
    """
    Utility class for processing documents, including chunking and metadata extraction
    """

    def __init__(self):
        # Initialize a basic tokenizer; in a real implementation, you might load a pre-trained one
        self.tokenizer = None  # We'll initialize this as needed
        pass

    def chunk_document(self, content: str, max_tokens: int = 1000, overlap: int = 100) -> List[Dict[str, Any]]:
        """
        Split document content into chunks of approximately max_tokens with specified overlap
        """
        # For this implementation, we'll use a simple approach
        # In a real implementation, you'd use a tokenizer to ensure token limits are respected
        
        # First, estimate tokens by counting words (1 word ~ 1 token on average)
        words = content.split()
        chunks = []
        start_idx = 0
        
        while start_idx < len(words):
            # Determine the end index for this chunk
            end_idx = start_idx + max_tokens
            
            # Extract the chunk
            chunk_words = words[start_idx:end_idx]
            chunk_content = " ".join(chunk_words)
            
            # Add the chunk to our list
            chunks.append({
                "content": chunk_content,
                "chunk_order": len(chunks),
                "token_count": len(chunk_words)
            })
            
            # Move the start index to account for overlap
            start_idx = end_idx - overlap if end_idx < len(words) else len(words)
        
        return chunks

    def extract_metadata(self, content: str, source_type: str, filename: str = None) -> Dict[str, Any]:
        """
        Extract metadata from the document
        """
        metadata = {
            "source_type": source_type,
            "filename": filename,
            "word_count": len(content.split()),
            "char_count": len(content),
            "line_count": len(content.splitlines())
        }
        
        # Extract more specific metadata based on source type
        if source_type == "text/plain":
            # For text files, we might look for titles, author info, etc.
            lines = content.splitlines()
            if lines:
                metadata["first_line"] = lines[0][:100]  # First 100 chars of first line
        elif source_type == "application/pdf":
            # In a real implementation, you'd use a PDF library to extract metadata
            pass
        elif source_type == "text/html":
            # In a real implementation, you'd parse HTML to extract title, meta tags, etc.
            pass
            
        return metadata

    def process_document_content(self, content: str, source_type: str = "text/plain") -> Dict[str, Any]:
        """
        Process document content: chunking and metadata extraction
        """
        # Extract metadata
        metadata = self.extract_metadata(content, source_type)
        
        # Create chunks
        chunks = self.chunk_document(content)
        
        return {
            "metadata": metadata,
            "chunks": chunks
        }