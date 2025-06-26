import os
import logging
from typing import Dict, Any, Optional, List
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import google.generativeai as genai
import openai
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self, openai_api_key: str, google_api_key: str = None):
        self.openai_api_key = openai_api_key
        self.google_api_key = google_api_key
        
        # Initialize Google Gemini if API key is provided
        if self.google_api_key:
            try:
                genai.configure(api_key=self.google_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("Google Gemini API configured successfully")
            except Exception as e:
                logger.error(f"Error configuring Google Gemini: {str(e)}")
                self.gemini_model = None
        else:
            self.gemini_model = None
            logger.warning("Google API key not provided. Using OpenAI for summarization.")
        
        # Initialize embeddings and text splitter
        try:
            self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=5000,
                chunk_overlap=500
            )
            logger.info("Embeddings and text splitter initialized")
        except Exception as e:
            logger.error(f"Error initializing embeddings: {str(e)}")
            self.embeddings = None
            self.text_splitter = None
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from uploaded PDF file."""
        try:
            text = ""
            pdf_reader = PdfReader(pdf_file)
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text.strip():
                        text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                except Exception as e:
                    logger.warning(f"Error extracting text from page {page_num + 1}: {str(e)}")
                    continue
            
            if not text.strip():
                logger.warning("No text extracted from PDF")
                return ""
            
            logger.info(f"Successfully extracted {len(text)} characters from PDF")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    def split_text_into_chunks(self, text: str) -> List[str]:
        """Split text into chunks for processing."""
        try:
            if not text.strip():
                return []
            
            if not self.text_splitter:
                logger.error("Text splitter not initialized")
                return []
            
            chunks = self.text_splitter.split_text(text)
            logger.info(f"Split text into {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error splitting text: {str(e)}")
            return []
    
    def create_vector_store(self, chunks: List[str]) -> Optional[Dict[str, Any]]:
        """Create vector store from text chunks using sentence-transformers."""
        try:
            if not chunks:
                logger.warning("No chunks provided for vector store")
                return None
            
            if not self.embeddings:
                logger.error("Embeddings not initialized")
                return None
            
            # Create embeddings for all chunks
            embeddings = self.embeddings.encode(chunks)
            
            # Convert NumPy arrays to lists for JSON serialization
            embeddings_list = embeddings.tolist()
            
            vector_store = {
                'chunks': chunks,
                'embeddings': embeddings_list,
                'model_name': 'all-MiniLM-L6-v2'
            }
            
            logger.info("Vector store created successfully")
            return vector_store
            
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            return None
    
    def similarity_search(self, vector_store: Dict[str, Any], query: str, k: int = 3) -> List[str]:
        """Search for similar chunks using cosine similarity."""
        try:
            if not vector_store or not self.embeddings:
                return []
            
            # Encode the query
            query_embedding = self.embeddings.encode([query])
            
            # Convert embeddings back to NumPy array for similarity calculation
            embeddings_array = np.array(vector_store['embeddings'])
            
            # Calculate cosine similarity
            from sklearn.metrics.pairwise import cosine_similarity
            similarities = cosine_similarity(query_embedding, embeddings_array)[0]
            
            # Get top k most similar chunks
            top_indices = np.argsort(similarities)[-k:][::-1]
            
            return [vector_store['chunks'][i] for i in top_indices]
            
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            return []
    
    def convert_to_latex(self, text: str) -> str:
        """Convert mathematical expressions to LaTeX format."""
        # Common mathematical patterns
        patterns = {
            r'(\d+)\^(\d+)': r'\1^{\2}',  # Superscript
            r'(\d+)_(\d+)': r'\1_{\2}',   # Subscript
            r'sigma': r'\\sigma',          # Sigma
            r'alpha': r'\\alpha',          # Alpha
            r'beta': r'\\beta',            # Beta
            r'gamma': r'\\gamma',          # Gamma
            r'delta': r'\\delta',          # Delta
            r'epsilon': r'\\epsilon',      # Epsilon
            r'lambda': r'\\lambda',        # Lambda
            r'mu': r'\\mu',                # Mu
            r'pi': r'\\pi',                # Pi
            r'omega': r'\\omega',          # Omega
            r'\\frac': r'\\frac',          # Fraction
            r'\\sum': r'\\sum',            # Summation
            r'\\prod': r'\\prod',          # Product
            r'\\int': r'\\int',            # Integral
            r'\\sqrt': r'\\sqrt',          # Square root
            r'\\infty': r'\\infty',        # Infinity
            r'\\partial': r'\\partial',    # Partial derivative
            r'\\nabla': r'\\nabla',        # Nabla
            r'\\cdot': r'\\cdot',          # Dot product
            r'\\times': r'\\times',        # Times
            r'\\div': r'\\div',            # Division
            r'\\pm': r'\\pm',              # Plus minus
            r'\\leq': r'\\leq',            # Less than or equal
            r'\\geq': r'\\geq',            # Greater than or equal
            r'\\neq': r'\\neq',            # Not equal
            r'\\approx': r'\\approx',      # Approximately
            r'\\propto': r'\\propto',      # Proportional to
            r'\\in': r'\\in',              # Element of
            r'\\subset': r'\\subset',      # Subset
            r'\\cup': r'\\cup',            # Union
            r'\\cap': r'\\cap',            # Intersection
        }
        
        # Replace patterns in text
        for pattern, replacement in patterns.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def generate_summary(self, text: str) -> str:
        """Generate comprehensive summary using Google Gemini or OpenAI."""
        try:
            if not text.strip():
                return "No text available for summarization."
            
            prompt = f"""
            You are an AI assistant specializing in creating detailed summaries of academic documents for literature reviews. 
            Your task is to summarize the document following these guidelines:

            1. Identify the main theories or concepts discussed.
            2. Summarize the key findings from relevant studies.
            3. Highlight areas of agreement or consensus in the research.
            4. Summarize the methodologies used in the research.
            5. Provide an overview of the potential implications of the research.
            6. Suggest possible directions for future research based on the current literature.
            7. If there is any architecture used then explain the architecture of model stepwise.
            
            Additionally, provide detailed explanations of the mathematical aspects of the research paper:
            
            8. Describe and explain the key mathematical models, theorems, or equations used in the paper.
            For each equation, please format it in LaTeX style using the following format:
            $equation$
            
            Document text:
            {text[:8000]}  # Limit text length for API
            
            Please provide a comprehensive, well-structured summary that covers all these aspects.
            Format the output with proper markdown:
            - Use ## for main sections (1-8)
            - Use ### for subsections
            - Use bullet points with * for lists
            - Use **bold** for emphasis
            - Use proper LaTeX formatting for equations
            """
            
            # Try Google Gemini first, fallback to OpenAI
            if self.gemini_model:
                try:
                    response = self.gemini_model.generate_content(prompt)
                    summary = response.text.strip()
                    logger.info("Summary generated using Google Gemini")
                    return summary
                except Exception as e:
                    logger.warning(f"Google Gemini failed, falling back to OpenAI: {str(e)}")
            
            # Fallback to OpenAI
            if self.openai_api_key:
                from openai import OpenAI
                client = OpenAI(api_key=self.openai_api_key)
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert research assistant specializing in academic paper analysis and summarization. Always format output with proper markdown and LaTeX."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2000,
                    temperature=0.3
                )
                
                summary = response.choices[0].message.content.strip()
                logger.info("Summary generated using OpenAI")
                return summary
            else:
                return "Error: No AI service configured for summarization."
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return f"Error generating summary: {str(e)}"
    
    def answer_question(self, question: str, vector_store: Dict[str, Any]) -> str:
        """Answer questions about the document using vector search."""
        try:
            if not vector_store:
                return "No document has been processed yet. Please upload a document first."
            
            # Search for relevant chunks
            relevant_chunks = self.similarity_search(vector_store, question, k=3)
            context = "\n\n".join(relevant_chunks)
            
            prompt = f"""
            You are an AI research assistant. Use the provided context from research papers to answer the question as accurately as possible. 
            If the answer is not available in the context, respond with, "The information is not available in the provided context."

            Context: {context}
            Question: {question}
            
            Please provide a clear, concise answer based on the context provided.
            """
            
            # Try Google Gemini first, fallback to OpenAI
            if self.gemini_model:
                try:
                    response = self.gemini_model.generate_content(prompt)
                    answer = response.text.strip()
                    logger.info("Question answered using Google Gemini")
                    return answer
                except Exception as e:
                    logger.warning(f"Google Gemini failed, falling back to OpenAI: {str(e)}")
            
            # Fallback to OpenAI
            if self.openai_api_key:
                from openai import OpenAI
                client = OpenAI(api_key=self.openai_api_key)
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert research assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.3
                )
                
                answer = response.choices[0].message.content.strip()
                logger.info("Question answered using OpenAI")
                return answer
            else:
                return "Error: No AI service configured for question answering."
            
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return f"Error answering question: {str(e)}"
    
    def extract_key_information(self, text: str) -> Dict[str, Any]:
        """Extract key information from the document."""
        try:
            prompt = f"""
            Extract key information from this academic document and return it in a structured format.
            Please identify:
            1. Title of the paper
            2. Authors (if mentioned)
            3. Abstract or main objective
            4. Key methodologies used
            5. Main findings or results
            6. Keywords or key terms
            7. Publication year (if mentioned)
            8. Research field or domain
            
            Document text:
            {text[:6000]}
            
            Return the information in a clear, structured format.
            """
            
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at extracting structured information from academic documents."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.2
            )
            
            extracted_info = response.choices[0].message.content.strip()
            logger.info("Key information extracted successfully")
            
            return {
                'extracted_info': extracted_info,
                'text_length': len(text),
                'processing_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error extracting key information: {str(e)}")
            return {
                'error': f"Error extracting key information: {str(e)}",
                'text_length': len(text),
                'processing_time': datetime.now().isoformat()
            }
    
    def process_document(self, pdf_file) -> Dict[str, Any]:
        """Complete document processing pipeline."""
        try:
            logger.info("Starting document processing")
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_file)
            if not text:
                return {
                    'success': False,
                    'error': 'Failed to extract text from PDF'
                }
            
            # Split into chunks
            chunks = self.split_text_into_chunks(text)
            if not chunks:
                return {
                    'success': False,
                    'error': 'Failed to create text chunks'
                }
            
            # Create vector store
            vector_store = self.create_vector_store(chunks)
            if not vector_store:
                return {
                    'success': False,
                    'error': 'Failed to create vector store'
                }
            
            # Extract key information
            key_info = self.extract_key_information(text)
            
            logger.info("Document processing completed successfully")
            
            return {
                'success': True,
                'text': text,
                'chunks': chunks,
                'chunks_count': len(chunks),
                'text_length': len(text),
                'key_info': key_info,
                'message': 'Document processed successfully!'
            }
            
        except Exception as e:
            logger.error(f"Error in document processing: {str(e)}")
            return {
                'success': False,
                'error': f'Error processing document: {str(e)}'
            } 