import unittest
from src.document_processor import DocumentProcessor
from src.models import ExtractedSection

class TestDocumentProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DocumentProcessor()
    
    def test_is_section_title(self):
        self.assertTrue(self.processor._is_section_title("Introduction"))
        self.assertTrue(self.processor._is_section_title("Key Findings"))
        self.assertFalse(self.processor._is_section_title(""))
        self.assertFalse(self.processor._is_section_title("this is a regular sentence."))
    
    def test_refine_text(self):
        input_text = "Line 1\n  Line 2  \n\nLine 3"
        expected = "Line 1 Line 2 Line 3"
        self.assertEqual(self.processor._refine_text(input_text), expected)
    
    def test_rank_sections(self):
        sections = [
            ExtractedSection("doc1.pdf", "Travel Tips", 0, 1),
            ExtractedSection("doc1.pdf", "History", 0, 2),
            ExtractedSection("doc1.pdf", "Planning Guide", 0, 3)
        ]
        
        persona = "Travel Planner"
        job = "Plan a trip"
        
        ranked = self.processor._rank_sections(sections, persona, job)
        
        # Check if travel-related sections are ranked higher
        self.assertEqual(ranked[0].section_title, "Travel Tips")
        self.assertEqual(ranked[1].section_title, "Planning Guide")

if __name__ == '__main__':
    unittest.main()