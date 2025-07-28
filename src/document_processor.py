import os
import fitz  # PyMuPDF
from typing import List, Dict
import spacy
from datetime import datetime
from .models import Metadata, ExtractedSection, SubsectionAnalysis, DocumentAnalysis

class DocumentProcessor:
    def __init__(self):
        # Load a smaller spaCy model to stay within size constraints
        self.nlp = spacy.load("en_core_web_sm")
        
    def process_documents(self, 
                         document_paths: List[str], 
                         persona: str, 
                         job_to_be_done: str) -> DocumentAnalysis:
        # Process metadata
        metadata = Metadata(
            input_documents=[os.path.basename(path) for path in document_paths],
            persona=persona,
            job_to_be_done=job_to_be_done,
            processing_timestamp=datetime.now()
        )
        
        # Process all documents
        sections = []
        subsections = []
        
        for doc_path in document_paths:
            doc_sections, doc_subsections = self._process_single_document(doc_path)
            sections.extend(doc_sections)
            subsections.extend(doc_subsections)
        
        # Rank sections by importance
        ranked_sections = self._rank_sections(sections, persona, job_to_be_done)
        
        return DocumentAnalysis(
            metadata=metadata,
            extracted_sections=ranked_sections[:5],  # Top 5 most important sections
            subsection_analysis=subsections
        )
    
    def _process_single_document(self, doc_path: str):
        sections = []
        subsections = []
        
        try:
            doc = fitz.open(doc_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                
                # Extract sections using text analysis
                page_sections = self._extract_sections(text, doc_path, page_num + 1)
                sections.extend(page_sections)
                
                # Extract detailed content for subsection analysis
                if self._is_relevant_page(text):
                    subsections.append(
                        SubsectionAnalysis(
                            document=doc_path.split('/')[-1],
                            refined_text=self._refine_text(text),
                            page_number=page_num + 1
                        )
                    )
            
            doc.close()
        except Exception as e:
            print(f"Error processing document {doc_path}: {str(e)}")
            
        return sections, subsections
    
    def _extract_sections(self, text: str, doc_path: str, page_num: int) -> List[ExtractedSection]:
        sections = []
        # Simple section extraction based on line breaks and text formatting
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if self._is_section_title(line):
                sections.append(
                    ExtractedSection(
                        document=doc_path.split('/')[-1],
                        section_title=line.strip(),
                        importance_rank=0,  # Will be updated later
                        page_number=page_num
                    )
                )
        return sections
    
    def _is_section_title(self, text: str) -> bool:
        # Simple heuristic for section titles
        return (len(text.strip()) > 0 and
                len(text.strip()) < 100 and
                text.strip()[0].isupper() and
                not text.strip().endswith('.'))
    
    def _is_relevant_page(self, text: str) -> bool:
        # Implement relevance checking logic
        doc = self.nlp(text)
        return len(doc.ents) > 0  # Simple check for named entities
    
    def _refine_text(self, text: str) -> str:
        # Clean and refine the text
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return ' '.join(lines)
    
    def _rank_sections(self, sections: List[ExtractedSection], persona: str, job: str) -> List[ExtractedSection]:
        """Rank sections based on relevance to persona and job."""
        # Convert persona and job to lowercase for matching
        persona_lower = persona.lower()
        job_lower = job.lower()
        
        # Define keywords based on persona and job
        keywords = set(persona_lower.split() + job_lower.split())
        
        # Score sections based on keyword matches
        for section in sections:
            title_lower = section.section_title.lower()
            score = sum(1 for keyword in keywords if keyword in title_lower)
            section.importance_rank = score
        
        # Sort by score (descending) and then by title (ascending)
        return sorted(sections, 
                        key=lambda x: (-x.importance_rank, x.section_title))