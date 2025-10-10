# DevMatch AI - Project-Developer Matching System

## Overview
DevMatch AI is an intelligent matching system that uses DeepSeek AI to analyze the compatibility between developers and projects. It considers technical skills, motivational alignment, and relevant experiences to provide comprehensive matching scores.

## Features
- ✅ Technical skill matching
- 🧠 AI-powered semantic analysis with DeepSeek
- 📊 Experience relevance evaluation
- 💻 HTML report generation
- 🌐 Flask web interface
- 📱 Responsive design
- 🎯 Individual project views

## Installation & Setup

### Prerequisites
- Python 3.7+
- Ollama with DeepSeek model installed

### Install Ollama and DeepSeek
```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull DeepSeek model
ollama pull deepseek-r1:1.5b
```

### Install Python Dependencies
```bash
# Install Flask (only needed for web server)
pip install -r requirements.txt
```

## Usage Options

### Option 1: Generate Static HTML Report (Recommended)
This generates an HTML file that you can open directly in any web browser:

```bash
python modelai3.py
```

This will:
- Generate a beautiful HTML report with interactive elements
- Save it as `devmatch_results.html`
- Display console output as well
- No server needed - just open the HTML file in your browser

### Option 2: Run Flask Web Server
For a dynamic web interface with API endpoints:

```bash
python flask_server.py
```

Then visit:
- **Main Interface**: http://localhost:5000
- **API Endpoint**: http://localhost:5000/api/results
- **Individual Projects**: http://localhost:5000/project/1, /project/2, /project/3

## Features Breakdown

### Technical Matching
- Calculates percentage of required technologies that the developer possesses
- Direct skill-to-requirement comparison

### AI Analysis with DeepSeek
- **Technical Affinity**: AI evaluation of technical fit
- **Motivational Affinity**: How well the developer's motivation aligns with the project
- **Experience Relevance**: How relevant past experiences are to the project domain
- **Smart Comments**: Natural language explanation of the match

### Experience Integration
The system now considers relevant experiences that might not be directly technical but could enhance project understanding:

- **Ana López**: Barista experience → Coffee shop system understanding
- **Carlos Pérez**: Personal trainer background → Fitness app insights
- **Lucía Martínez**: Teaching experience → Educational platform expertise

## Project Structure

```
├── modelai3.py          # Main matching system with HTML generation
├── flask_server.py      # Flask web server (optional)
├── requirements.txt     # Python dependencies
├── devmatch_results.html # Generated HTML report
└── README.md           # This file
```

## Sample Projects & Developers

### Projects
1. **Coffee Shop Ordering System** - Web application for cafeteria management
2. **Fitness Mobile App** - Progress tracking and health recommendations
3. **Online Course Platform** - Educational content with payment integration

### Developers
1. **Ana López** - Java/Spring Boot developer with barista experience
2. **Carlos Pérez** - Mobile developer with fitness background
3. **Lucía Martínez** - Python/Django developer with teaching experience

## HTML Report Features

- 📊 **Interactive Progress Bars**: Visual representation of matching scores
- 🎨 **Modern Design**: Responsive layout with gradient backgrounds
- 📱 **Mobile Friendly**: Works perfectly on all device sizes
- 🔍 **Detailed Analysis**: Shows skills, experiences, and AI insights
- ⚡ **Fast Loading**: Static HTML with embedded CSS

## API Endpoints (Flask Server)

- `GET /` - Main HTML interface
- `GET /api/results` - JSON API with all matching results
- `GET /project/{id}` - Detailed view for specific project

## Customization

### Adding New Projects
Edit the `projects` list in `modelai3.py`:

```python
projects = [
    {
        "id": 4,
        "name": "Your Project Name",
        "description": "Project description",
        "required_technologies": ["Python", "React"],
        "experience_level": "Intermediate",
        "project_type": "Web",
        "status": "Open"
    }
]
```

### Adding New Developers
Edit the `developers` list in `modelai3.py`:

```python
developers = [
    {
        "id": 4,
        "name": "New Developer",
        "skills": ["Python", "React"],
        "experience_level": "Intermediate",
        "motivation": "Developer motivation",
        "experiences": [
            "Relevant experience 1",
            "Relevant experience 2"
        ]
    }
]
```

## Troubleshooting

### DeepSeek Not Working
- Make sure Ollama is running: `ollama serve`
- Check if DeepSeek model is installed: `ollama list`
- Pull the model if missing: `ollama pull deepseek-r1:1.5b`

### Flask Server Issues
- Install Flask: `pip install flask`
- Check if port 5000 is available
- Try running on different port: modify the `port=5000` parameter

### HTML Report Not Generating
- Check file permissions in the current directory
- Ensure Python has write access to the folder

## License
This project is open source and available under the MIT License.
