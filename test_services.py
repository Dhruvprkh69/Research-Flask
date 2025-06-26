#!/usr/bin/env python3
"""
Test script to verify all AI services are working correctly.
Run this script to test the integration before starting the Flask app.
"""

import os
import sys
from config import OPENAI_API_KEY, ARXIV_API_KEY, SEMANTIC_SCHOLAR_API_KEY

# Set environment variables from config
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
os.environ['ARXIV_API_KEY'] = ARXIV_API_KEY
os.environ['SEMANTIC_SCHOLAR_API_KEY'] = SEMANTIC_SCHOLAR_API_KEY

def test_ai_service():
    """Test AI service functionality"""
    print("🧠 Testing AI Service...")
    try:
        from app.services.ai_service import AIService
        ai_service = AIService()
        
        # Test summary generation
        test_text = "This is a test research paper about machine learning and artificial intelligence."
        summary = ai_service.generate_summary(test_text)
        print(f"✅ Summary generation: {'Working' if summary else 'Failed'}")
        
        # Test concept extraction
        concepts = ai_service.extract_key_concepts(test_text)
        print(f"✅ Concept extraction: {'Working' if concepts else 'Failed'}")
        
        return True
    except Exception as e:
        print(f"❌ AI Service Error: {str(e)}")
        return False

def test_pdf_processor():
    """Test PDF processor functionality"""
    print("📄 Testing PDF Processor...")
    try:
        from app.services.pdf_processor import PDFProcessor
        pdf_processor = PDFProcessor()
        
        # Test text processing
        test_text = "This is a test document for processing."
        chunks = pdf_processor.split_text(test_text)
        print(f"✅ Text splitting: {'Working' if chunks else 'Failed'}")
        
        return True
    except Exception as e:
        print(f"❌ PDF Processor Error: {str(e)}")
        return False

def test_citation_service():
    """Test citation service functionality"""
    print("📚 Testing Citation Service...")
    try:
        from app.services.citation_service import CitationService
        citation_service = CitationService()
        
        # Test with a known arXiv paper
        test_url = "https://arxiv.org/abs/1706.03762"  # Attention is All You Need
        citation = citation_service.generate_citation(test_url, "APA")
        print(f"✅ Citation generation: {'Working' if citation else 'Failed'}")
        
        return True
    except Exception as e:
        print(f"❌ Citation Service Error: {str(e)}")
        return False

def test_search_service():
    """Test search service functionality"""
    print("🔍 Testing Search Service...")
    try:
        from app.services.search_service import SearchService
        search_service = SearchService()
        
        # Test paper search
        papers = search_service.find_similar_papers("transformer architecture", "cs.LG", 2)
        print(f"✅ Paper search: {'Working' if papers else 'Failed'}")
        
        return True
    except Exception as e:
        print(f"❌ Search Service Error: {str(e)}")
        return False

def check_environment():
    """Check if environment variables are set"""
    print("🔧 Checking Environment...")
    
    required_vars = ['OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your config.py file")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def main():
    """Run all tests"""
    print("🚀 Starting Service Tests...\n")
    
    # Check environment first
    env_ok = check_environment()
    if not env_ok:
        print("\n❌ Environment check failed. Please fix the issues above.")
        sys.exit(1)
    
    # Test all services
    tests = [
        test_ai_service,
        test_pdf_processor,
        test_citation_service,
        test_search_service
    ]
    
    results = []
    for test in tests:
        print()
        result = test()
        results.append(result)
    
    # Summary
    print("\n" + "="*50)
    print("📊 Test Results Summary")
    print("="*50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All {total} tests passed! Your Research AI Assistant is ready to use.")
        print("\nYou can now run: python run.py")
    else:
        print(f"⚠️  {passed}/{total} tests passed. Some services may not work correctly.")
        print("\nPlease check the error messages above and fix any issues.")
    
    print("="*50)

if __name__ == "__main__":
    main() 