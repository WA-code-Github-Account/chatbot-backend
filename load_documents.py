import os
import asyncio
from pathlib import Path

async def load_book_documents():
    """Load all book markdown files from data/documents"""
    documents_path = Path("data/documents")
    
    if not documents_path.exists():
        print("❌ Documents folder not found!")
        return
    
    # Find all .md files
    md_files = list(documents_path.rglob("*.md"))
    
    print(f"✅ Found {len(md_files)} markdown files")
    
    for md_file in md_files:
        # Read file content
        content = md_file.read_text(encoding='utf-8')
        print(f"📄 Loaded: {md_file.name} ({len(content)} chars)")
    
    print(f"\n🎉 Successfully loaded {len(md_files)} documents!")

if __name__ == "__main__":
    asyncio.run(load_book_documents())
