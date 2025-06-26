from flask import Blueprint, render_template, request, jsonify, current_app, send_file
from app.services.pdf_processor import PDFProcessor
from app.services.ai_service import AIService
import logging
import os
import uuid
import io
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import hashlib

logger = logging.getLogger(__name__)
paper_analysis_bp = Blueprint("paper_analysis", __name__)

# Initialize services
pdf_processor = None
ai_service = None

def get_services():
    global pdf_processor, ai_service
    if pdf_processor is None:
        openai_api_key = current_app.config.get('OPENAI_API_KEY')
        google_api_key = current_app.config.get('GOOGLE_API_KEY')
        
        if not openai_api_key and not google_api_key:
            logger.error("No AI API keys configured")
            return None, None
            
        pdf_processor = PDFProcessor(openai_api_key, google_api_key)
        ai_service = AIService(openai_api_key) if openai_api_key else None
    return pdf_processor, ai_service

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_markdown_to_pdf_text(text):
    """Convert markdown text to PDF-friendly format."""
    lines = text.split('\n')
    pdf_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Handle headers
        if line.startswith('## '):
            pdf_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            pdf_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('# '):
            pdf_lines.append(f'<h1>{line[2:]}</h1>')
        # Handle bullet points
        elif line.startswith('* '):
            pdf_lines.append(f'• {line[2:]}')
        elif line.startswith('- '):
            pdf_lines.append(f'• {line[2:]}')
        # Handle bold text
        elif '**' in line:
            # Simple bold replacement
            line = line.replace('**', '<b>').replace('<b>', '</b>', 1)
            pdf_lines.append(line)
        # Handle LaTeX equations
        elif '$' in line:
            # Keep LaTeX equations as is for now
            pdf_lines.append(line)
        else:
            pdf_lines.append(line)
    
    return '\n'.join(pdf_lines)

@paper_analysis_bp.route('/')
def paper_analysis_page():
    return render_template('paper_analysis.html')

@paper_analysis_bp.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No PDF file uploaded'}), 400
        
        pdf_file = request.files['file']
        if pdf_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not pdf_file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Get services
        pdf_proc, ai_svc = get_services()
        if not pdf_proc:
            return jsonify({'error': 'Services not available. Please check configuration.'}), 500
        
        logger.info(f"Processing PDF: {pdf_file.filename}")
        
        # Extract text from PDF
        text = pdf_proc.extract_text_from_pdf(pdf_file)
        if not text:
            return jsonify({'error': 'Could not extract text from PDF'}), 400
        
        # Split text into chunks
        chunks = pdf_proc.split_text_into_chunks(text)
        if not chunks:
            return jsonify({'error': 'Could not process text chunks'}), 400
        
        # Create vector store
        vector_store = pdf_proc.create_vector_store(chunks)
        if not vector_store:
            return jsonify({'error': 'Could not create vector store'}), 500
        
        # Store vector store in session or cache for later use
        # For now, we'll store it in a simple way - in production you'd use Redis or similar
        session_id = hashlib.md5(f"{pdf_file.filename}_{text[:100]}".encode()).hexdigest()
        
        # Store in a simple in-memory cache (not recommended for production)
        if not hasattr(current_app, 'vector_stores'):
            current_app.vector_stores = {}
        if not hasattr(current_app, 'document_texts'):
            current_app.document_texts = {}
            
        current_app.vector_stores[session_id] = vector_store
        current_app.document_texts[session_id] = text  # Store the original text
        
        return jsonify({
            'success': True,
            'text': text,
            'chunks': chunks,
            'session_id': session_id,
            'filename': pdf_file.filename,
            'message': 'PDF processed successfully'
        })
        
    except Exception as e:
        logger.error(f"Error uploading PDF: {str(e)}")
        return jsonify({'error': f'Error uploading PDF: {str(e)}'}), 500

@paper_analysis_bp.route('/generate-summary', methods=['POST'])
def generate_summary():
    try:
        data = request.get_json()
        session_id = data.get('session_id', '')
        
        if not session_id:
            return jsonify({'error': 'Session ID is required'}), 400
        
        # Get services
        pdf_proc, ai_svc = get_services()
        if not pdf_proc:
            return jsonify({'error': 'Services not available. Please check configuration.'}), 500
        
        # Retrieve vector store from cache to get the original text
        if not hasattr(current_app, 'vector_stores') or session_id not in current_app.vector_stores:
            return jsonify({'error': 'Document session expired. Please upload the document again.'}), 400
        
        if not hasattr(current_app, 'document_texts') or session_id not in current_app.document_texts:
            return jsonify({'error': 'Document text not found. Please upload the document again.'}), 400
        
        # Get the original text
        original_text = current_app.document_texts[session_id]
        
        logger.info("Generating document summary")
        summary = pdf_proc.generate_summary(original_text)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'message': 'Summary generated successfully'
        })
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        return jsonify({'error': f'Error generating summary: {str(e)}'}), 500

