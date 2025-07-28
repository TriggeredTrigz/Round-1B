import os
import sys
from src.config_loader import ConfigLoader
from src.document_processor import DocumentProcessor
from src.utils import save_analysis_to_json

def main():
    # Configure paths
    # input_dir = os.path.join(os.getcwd(), "data", "input")  
    # output_dir = os.path.join(os.getcwd(), "data", "output")
    input_dir = "/data/input"
    pdfs_dir = os.path.join(input_dir, "PDFs")
    output_dir = "/data/output"
    input_json = os.path.join(input_dir, "challenge1b_input.json")
    output_file = os.path.join(output_dir, "analysis_output.json")
    
    # Validate directories and files
    if not os.path.exists(input_dir):
        print(f"Error: Input directory {input_dir} does not exist")
        sys.exit(1)
    
    if not os.path.exists(pdfs_dir):
        print(f"Error: PDFs directory {pdfs_dir} does not exist")
        sys.exit(1)
    
    if not os.path.exists(input_json):
        print(f"Error: Input JSON file {input_json} does not exist")
        sys.exit(1)
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Load configuration
        config = ConfigLoader.load_input_config(input_json)
        
        # Initialize processor
        processor = DocumentProcessor()
        
        # Get full paths for PDF files
        pdf_files = [
            os.path.join(pdfs_dir, doc.filename)  
            for doc in config.documents
        ]
        
        # Validate PDF files exist
        for pdf_file in pdf_files:
            if not os.path.exists(pdf_file):
                print(f"Error: PDF file not found: {pdf_file}")
                sys.exit(1)
        
        # Process documents
        analysis = processor.process_documents(
            document_paths=pdf_files,
            persona=config.persona.role,
            job_to_be_done=config.job_to_be_done.task
        )
        
        # Save results
        save_analysis_to_json(analysis, output_file)
        print(f"Analysis complete. Results saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()