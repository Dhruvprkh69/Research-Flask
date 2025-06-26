from flask import Blueprint, render_template, request, jsonify
from app.services.citation_service import CitationService
import logging

logger = logging.getLogger(__name__)
citations_bp = Blueprint("citations", __name__)

# Initialize citation service
citation_service = CitationService()

@citations_bp.route('/')
def citations_page():
    return render_template('citations.html')

@citations_bp.route('/generate-citation', methods=['POST'])
def generate_citation():
    try:
        data = request.get_json()
        arxiv_url = data.get('arxiv_url', '')
        style = data.get('style', 'APA')
        
        if not arxiv_url:
            return jsonify({'error': 'ArXiv URL is required'}), 400
        
        logger.info(f"Generating {style} citation for: {arxiv_url}")
        
        # Use real citation service
        result = citation_service.generate_citation(arxiv_url, style)
        
        if not result['success']:
            return jsonify(result), 400
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error generating citation: {str(e)}")
        return jsonify({'error': f'Error generating citation: {str(e)}'}), 500

@citations_bp.route('/generate-bibliography', methods=['POST'])
def generate_bibliography():
    try:
        data = request.get_json()
        arxiv_urls = data.get('arxiv_urls', [])
        style = data.get('style', 'APA')
        
        if not arxiv_urls:
            return jsonify({'error': 'ArXiv URLs are required'}), 400
        
        if len(arxiv_urls) > 20:  # Limit to 20 papers
            return jsonify({'error': 'Maximum 20 papers allowed for bibliography'}), 400
        
        logger.info(f"Generating {style} bibliography for {len(arxiv_urls)} papers")
        
        # Use real citation service
        result = citation_service.generate_bibliography(arxiv_urls, style)
        
        if not result['success']:
            return jsonify(result), 400
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error generating bibliography: {str(e)}")
        return jsonify({'error': f'Error generating bibliography: {str(e)}'}), 500

@citations_bp.route('/paper-metadata', methods=['POST'])
def get_paper_metadata():
    try:
        data = request.get_json()
        arxiv_url = data.get('arxiv_url', '')
        
        if not arxiv_url:
            return jsonify({'error': 'ArXiv URL is required'}), 400
        
        logger.info(f"Fetching metadata for: {arxiv_url}")
        
        # Use real citation service
        metadata = citation_service.get_paper_metadata(arxiv_url)
        
        if not metadata:
            return jsonify({
                'success': False,
                'error': 'Could not retrieve paper metadata'
            }), 404
        
        return jsonify({
            'success': True,
            'metadata': metadata,
            'message': 'Paper metadata retrieved successfully'
        })
        
    except Exception as e:
        logger.error(f"Error fetching paper metadata: {str(e)}")
        return jsonify({'error': f'Error fetching metadata: {str(e)}'}), 500

@citations_bp.route('/download', methods=['POST'])
def download_citation():
    try:
        data = request.get_json()
        citation = data.get('citation', '')
        style = data.get('style', 'APA')
        
        if not citation:
            return jsonify({'error': 'No citation to download'}), 400
        
        # Create filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"citation_{style.lower()}_{timestamp}.txt"
        
        return jsonify({
            'success': True,
            'download_text': citation,
            'filename': filename,
            'message': 'Citation ready for download'
        })
        
    except Exception as e:
        logger.error(f"Error preparing download: {str(e)}")
        return jsonify({'error': f'Error preparing download: {str(e)}'}), 500 