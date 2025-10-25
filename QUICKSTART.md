# TK Reports - Quick Start Guide

## Getting Started in 3 Easy Steps

### Step 1: Setup the Environment

```bash
# Navigate to the project directory
cd "/Users/efeobukohwo/Desktop/TK Reports"

# Run the setup script (macOS/Linux)
./setup.sh

# OR manually:
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Key

The OpenAI API key is already configured in your `.env` file. Verify it exists:

```bash
cat .env
```

You should see:
```
OPENAI_API_KEY=your_api_key_here
```

### Step 3: Run the Application

```bash
# Make sure you're in the project directory and virtual environment is activated
source venv/bin/activate  # If not already activated

# Run the Flask app
python app.py

# OR
flask run --port=5016
```

Then open your browser to: **http://127.0.0.1:5016**

---

## Testing the Application

A sample dataset (`sample_data.csv`) is included in the project. Use it to test the application:

1. Open http://127.0.0.1:5016 in your browser
2. Click "Choose File" and select `sample_data.csv`
3. Select your preferred format (PDF or DOCX)
4. Click "Generate Report"
5. Wait for processing (may take 30-60 seconds)
6. Download your generated report!

---

## Project Structure

```
TK Reports/
├── app.py                  # Main Flask application
├── config.yaml             # Configuration settings
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API keys)
├── setup.sh               # Setup script
├── sample_data.csv        # Sample dataset for testing
├── Readme.md              # Full documentation
├── QUICKSTART.md          # This file
│
├── templates/             # HTML templates
│   ├── index.html         # Upload page
│   └── result.html        # Results page
│
├── static/                # Static assets
│   ├── css/
│   │   └── style.css      # Custom styles
│   └── js/
│       └── script.js      # JavaScript
│
├── utils/                 # Core modules
│   ├── __init__.py
│   ├── data_processor.py  # Data analysis
│   ├── ai_engine.py       # OpenAI integration
│   └── report_generator.py # PDF/DOCX generation
│
├── uploads/               # Uploaded files (temporary)
└── outputs/               # Generated reports
    └── charts/            # Generated charts
```

---

## Common Commands

### Activate Virtual Environment
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Deactivate Virtual Environment
```bash
deactivate
```

### Run the Application
```bash
python app.py
# or
flask run --port=5016
```

### Install New Dependencies
```bash
pip install package-name
pip freeze > requirements.txt  # Update requirements.txt
```

### Check Application Health
```bash
curl http://127.0.0.1:5016/health
```

---

## Troubleshooting

### Port Already in Use
If port 5016 is in use, try a different port:
```bash
flask run --port=5017
```

### Import Errors
Make sure the virtual environment is activated and all dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### OpenAI API Errors
- Verify your API key in `.env`
- Check your OpenAI account has credits
- Ensure you're using a valid model (gpt-4-turbo)

### File Upload Issues
- Check file size (max 16MB)
- Ensure file format is CSV or Excel (.xlsx, .xls)
- Verify `uploads/` directory exists and is writable

---

## Next Steps

1. ✅ Test with sample data
2. Upload your own datasets
3. Customize `config.yaml` for your needs
4. Modify templates for branding
5. Deploy to production (see README.md)

---

## Support

For issues or questions:
- Email: talk2efeprogress@gmail.com
- GitHub: github.com/EfeObus

---

**Happy Reporting! 🎉**
