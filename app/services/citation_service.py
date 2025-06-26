import requests
import xmltodict
from datetime import datetime
import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CitationService:
    def __init__(self):
        self.arxiv_api_base = "http://export.arxiv.org/api/query"
    
    def get_arxiv_data(self, arxiv_url: str) -> Optional[Dict[str, Any]]:
        """Fetch data from arXiv using the arXiv API."""
        try:
            # Extract arXiv ID from the URL
            if '/abs/' in arxiv_url:
                arxiv_id = arxiv_url.split('/abs/')[-1]
            elif '/pdf/' in arxiv_url:
                arxiv_id = arxiv_url.split('/pdf/')[-1].replace('.pdf', '')
            else:
                arxiv_id = arxiv_url.split('/')[-1]
            
            # Construct the API URL
            api_url = f'{self.arxiv_api_base}?id_list={arxiv_id}'
            
            logger.info(f"Fetching data for arXiv ID: {arxiv_id}")
            
            # Make a request to the arXiv API
            response = requests.get(api_url, timeout=10)
            
            # Parse the response as XML
            if response.status_code == 200:
                data = xmltodict.parse(response.content)
                entry = data['feed']['entry']
                logger.info(f"Successfully fetched data for {arxiv_id}")
                return entry
            else:
                logger.error(f"Failed to fetch data: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching arXiv data: {str(e)}")
            return None

    def format_apa_citation(self, paper_data: Dict[str, Any]) -> str:
        """Format the arXiv paper data into an APA citation."""
        try:
            title = paper_data.get('title', 'No title available').replace("\n", " ").strip()
            authors = paper_data.get('author', [])
            published_date = paper_data.get('published', 'No date available')
            
            # Parse the date
            try:
                year = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%SZ").year
            except:
                year = datetime.now().year

            # Format authors
            if isinstance(authors, list):
                author_names = []
                for author in authors:
                    name_parts = author['name'].split()
                    if len(name_parts) >= 2:
                        author_names.append(f"{name_parts[-1]}, {name_parts[0]}.")
                    else:
                        author_names.append(author['name'])
                
                if len(authors) == 1:
                    authors_str = author_names[0]
                elif len(authors) == 2:
                    authors_str = f"{author_names[0]} & {author_names[1]}"
                else:
                    authors_str = ", ".join(author_names[:-1]) + f", & {author_names[-1]}"
            else:
                name_parts = authors['name'].split()
                if len(name_parts) >= 2:
                    authors_str = f"{name_parts[-1]}, {name_parts[0]}."
                else:
                    authors_str = authors['name']

            # Get arXiv ID
            arxiv_id = paper_data.get('id', '').split('/')[-1]
            
            citation = f"{authors_str} ({year}). {title}. arXiv. https://arxiv.org/abs/{arxiv_id}"
            return citation
            
        except Exception as e:
            logger.error(f"Error formatting APA citation: {str(e)}")
            return "Error formatting citation"

    def format_mla_citation(self, paper_data: Dict[str, Any]) -> str:
        """Format the arXiv paper data into an MLA citation."""
        try:
            title = paper_data.get('title', 'No title available').replace("\n", " ").strip()
            authors = paper_data.get('author', [])
            published_date = paper_data.get('published', 'No date available')
            
            # Parse the date
            try:
                year = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%SZ").year
            except:
                year = datetime.now().year
            
            # Format authors
            if isinstance(authors, list):
                author_names = []
                for author in authors:
                    name_parts = author['name'].split()
                    if len(name_parts) >= 2:
                        author_names.append(f"{name_parts[-1]}, {name_parts[0]}")
                    else:
                        author_names.append(author['name'])
                authors_str = ", and ".join(author_names)
            else:
                name_parts = authors['name'].split()
                if len(name_parts) >= 2:
                    authors_str = f"{name_parts[-1]}, {name_parts[0]}"
                else:
                    authors_str = authors['name']
            
            # Get arXiv ID
            arxiv_id = paper_data.get('id', '').split('/')[-1]
            
            citation = f"{authors_str}. \"{title}.\" arXiv, {year}, https://arxiv.org/abs/{arxiv_id}."
            return citation
            
        except Exception as e:
            logger.error(f"Error formatting MLA citation: {str(e)}")
            return "Error formatting citation"

    def format_chicago_citation(self, paper_data: Dict[str, Any]) -> str:
        """Format the arXiv paper data into a Chicago citation."""
        try:
            title = paper_data.get('title', 'No title available').replace("\n", " ").strip()
            authors = paper_data.get('author', [])
            published_date = paper_data.get('published', 'No date available')
            
            # Parse the date
            try:
                year = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%SZ").year
            except:
                year = datetime.now().year
            
            # Format authors
            if isinstance(authors, list):
                author_names = []
                for author in authors:
                    name_parts = author['name'].split()
                    if len(name_parts) >= 2:
                        author_names.append(f"{name_parts[-1]}, {name_parts[0]}")
                    else:
                        author_names.append(author['name'])
                authors_str = " and ".join(author_names)
            else:
                name_parts = authors['name'].split()
                if len(name_parts) >= 2:
                    authors_str = f"{name_parts[-1]}, {name_parts[0]}"
                else:
                    authors_str = authors['name']
            
            # Get arXiv ID
            arxiv_id = paper_data.get('id', '').split('/')[-1]
            
            citation = f"{authors_str}. \"{title}.\" {year}. arXiv. https://arxiv.org/abs/{arxiv_id}."
            return citation
            
        except Exception as e:
            logger.error(f"Error formatting Chicago citation: {str(e)}")
            return "Error formatting citation"

    def format_ieee_citation(self, paper_data: Dict[str, Any]) -> str:
        """Format the arXiv paper data into an IEEE citation."""
        try:
            title = paper_data.get('title', 'No title available').replace("\n", " ").strip()
            authors = paper_data.get('author', [])
            published_date = paper_data.get('published', 'No date available')
            
            # Parse the date
            try:
                year = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%SZ").year
            except:
                year = datetime.now().year
            
            # Format authors
            if isinstance(authors, list):
                author_names = []
                for author in authors:
                    name_parts = author['name'].split()
                    if len(name_parts) >= 2:
                        author_names.append(f"{name_parts[0]}. {name_parts[-1]}")
                    else:
                        author_names.append(author['name'])
                authors_str = ", ".join(author_names)
            else:
                name_parts = authors['name'].split()
                if len(name_parts) >= 2:
                    authors_str = f"{name_parts[0]}. {name_parts[-1]}"
                else:
                    authors_str = authors['name']
            
            # Get arXiv ID
            arxiv_id = paper_data.get('id', '').split('/')[-1]
            
            citation = f"{authors_str}, \"{title},\" arXiv, {year}. [Online]. Available: https://arxiv.org/abs/{arxiv_id}."
            return citation
            
        except Exception as e:
            logger.error(f"Error formatting IEEE citation: {str(e)}")
            return "Error formatting citation"

    def generate_citation(self, arxiv_url: str, style: str = "APA") -> Dict[str, Any]:
        """Generate citation for a single arXiv paper."""
        try:
            if not arxiv_url:
                return {
                    'success': False,
                    'error': 'ArXiv URL is required'
                }
            
            # Fetch paper data
            paper_data = self.get_arxiv_data(arxiv_url)
            if not paper_data:
                return {
                    'success': False,
                    'error': 'Could not retrieve paper data. Please check the arXiv URL.'
                }
            
            # Generate citation based on style
            if style == "APA":
                citation = self.format_apa_citation(paper_data)
            elif style == "MLA":
                citation = self.format_mla_citation(paper_data)
            elif style == "Chicago":
                citation = self.format_chicago_citation(paper_data)
            elif style == "IEEE":
                citation = self.format_ieee_citation(paper_data)
            else:
                return {
                    'success': False,
                    'error': f'Unsupported citation style: {style}'
                }
            
            return {
                'success': True,
                'citation': citation,
                'style': style,
                'paper_title': paper_data.get('title', 'Unknown'),
                'authors': paper_data.get('author', []),
                'arxiv_id': paper_data.get('id', '').split('/')[-1],
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating citation: {str(e)}")
            return {
                'success': False,
                'error': f'Error generating citation: {str(e)}'
            }

    def generate_bibliography(self, arxiv_urls: list, style: str = "APA") -> Dict[str, Any]:
        """Generate bibliography for multiple arXiv papers."""
        try:
            if not arxiv_urls:
                return {
                    'success': False,
                    'error': 'ArXiv URLs are required'
                }
            
            if len(arxiv_urls) > 20:
                return {
                    'success': False,
                    'error': 'Maximum 20 papers allowed for bibliography'
                }
            
            citations = []
            failed_papers = []
            
            for i, url in enumerate(arxiv_urls):
                try:
                    result = self.generate_citation(url, style)
                    if result['success']:
                        citations.append(result['citation'])
                    else:
                        failed_papers.append(f"Paper {i+1}: {result['error']}")
                except Exception as e:
                    failed_papers.append(f"Paper {i+1}: Error processing")
            
            if not citations:
                return {
                    'success': False,
                    'error': 'No citations could be generated',
                    'failed_papers': failed_papers
                }
            
            bibliography = "\n\n".join(citations)
            
            return {
                'success': True,
                'bibliography': bibliography,
                'style': style,
                'total_papers': len(arxiv_urls),
                'successful_citations': len(citations),
                'failed_papers': failed_papers,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating bibliography: {str(e)}")
            return {
                'success': False,
                'error': f'Error generating bibliography: {str(e)}'
            }

    def get_paper_metadata(self, arxiv_url: str) -> Optional[Dict[str, Any]]:
        """Get paper metadata from arXiv."""
        try:
            paper_data = self.get_arxiv_data(arxiv_url)
            if not paper_data:
                return None
            
            return {
                'title': paper_data.get('title', 'Unknown'),
                'authors': paper_data.get('author', []),
                'abstract': paper_data.get('summary', ''),
                'published_date': paper_data.get('published', ''),
                'updated_date': paper_data.get('updated', ''),
                'categories': paper_data.get('category', []),
                'arxiv_id': paper_data.get('id', '').split('/')[-1],
                'doi': paper_data.get('doi', None),
                'journal_ref': paper_data.get('journal_ref', None)
            }
            
        except Exception as e:
            logger.error(f"Error getting paper metadata: {str(e)}")
            return None 