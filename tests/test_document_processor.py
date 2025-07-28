import unittest
import os
from src.document_processor import DocumentProcessor
from src.models import ExtractedSection, SubsectionAnalysis

class TestDocumentProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DocumentProcessor()
        self.test_data_dir = os.path.join(
            os.path.dirname(__file__),
            'test_data'
        )
        
    def test_is_section_title(self):
        # Test valid section titles
        self.assertTrue(self.processor._is_section_title("Introduction"))
        self.assertTrue(self.processor._is_section_title("Key Findings"))
        self.assertTrue(self.processor._is_section_title("1. Executive Summary"))
        
        # Test invalid section titles
        self.assertFalse(self.processor._is_section_title(""))
        self.assertFalse(self.processor._is_section_title("this is a regular sentence."))
        self.assertFalse(self.processor._is_section_title("   "))
        self.assertFalse(self.processor._is_section_title("a" * 101))  # Too long
    
    def test_refine_text(self):
        # Test basic text refinement
        input_text = "Line 1\n  Line 2  \n\nLine 3"
        expected = "Line 1 Line 2 Line 3"
        self.assertEqual(self.processor._refine_text(input_text), expected)
        
        # Test empty lines and spaces
        input_text = "\n\n  Test  \n\n  Text  \n"
        expected = "Test Text"
        self.assertEqual(self.processor._refine_text(input_text), expected)
        
        # Test single line
        self.assertEqual(self.processor._refine_text("Single"), "Single")
    
    def test_rank_sections(self):
        sections = [
            ExtractedSection("doc1.pdf", "Travel Tips", 0, 1),
            ExtractedSection("doc1.pdf", "History", 0, 2),
            ExtractedSection("doc1.pdf", "Planning Guide", 0, 3),
            ExtractedSection("doc1.pdf", "Travel Planner's Notes", 0, 4),
            ExtractedSection("doc1.pdf", "Local Cuisine", 0, 5)
        ]
        
        persona = "Travel Planner"
        job = "Plan a trip"
        
        ranked = self.processor._rank_sections(sections, persona, job)
        
        # Check if travel-related sections are ranked higher
        self.assertEqual(ranked[0].section_title, "Travel Planner's Notes")
        self.assertEqual(ranked[1].section_title, "Travel Tips")
        self.assertEqual(ranked[2].section_title, "Planning Guide")
        
    def test_is_relevant_page(self):
        # Test page with named entities
        text_with_entities = "Paris is the capital of France. The Eiffel Tower is beautiful."
        self.assertTrue(self.processor._is_relevant_page(text_with_entities))
        
        # Test page without named entities
        text_without_entities = "The weather was nice that day."
        self.assertFalse(self.processor._is_relevant_page(text_without_entities))
    
    def test_extract_sections(self):
        test_text = """Introduction
        This is introduction text.
        
        Chapter 1: Getting Started
        This is chapter content.
        
        Summary
        This is the summary."""
        
        sections = self.processor._extract_sections(test_text, "test.pdf", 1)
        
        self.assertEqual(len(sections), 3)
        self.assertEqual(sections[0].section_title, "Introduction")
        self.assertEqual(sections[1].section_title, "Chapter 1: Getting Started")
        self.assertEqual(sections[2].section_title, "Summary")

if __name__ == '__main__':
    unittest.main()