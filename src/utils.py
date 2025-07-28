import os
import json
from datetime import datetime
from .models import DocumentAnalysis

def save_analysis_to_json(analysis: DocumentAnalysis, output_path: str):
    """Convert analysis results to JSON and save to file."""
    
    def datetime_handler(x):
        if isinstance(x, datetime):
            return x.isoformat()
        raise TypeError(f"Object of type {type(x)} is not JSON serializable")
    
    analysis_dict = {
        "metadata": {
            "input_documents": analysis.metadata.input_documents,
            "persona": analysis.metadata.persona,
            "job_to_be_done": analysis.metadata.job_to_be_done,
            "processing_timestamp": analysis.metadata.processing_timestamp
        },
        "extracted_sections": [
            {
                "document": section.document,
                "section_title": section.section_title,
                "importance_rank": section.importance_rank,
                "page_number": section.page_number
            }
            for section in analysis.extracted_sections
        ],
        "subsection_analysis": [
            {
                "document": subsection.document,
                "refined_text": subsection.refined_text,
                "page_number": subsection.page_number
            }
            for subsection in analysis.subsection_analysis
        ]
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis_dict, f, indent=4, default=datetime_handler)

# ...existing code...

def validate_pdf_path(pdf_path: str) -> bool:
    """Validate if the given path is a valid PDF file."""
    return os.path.exists(pdf_path) and pdf_path.lower().endswith('.pdf')

def create_output_directory(directory: str) -> None:
    """Create output directory if it doesn't exist."""
    try:
        os.makedirs(directory, exist_ok=True)
    except Exception as e:
        raise Exception(f"Failed to create output directory: {str(e)}")