@paper_analysis_bp.route('/answer-question', methods=['POST'])
def answer_question():
    try:
        data = request.get_json()
        question = data.get('question', '')
        session_id = data.get('session_id', '')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        if not session_id:
            return jsonify({'error': 'Session ID is required'}), 400
        
        # Get services
        pdf_proc, ai_svc = get_services()
        if not pdf_proc:
            return jsonify({'error': 'Services not available. Please check configuration.'}), 500
        
        # Retrieve vector store from cache
        if not hasattr(current_app, 'vector_stores') or session_id not in current_app.vector_stores:
            return jsonify({'error': 'Document session expired. Please upload the document again.'}), 400
        
        vector_store = current_app.vector_stores[session_id]
        
        logger.info(f"Answering question: {question[:50]}...")
        
        # Answer question
        answer = pdf_proc.answer_question(question, vector_store)
        
        return jsonify({
            'success': True,
            'answer': answer,
            'question': question,
            'message': 'Question answered successfully'
        })
        
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        return jsonify({'error': f'Error answering question: {str(e)}'}), 500

@paper_analysis_bp.route('/analyze-structure', methods=['POST'])
def analyze_structure():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Document text is required'}), 400
        
        # Get services
        pdf_proc, ai_svc = get_services()
        if not pdf_proc or not ai_svc:
            return jsonify({'error': 'Services not available. Please check configuration.'}), 500
        
        logger.info("Analyzing paper structure")
        
        # Analyze paper structure
        result = ai_svc.analyze_paper_structure(text)
        
        if not result['success']:
            return jsonify(result), 400
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error analyzing paper structure: {str(e)}")
        return jsonify({'error': f'Error analyzing structure: {str(e)}'}), 500

@paper_analysis_bp.route('/extract-key-info', methods=['POST'])
def extract_key_info():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Document text is required'}), 400
        
        # Get services
        pdf_proc, ai_svc = get_services()
        if not pdf_proc or not ai_svc:
            return jsonify({'error': 'Services not available. Please check configuration.'}), 500
        
        logger.info("Extracting key information")
        
        # Extract key information
        key_info = pdf_proc.extract_key_information(text)
        
        return jsonify({
            'success': True,
            'key_info': key_info,
            'message': 'Key information extracted successfully'
        })
        
    except Exception as e:
        logger.error(f"Error extracting key info: {str(e)}")
        return jsonify({'error': f'Error extracting key info: {str(e)}'}), 500

@paper_analysis_bp.route('/generate-insights', methods=['POST'])
def generate_insights():
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        context = data.get('context', '')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        # Get services
        pdf_proc, ai_svc = get_services()
        if not pdf_proc or not ai_svc:
            return jsonify({'error': 'Services not available. Please check configuration.'}), 500
        
        logger.info(f"Generating insights for topic: {topic}")
        
        # Generate research insights
        result = ai_svc.generate_research_insights(topic, context)
        
        if not result['success']:
            return jsonify(result), 400
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}")
        return jsonify({'error': f'Error generating insights: {str(e)}'}), 500

@paper_analysis_bp.route('/suggest-questions', methods=['POST'])
def suggest_questions():
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        context = data.get('context', '')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        # Get services
        pdf_proc, ai_svc = get_services()
        if not pdf_proc or not ai_svc:
            return jsonify({'error': 'Services not available. Please check configuration.'}), 500
        
        logger.info(f"Suggesting research questions for topic: {topic}")
        
        # Suggest research questions
        result = ai_svc.suggest_research_questions(topic, context)
        
        if not result['success']:
            return jsonify(result), 400
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error suggesting questions: {str(e)}")
        return jsonify({'error': f'Error suggesting questions: {str(e)}'}), 500

