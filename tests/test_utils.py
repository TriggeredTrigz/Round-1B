import unittest
import os
import json
from datetime import datetime
from src.utils import save_analysis_to_json, validate_pdf_path, create_output_directory
from src.models import (
    Metadata, 
    ExtractedSection, 
    SubsectionAnalysis, 
    DocumentAnalysis
)

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.test_output_dir = os.path.join(
            os.path.dirname(__file__),
            'test_data',
            'output'
        )
        os.makedirs(self.test_output_dir, exist_ok=True)
        
    def test_validate_pdf_path(self):
        # Create a temporary test PDF file
        test_pdf = os.path.join(self.test_output_dir, "test.pdf")
        with open(test_pdf, 'w') as f:
            f.write("dummy pdf")
            
        self.assertTrue(validate_pdf_path(test_pdf))
        self.assertFalse(validate_pdf_path("nonexistent.pdf"))
        self.assertFalse(validate_pdf_path("test.txt"))
        
        # Cleanup
        os.remove(test_pdf)
        
    def test_create_output_directory(self):
        test_dir = os.path.join(self.test_output_dir, "test_create_dir")
        
        # Test directory creation
        create_output_directory(test_dir)
        self.assertTrue(os.path.exists(test_dir))
        
        # Test recreation of existing directory
        create_output_directory(test_dir)  # Should not raise exception
        
        # Cleanup
        os.rmdir(test_dir)
        
    def test_save_analysis_to_json(self):
        # Create test data
        metadata = Metadata(
            input_documents=["test.pdf"],
            persona="Test Persona",
            job_to_be_done="Test Job",
            processing_timestamp=datetime.now()
        )
        
        extracted_section = ExtractedSection(
            document="test.pdf",
            section_title="Test Section",
            importance_rank=1,
            page_number=1
        )
        
        subsection = SubsectionAnalysis(
            document="test.pdf",
            refined_text="Test refined text",
            page_number=1
        )
        
        analysis = DocumentAnalysis(
            metadata=metadata,
            extracted_sections=[extracted_section],
            subsection_analysis=[subsection]
        )
        
        # Save to JSON
        output_file = os.path.join(self.test_output_dir, "test_output.json")
        save_analysis_to_json(analysis, output_file)
        
        # Verify JSON content
        with open(output_file, 'r') as f:
            data = json.load(f)
            
        self.assertEqual(data["metadata"]["input_documents"], ["test.pdf"])
        self.assertEqual(data["metadata"]["persona"], "Test Persona")
        self.assertEqual(len(data["extracted_sections"]), 1)
        self.assertEqual(len(data["subsection_analysis"]), 1)
        
        # Cleanup
        os.remove(output_file)
        
    def tearDown(self):
        # Cleanup test output directory
        if os.path.exists(self.test_output_dir):
            for file in os.listdir(self.test_output_dir):
                os.remove(os.path.join(self.test_output_dir, file))
            os.rmdir(self.test_output_dir)

if __name__ == '__main__':
    unittest.main()