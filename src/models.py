from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

# Input JSON models
@dataclass
class Document:
    filename: str
    title: str

@dataclass
class Persona:
    role: str

@dataclass
class JobToBeDone:
    task: str

@dataclass
class ChallengeInfo:
    challenge_id: str
    test_case_name: str
    description: str

@dataclass
class InputConfig:
    challenge_info: ChallengeInfo
    documents: List[Document]
    persona: Persona
    job_to_be_done: JobToBeDone

# Input PDF models
@dataclass
class Metadata:
    input_documents: List[str]
    persona: str
    job_to_be_done: str
    processing_timestamp: datetime

@dataclass
class ExtractedSection:
    document: str
    section_title: str
    importance_rank: int
    page_number: int

@dataclass
class SubsectionAnalysis:
    document: str
    refined_text: str
    page_number: int

@dataclass
class DocumentAnalysis:
    metadata: Metadata
    extracted_sections: List[ExtractedSection]
    subsection_analysis: List[SubsectionAnalysis]