@paper_analysis_bp.route('/extract-concepts', methods=['POST'])
def extract_concepts():
    try:
        data = request.get_json()
        filename = data.get('filename')
        if not filename:
            return jsonify({'error': 'Filename is required'}), 400
        # Placeholder concepts for now
        concepts = ["Machine Learning", "Artificial Intelligence", "Deep Learning", "Neural Networks", "Research Methods"]
        return jsonify({'success': True, 'concepts': concepts})
    except Exception as e:
        return jsonify({'error': f'Error extracting concepts: {str(e)}'}), 500

@paper_analysis_bp.route('/literature-review', methods=['POST'])
def generate_literature_review():
    try:
        data = request.get_json()
        filename = data.get('filename')
        if not filename:
            return jsonify({'error': 'Filename is required'}), 400
        # Placeholder literature review for now
        literature_review = """
        This is a placeholder literature review. The AI integration will provide comprehensive analysis soon.
        
        Structure:
        1. Introduction and Background
        2. Methodology Overview
        3. Key Findings and Results
        4. Theoretical Contributions
        5. Practical Implications
        6. Limitations and Future Work
        7. Conclusion
        """
        return jsonify({'success': True, 'literature_review': literature_review})
    except Exception as e:
        return jsonify({'error': f'Error generating literature review: {str(e)}'}), 500

@paper_analysis_bp.route('/analyze-methodology', methods=['POST'])
def analyze_methodology():
    try:
        data = request.get_json()
        filename = data.get('filename')
        if not filename:
            return jsonify({'error': 'Filename is required'}), 400
        # Placeholder methodology analysis for now
        methodology_analysis = """
        This is a placeholder methodology analysis. The AI integration will provide detailed analysis soon.
        
        Analysis includes:
        1. Research design and approach
        2. Data collection methods
        3. Analysis techniques
        4. Tools and technologies used
        5. Validity and reliability considerations
        """
        return jsonify({'success': True, 'methodology_analysis': methodology_analysis})
    except Exception as e:
        return jsonify({'error': f'Error analyzing methodology: {str(e)}'}), 500

@paper_analysis_bp.route('/download-summary', methods=['POST'])
def download_summary():
    try:
        data = request.get_json()
        summary = data.get('summary', '')
        filename = data.get('filename', 'summary.pdf')
        
        if not summary:
            return jsonify({'error': 'No summary to download'}), 400
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=12
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=8
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        )
        
        # Convert markdown to PDF content
        pdf_content = []
        
        # Add title
        pdf_content.append(Paragraph("Research Paper Summary", title_style))
        pdf_content.append(Spacer(1, 20))
        
        # Process summary text
        lines = summary.split('\n')
        current_text = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_text:
                    pdf_content.append(Paragraph(current_text, normal_style))
                    current_text = ""
                continue
                
            # Handle headers
            if line.startswith('## '):
                if current_text:
                    pdf_content.append(Paragraph(current_text, normal_style))
                    current_text = ""
                pdf_content.append(Paragraph(line[3:], heading_style))
            elif line.startswith('### '):
                if current_text:
                    pdf_content.append(Paragraph(current_text, normal_style))
                    current_text = ""
                pdf_content.append(Paragraph(line[4:], subheading_style))
            elif line.startswith('# '):
                if current_text:
                    pdf_content.append(Paragraph(current_text, normal_style))
                    current_text = ""
                pdf_content.append(Paragraph(line[2:], title_style))
            # Handle bullet points
            elif line.startswith('* ') or line.startswith('- '):
                if current_text:
                    pdf_content.append(Paragraph(current_text, normal_style))
                    current_text = ""
                pdf_content.append(Paragraph(f"• {line[2:]}", normal_style))
            # Handle LaTeX equations (simplified)
            elif '$' in line:
                if current_text:
                    pdf_content.append(Paragraph(current_text, normal_style))
                    current_text = ""
                # Replace LaTeX with simple text for now
                equation_text = line.replace('$', '').replace('\\', '')
                pdf_content.append(Paragraph(f"Equation: {equation_text}", normal_style))
            else:
                if current_text:
                    current_text += " " + line
                else:
                    current_text = line
        
        # Add any remaining text
        if current_text:
            pdf_content.append(Paragraph(current_text, normal_style))
        
        # Build PDF
        doc.build(pdf_content)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename.replace('.pdf', '_summary.pdf'),
            mimetype='application/pdf'
        )
        
    except Exception as e:
        logger.error(f"Error downloading summary: {str(e)}")
        return jsonify({'error': f'Error downloading summary: {str(e)}'}), 500 