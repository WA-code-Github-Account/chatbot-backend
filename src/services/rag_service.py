from typing import List, Dict, Any, Optional
from uuid import UUID
from src.services.document_service import DocumentService
from src.services.vector_service import VectorService
from src.services.llm_service import LLMService
from src.services.language_service import LanguageDetectionService
from src.models.user_query import UserQuery
from src.models.source_citation import SourceCitation
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import uuid
import logging


logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.document_service = DocumentService(db_session)
        self.vector_service = VectorService()
        self.llm_service = LLMService()
        self.language_service = LanguageDetectionService()

    async def process_query(
        self,
        query_text: str,
        user_id: UUID,
        language: str = "en",
        max_sources: int = 5
    ) -> Dict[str, Any]:
        """Process a user query using the RAG pipeline"""
        start_time = datetime.utcnow()

        try:
            # Step 1: Detect language if not explicitly provided or verify provided language
            detected_language = self.language_service.detect_language(query_text)

            # Use detected language if none was specified, or validate the specified language
            if language == "detect":
                language = detected_language
            else:
                # If a specific language was requested, still detect to see if translation might be needed
                pass

            # Step 2: Preprocess the query text according to detected language
            processed_query = self.language_service.preprocess_text_for_language(query_text, detected_language)

            # Step 3: Generate embedding for the query
            query_embedding = await self.llm_service.generate_embedding(processed_query)

            # Step 4: Search for relevant document chunks in vector database
            search_results = await self.vector_service.search_similar(
                query_embedding=query_embedding,
                top_k=max_sources
            )

            if not search_results:
                # No relevant documents found
                response = "I don't have information about this in my knowledge base"
                sources = []
            else:
                # Step 5: Get context from relevant chunks
                context_parts = []
                sources = []

                for result in search_results:
                    payload = result.get('payload', {})
                    chunk_content = payload.get('content', '')
                    document_id = payload.get('document_id', '')

                    if chunk_content:
                        # Preprocess context according to language
                        processed_chunk = self.language_service.preprocess_text_for_language(chunk_content, detected_language)
                        context_parts.append(processed_chunk)

                    # Create source citation info
                    source_info = {
                        'document_id': document_id,
                        'score': result.get('score', 0),
                        'content_preview': chunk_content[:200]  # First 200 chars as preview
                    }
                    sources.append(source_info)

                context = "\n\n".join(context_parts)

                # Step 6: Generate response using LLM with context
                response = await self.llm_service.generate_response(
                    prompt=processed_query,
                    context=context,
                    language=language
                )

            # Step 7: Calculate response time
            response_time_ms = (datetime.utcnow() - start_time).total_seconds() * 1000

            # Step 8: Save query and response to database
            user_query = UserQuery(
                id=uuid.uuid4(),
                query_text=query_text,
                user_id=user_id,
                timestamp=datetime.utcnow(),
                response=response,
                source_citations=str([{'id': s['document_id'], 'score': s['score']} for s in sources]),
                response_time_ms=response_time_ms,
                language=language
            )

            self.db_session.add(user_query)
            await self.db_session.commit()

            # Step 8.5: Save source citations to database
            for source in sources:
                citation = SourceCitation(
                    id=uuid.uuid4(),
                    document_id=source.get('document_id', ''),
                    document_title=source.get('document_title', 'Unknown Document'),
                    page_number=source.get('page_number'),
                    section=source.get('section', ''),
                    text_preview=source.get('content_preview', ''),
                    similarity_score=source.get('score', 0),
                    query_id=user_query.id,
                    source_url=source.get('source_url'),
                    source_type=source.get('source_type'),
                    chunk_id=source.get('chunk_id')
                )
                self.db_session.add(citation)

            await self.db_session.commit()

            # Step 9: Format response according to requirements
            result = {
                'response': response,
                'sources': sources,
                'query_time_ms': response_time_ms,
                'language': language
            }

            logger.info(f"Query processed successfully for user {user_id}, response time: {response_time_ms}ms")
            return result

        except Exception as e:
            logger.error(f"Error processing query for user {user_id}: {str(e)}")
            raise

    async def validate_response_accuracy(self, response: str, sources: List[Dict[str, Any]]) -> float:
        """Validate the accuracy of the response against the provided sources"""
        try:
            # Combine all source content
            source_content = " ".join([source.get('content_preview', '') for source in sources])
            
            # Use LLMService to validate accuracy
            accuracy = await self.llm_service.validate_response_accuracy(response, source_content)
            return accuracy
        except Exception as e:
            logger.error(f"Error validating response accuracy: {str(e)}")
            return 0.0

    async def format_citations(self, sources: List[Dict[str, Any]], query_id: UUID = None) -> List[Dict[str, Any]]:
        """Format sources according to citation requirements"""
        formatted_sources = []

        for source in sources:
            formatted_source = {
                'document_id': source.get('document_id', ''),
                'document_title': source.get('document_title', 'Unknown Document'),
                'page_number': source.get('page_number'),
                'section': source.get('section', ''),
                'text_preview': source.get('content_preview', '')[:100] + "...",
                'similarity_score': source.get('score', 0),
                'source_url': source.get('source_url'),
                'source_type': source.get('source_type'),
                'chunk_id': source.get('chunk_id')
            }
            formatted_sources.append(formatted_source)

        return formatted_sources