import openai
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
    
    def generate_research_insights(self, topic: str, context: str = "") -> Dict[str, Any]:
        """Generate research insights and analysis for a given topic."""
        try:
            prompt = f"""
            You are an expert research analyst. Provide comprehensive insights about the research topic: "{topic}"
            
            Please provide:
            1. Current state of research in this area
            2. Key challenges and opportunities
            3. Emerging trends and technologies
            4. Potential research directions
            5. Important papers or researchers to follow
            6. Practical applications and implications
            
            Additional context: {context}
            
            Provide a well-structured analysis with specific examples and actionable insights.
            """
            
            client = OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert research analyst with deep knowledge across multiple academic domains."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            insights = response.choices[0].message.content.strip()
            logger.info(f"Generated research insights for topic: {topic}")
            
            return {
                'success': True,
                'topic': topic,
                'insights': insights,
                'generated_at': datetime.now().isoformat(),
                'model': 'gpt-3.5-turbo'
            }
            
        except Exception as e:
            logger.error(f"Error generating research insights: {str(e)}")
            return {
                'success': False,
                'error': f'Error generating insights: {str(e)}',
                'topic': topic
            }
    
    def analyze_paper_structure(self, paper_text: str) -> Dict[str, Any]:
        """Analyze the structure and key components of a research paper."""
        try:
            prompt = f"""
            Analyze the structure and key components of this research paper. Please identify:
            
            1. Paper title and authors
            2. Abstract and main objective
            3. Introduction and background
            4. Methodology and approach
            5. Key findings and results
            6. Conclusions and implications
            7. References and citations
            8. Research contributions
            9. Limitations and future work
            10. Keywords and topics
            
            Paper text:
            {paper_text[:6000]}
            
            Provide a structured analysis with clear sections and bullet points.
            """
            
            client = OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing academic paper structure and content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            analysis = response.choices[0].message.content.strip()
            logger.info("Paper structure analysis completed")
            
            return {
                'success': True,
                'analysis': analysis,
                'text_length': len(paper_text),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing paper structure: {str(e)}")
            return {
                'success': False,
                'error': f'Error analyzing paper: {str(e)}',
                'text_length': len(paper_text)
            }
    
    def generate_literature_review(self, topic: str, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a literature review based on multiple papers."""
        try:
            # Prepare paper summaries
            paper_summaries = []
            for i, paper in enumerate(papers[:10]):  # Limit to 10 papers
                summary = f"Paper {i+1}: {paper.get('title', 'Unknown')}\n"
                summary += f"Authors: {paper.get('authors', 'Unknown')}\n"
                summary += f"Abstract: {paper.get('abstract', 'No abstract available')}\n"
                summary += f"Published: {paper.get('published_date', 'Unknown')}\n"
                paper_summaries.append(summary)
            
            papers_text = "\n\n".join(paper_summaries)
            
            prompt = f"""
            Create a comprehensive literature review for the topic: "{topic}"
            
            Based on the following papers, provide:
            1. Introduction and background
            2. Current state of research
            3. Key findings and methodologies
            4. Gaps in existing research
            5. Future research directions
            6. Conclusions
            
            Papers to review:
            {papers_text}
            
            Write a well-structured literature review that synthesizes the key findings and identifies research opportunities.
            """
            
            client = OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at writing comprehensive literature reviews."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2500,
                temperature=0.4
            )
            
            literature_review = response.choices[0].message.content.strip()
            logger.info(f"Generated literature review for topic: {topic}")
            
            return {
                'success': True,
                'topic': topic,
                'literature_review': literature_review,
                'papers_analyzed': len(papers),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating literature review: {str(e)}")
            return {
                'success': False,
                'error': f'Error generating literature review: {str(e)}',
                'topic': topic
            }
    
    def suggest_research_questions(self, topic: str, context: str = "") -> Dict[str, Any]:
        """Suggest research questions for a given topic."""
        try:
            prompt = f"""
            Generate research questions for the topic: "{topic}"
            
            Please provide:
            1. Fundamental research questions
            2. Applied research questions
            3. Methodological questions
            4. Theoretical questions
            5. Practical implementation questions
            6. Future-oriented questions
            
            Additional context: {context}
            
            For each question, provide:
            - The question itself
            - Why it's important
            - Potential approaches to answer it
            - Expected impact
            
            Generate 10-15 high-quality research questions.
            """
            
            client = OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at formulating research questions across various academic domains."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.6
            )
            
            questions = response.choices[0].message.content.strip()
            logger.info(f"Generated research questions for topic: {topic}")
            
            return {
                'success': True,
                'topic': topic,
                'research_questions': questions,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error suggesting research questions: {str(e)}")
            return {
                'success': False,
                'error': f'Error generating questions: {str(e)}',
                'topic': topic
            }
    
    def analyze_research_trends(self, field: str, time_period: str = "recent") -> Dict[str, Any]:
        """Analyze research trends in a specific field."""
        try:
            prompt = f"""
            Analyze research trends in the field: "{field}" for the {time_period} period.
            
            Please provide:
            1. Emerging topics and themes
            2. Popular methodologies and approaches
            3. Key breakthroughs and innovations
            4. Challenges and limitations
            5. Future directions and opportunities
            6. Notable researchers and institutions
            7. Impact on industry and society
            8. Funding and collaboration trends
            
            Provide a comprehensive analysis with specific examples and data points where possible.
            """
            
            client = OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing research trends and patterns across academic fields."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.5
            )
            
            trends_analysis = response.choices[0].message.content.strip()
            logger.info(f"Analyzed research trends for field: {field}")
            
            return {
                'success': True,
                'field': field,
                'time_period': time_period,
                'trends_analysis': trends_analysis,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing research trends: {str(e)}")
            return {
                'success': False,
                'error': f'Error analyzing trends: {str(e)}',
                'field': field
            }
    
    def generate_research_proposal(self, topic: str, objectives: List[str]) -> Dict[str, Any]:
        """Generate a research proposal outline."""
        try:
            objectives_text = "\n".join([f"- {obj}" for obj in objectives])
            
            prompt = f"""
            Generate a research proposal outline for the topic: "{topic}"
            
            Research objectives:
            {objectives_text}
            
            Please provide:
            1. Executive Summary
            2. Introduction and Background
            3. Problem Statement
            4. Research Objectives
            5. Literature Review
            6. Methodology
            7. Expected Outcomes
            8. Timeline and Milestones
            9. Budget Considerations
            10. Risk Assessment
            11. References
            
            Provide a comprehensive, well-structured research proposal outline.
            """
            
            client = OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at writing research proposals and grant applications."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2500,
                temperature=0.4
            )
            
            proposal = response.choices[0].message.content.strip()
            logger.info(f"Generated research proposal for topic: {topic}")
            
            return {
                'success': True,
                'topic': topic,
                'objectives': objectives,
                'proposal': proposal,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating research proposal: {str(e)}")
            return {
                'success': False,
                'error': f'Error generating proposal: {str(e)}',
                'topic': topic
            } 