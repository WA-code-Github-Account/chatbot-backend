from typing import List, Dict, Any
from src.models.source_citation import SourceCitationResponse


def format_citation(source: Dict[str, Any]) -> str:
    """
    Format a source citation according to the required format: [Source: document_name, page/section]
    """
    document_title = source.get('document_title', 'Unknown Document')
    page_number = source.get('page_number')
    section = source.get('section')
    
    citation_parts = [f"Source: {document_title}"]
    
    if page_number is not None:
        citation_parts.append(f"page {page_number}")
    
    if section:
        citation_parts.append(f"section {section}")
    
    return f"[{', '.join(citation_parts)}]"


def format_multiple_citations(sources: List[Dict[str, Any]]) -> str:
    """
    Format multiple source citations
    """
    if not sources:
        return ""
    
    citations = [format_citation(source) for source in sources]
    return " ".join(citations)


def create_source_citation_response(source: Dict[str, Any]) -> SourceCitationResponse:
    """
    Create a SourceCitationResponse object from a source dictionary
    """
    return SourceCitationResponse(
        document_id=source.get('document_id', ''),
        document_title=source.get('document_title', 'Unknown Document'),
        page_number=source.get('page_number'),
        section=source.get('section', ''),
        text_preview=source.get('content_preview', ''),
        similarity_score=source.get('score', 0)
    )