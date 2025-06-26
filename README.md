# Research AI Assistant - Flask Version

A comprehensive AI-powered research assistant built with Flask, featuring PDF analysis, citation generation, and paper search capabilities.

## Features

- **📄 PDF Analysis**: Upload and analyze research papers with AI-powered summaries, Q&A, and literature reviews
- **📚 Citation Generation**: Generate citations in multiple formats (APA, MLA, Chicago, IEEE) from arXiv URLs
- **🔍 Paper Search**: Find similar research papers using semantic search with SciBERT embeddings
- **🎯 Interactive Q&A**: Ask questions about uploaded papers and get AI-powered answers
- **📊 Literature Review**: Generate comprehensive literature review analyses
- **📈 Trending Papers**: Discover the latest trending papers in various categories

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
cd Research_AI_Flask
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit the `config.py` file and replace the placeholder values with your actual API keys:

```python
# OpenAI API Key for AI services
OPENAI_API_KEY = "sk-proj-your-actual-openai-api-key"

# ArXiv API Key (optional, for enhanced arXiv access)
ARXIV_API_KEY = "your-actual-arxiv-api-key"

# Semantic Scholar API Key (optional, for enhanced paper search)
SEMANTIC_SCHOLAR_API_KEY = "your-actual-semantic-scholar-api-key"

# Flask Secret Key (generate a random one for production)
FLASK_SECRET_KEY = "your-actual-secret-key"
```

### 3. Get API Keys

#### OpenAI API Key (Required)
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add it to your `config.py` file as `OPENAI_API_KEY`

#### ArXiv API Key (Optional)
1. Go to [ArXiv API](https://arxiv.org/help/api)
2. Register for an API key
3. Add it to your `config.py` file as `ARXIV_API_KEY`

#### Semantic Scholar API Key (Optional)
1. Go to [Semantic Scholar API](https://www.semanticscholar.org/product/api)
2. Register for an API key
3. Add it to your `config.py` file as `SEMANTIC_SCHOLAR_API_KEY`

### 4. Run the Application

```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Usage

### PDF Analysis
1. Navigate to "Analyze Papers"
2. Upload a PDF research paper
3. Generate AI-powered summaries, ask questions, or create literature reviews
4. Download results as text files

### Citation Generation
1. Navigate to "Citations"
2. Enter an arXiv URL (e.g., `https://arxiv.org/abs/1706.03762`)
3. Select citation style (APA, MLA, Chicago, IEEE)
4. Generate and download citations

### Paper Search
1. Navigate to "Find Papers"
2. Enter a research concept or topic
3. Select category and number of results
4. Browse similar papers with similarity scores
5. View trending papers in various categories

## Technical Architecture

### Services
- **AI Service**: OpenAI integration for text analysis and generation
- **PDF Processor**: PyPDF2 and LangChain for document processing
- **Citation Service**: arXiv API integration for citation generation
- **Search Service**: SciBERT embeddings and arXiv search for paper discovery

### Dependencies
- **Flask**: Web framework
- **OpenAI**: AI text generation
- **LangChain**: Document processing and QA chains
- **PyPDF2**: PDF text extraction
- **Transformers**: SciBERT model for embeddings
- **ArXiv**: Paper search and metadata
- **FAISS**: Vector similarity search

## File Structure

```
Research_AI_Flask/
├── app/
│   ├── routes/           # Flask route handlers
│   ├── services/         # Business logic services
│   ├── templates/        # HTML templates
│   └── static/          # CSS, JS, uploads
├── instance/            # Database files
├── config.py           # Configuration and API keys
├── requirements.txt     # Python dependencies
├── run.py              # Application entry point
└── README.md           # This file
```

## API Endpoints

### Paper Analysis
- `POST /paper/upload` - Upload PDF file
- `POST /paper/generate-summary` - Generate AI summary
- `POST /paper/ask-question` - Ask questions about paper
- `POST /paper/extract-concepts` - Extract key concepts
- `POST /paper/literature-review` - Generate literature review
- `POST /paper/analyze-methodology` - Analyze methodology
- `POST /paper/download-summary` - Download summary

### Citations
- `POST /citations/generate` - Generate citation
- `POST /citations/batch` - Batch citation generation
- `POST /citations/paper-metadata` - Get paper metadata
- `POST /citations/download` - Download citation

### Search
- `POST /search/search-papers` - Search similar papers
- `GET /search/categories` - Get paper categories
- `POST /search/paper-details` - Get paper details
- `GET /search/trending` - Get trending papers

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**: Ensure your `OPENAI_API_KEY` is set correctly in `config.py`
2. **PDF Upload Issues**: Check file size (max 16MB) and ensure it's a valid PDF
3. **Model Loading Errors**: First run may take time to download AI models
4. **ArXiv API Errors**: Check internet connection and arXiv service status

### Performance Tips

- The first run will download AI models (~2GB total)
- Subsequent runs will be faster as models are cached
- For production, consider using GPU acceleration for better performance

## Security Notes

⚠️ **Important**: Never commit your `config.py` file with real API keys to version control. Add `config.py` to your `.gitignore` file to prevent accidental commits.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub or contact the development team. 