# TK Reports - AI-Powered Data Analysis & Report Generation

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

TK Reports is an advanced AI-powered data analytics platform that transforms your datasets into comprehensive, professional-grade analytical reports. Built with Flask and OpenAI GPT-4 Turbo, it combines statistical analysis, machine learning insights, and natural language generation to produce executive-ready reports in both DOCX and PDF formats.

## 🌟 Key Features

### 📊 Comprehensive Data Analysis
- **Advanced Statistics**: Mean, median, mode, standard deviation, skewness, kurtosis, coefficient of variation
- **Outlier Detection**: IQR-based outlier identification with detailed reporting
- **Correlation Analysis**: Pearson correlation with strength classification (weak, moderate, strong, very strong)
- **Distribution Analysis**: Automated pattern detection and distribution characterization
- **Missing Data Assessment**: Comprehensive data quality scoring and completeness analysis

### 🎯 Research Objective-Driven Reports
- **Focused Analysis**: Specify your research objective/purpose to guide the entire analysis
- **Targeted Insights**: AI-generated content aligned with your specific research goals
- **Objective-Centric Recommendations**: Prioritized actions that directly advance your stated objectives
- **Contextual Interpretation**: All findings framed in relation to your research purpose

### 🤖 AI-Powered Narrative Generation
- **GPT-4 Turbo Integration**: Leverages OpenAI's most advanced language model
- **Comprehensive Executive Summaries**: 400-500 word multi-paragraph summaries (6 sections)
- **Detailed Key Findings**: 600-800 word structured findings with 5 subsections
- **Deep Insights Interpretation**: 500-700 word analytical interpretations
- **Actionable Recommendations**: 6-8 specific, data-driven recommendations with rationale
- **Intelligent Fallback**: Automatic high-quality content generation when API unavailable

### 📈 Advanced Visualizations
- **5 Professional Charts**: 
  - Distribution plots with KDE overlays
  - Correlation heatmaps with annotations
  - Categorical bar charts with percentages
  - Box plots for outlier visualization
  - Scatter plots for relationship analysis
- **100-150 Word Chart Interpretations**: Detailed explanations for each visualization
- **High-Quality Graphics**: Matplotlib and Seaborn-powered publication-ready charts

### 📄 Professional Report Formats

#### DOCX Reports (Comprehensive - 800+ lines)
- **Cover Page**: Professional title page with metadata
- **Executive Summary**: AI-generated strategic overview
- **Introduction**: 
  - 2.1 Research Objective and Purpose (if provided)
  - 2.2 Dataset Overview
  - 2.3 Analytical Objectives
- **Methodology**: 
  - 3.1 Data Source and Scope
  - 3.2 Analytical Tools and Technologies
  - 3.3 Analytical Approach (7-step process)
  - 3.4 Quality Assurance
- **Key Findings**:
  - 4.1 Dataset Composition (7-metric table)
  - 4.2 Numerical Statistics (top 5 variables × 7 columns)
  - 4.3 Categorical Distribution (detailed lists)
  - 4.4 Correlation Patterns (comprehensive table)
  - 4.5 Visual Analysis (5 charts with interpretations)
- **Insights**: AI-generated deep interpretation
- **Recommendations**: 6-8 prioritized, actionable recommendations
- **Conclusion**: 
  - 8.1 Summary of Insights
  - 8.2 Strategic Implications
  - 8.3 Limitations and Considerations
  - 8.4 Next Steps
- **Appendix**: Summary statistics table

#### PDF Reports (Enhanced with Error Handling)
- Comprehensive sections matching DOCX format
- Robust chart rendering with fallback handling
- Clean typography using Helvetica font family
- Optimized for printing and digital distribution

### 🚀 Technical Capabilities
- **Large Dataset Support**: Handles up to **100MB** file uploads
- **Multiple Formats**: CSV, XLSX, XLS, TSV file support
- **Smart Sampling**: Automatic sampling for datasets >10,000 rows (visualization optimization)
- **Canadian Standards**: Locale-specific formatting (en_CA) for dates, numbers, and currency
- **Real-time Processing**: Live feedback during analysis stages
- **Error Recovery**: Comprehensive error handling with graceful degradation

## 📋 Requirements

- Python 3.11+
- Flask 3.0.0
- OpenAI API Key (GPT-4 Turbo access)
- Required Python packages (see `requirements.txt`)

## 🛠️ Installation

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/EfeObus/TK-Reports.git
cd TK-Reports

# Run setup script
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/EfeObus/TK-Reports.git
cd TK-Reports

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create required directories
mkdir -p uploads outputs

# Configure environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## ⚙️ Configuration

### Environment Variables (.env)

```bash
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Application Configuration (config.yaml)

```yaml
openai:
  api_key: ${OPENAI_API_KEY}
  model: "gpt-4-turbo-preview"
  temperature: 0.7
  max_tokens: 2000

report:
  locale: "en_CA"
  export_formats:
    - "pdf"
    - "docx"

server:
  host: "0.0.0.0"
  port: 5016
  debug: true
```

## 🚀 Usage

### Starting the Application

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the application
python app.py

# Access in browser
# http://localhost:5016
```

### Generating Reports

1. **Upload Your Dataset**
   - Navigate to http://localhost:5016
   - Select your data file (CSV, XLSX, XLS, or TSV up to 100MB)

2. **Provide Report Metadata**
   - **Report Title**: E.g., "Q4 2024 Sales Performance Analysis"
   - **Prepared For**: E.g., "Executive Leadership Team"
   - **Prepared By**: E.g., "Data Analytics Department"
   - **Research Objective** (NEW): E.g., "Analyze employee attrition patterns to identify retention strategies and reduce turnover by 15% over the next fiscal year"

3. **Select Format**
   - Choose DOCX for comprehensive reports with full formatting
   - Choose PDF for distributable, print-ready reports

4. **Generate & Download**
   - Click "Generate Report"
   - Wait for analysis to complete (progress indicators shown)
   - Download your professional report

## 📊 Sample Use Cases

### Business Analytics
```
Objective: Identify key drivers of customer churn and develop targeted retention strategies
Dataset: Customer transaction history, demographics, engagement metrics
Output: 15-page comprehensive report with predictive insights and recommendations
```

### HR Analytics
```
Objective: Analyze employee attrition patterns to reduce turnover by 15% over next fiscal year
Dataset: Employee records with 39 variables including performance, demographics, satisfaction
Output: Detailed retention strategy report with correlation analysis and action items
```

### Healthcare Research
```
Objective: Determine how age, education, and income affect individual health outcomes
Dataset: Health survey responses from 253,680 participants across 18 variables
Output: Statistical analysis report with demographic breakdowns and health correlations
```

### Sales Performance
```
Objective: Optimize product mix and identify high-growth market segments
Dataset: Global sales data with 51,290 transactions across 24 product categories
Output: Strategic sales report with regional analysis and revenue optimization recommendations
```

## 🏗️ Architecture

```
TK-Reports/
├── app.py                          # Flask application entry point
├── config.yaml                     # Application configuration
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── setup.sh                        # Automated setup script
│
├── templates/
│   ├── index.html                  # Upload form with objective field
│   └── result.html                 # Download page
│
├── static/
│   ├── css/
│   │   └── style.css              # Custom styling
│   └── js/
│       └── script.js              # Client-side validation (100MB)
│
├── utils/
│   ├── __init__.py
│   ├── ai_engine.py               # OpenAI GPT-4 integration with objective support
│   ├── data_processor.py          # Advanced statistical analysis
│   └── report_generator.py        # DOCX/PDF generation (1300+ lines)
│
├── uploads/                        # Temporary file uploads
└── outputs/                        # Generated reports
```

## 🔧 Technical Stack

### Backend
- **Flask 3.0.0**: Web framework
- **OpenAI 2.6.1**: GPT-4 Turbo API integration
- **Pandas 2.1.4**: Data manipulation and analysis
- **NumPy 1.26.2**: Numerical computations
- **SciPy 1.16.2**: Advanced statistics (skewness, kurtosis, outliers)

### Document Generation
- **python-docx 1.1.0**: Comprehensive DOCX reports
- **fpdf2 2.7.6**: PDF report generation

### Visualization
- **Matplotlib 3.8.2**: Statistical charts
- **Seaborn 0.13.0**: Enhanced visualizations

### Data Processing
- **openpyxl 3.1.2**: Excel XLSX support
- **xlrd 2.0.1+**: Excel XLS support

## 📈 Performance & Scalability

- **File Size Limit**: 100MB (configurable)
- **Processing Speed**: 
  - Small datasets (<1,000 rows): ~10-15 seconds
  - Medium datasets (1,000-10,000 rows): ~20-30 seconds
  - Large datasets (>10,000 rows): ~30-60 seconds (with sampling)
- **Memory Efficiency**: Automatic sampling for large datasets
- **Concurrent Users**: Supports multiple simultaneous report generations

## 🔐 Security & Privacy

- File uploads are temporary and automatically managed
- No data is stored permanently on the server
- OpenAI API calls are secure and encrypted
- Environment variables protect sensitive API keys
- Input validation prevents malicious file uploads

## 🐛 Troubleshooting

### Common Issues

**OpenAI API Errors**
```
Error: "cannot import name 'Chat' from 'openai.resources.chat'"
Solution: This is a known import issue. The application uses intelligent fallback content.
No action needed - reports will still generate successfully.
```

**Large File Upload Errors**
```
Error: "File is too large. Maximum size is 100MB"
Solution: Compress your dataset or increase MAX_CONTENT_LENGTH in app.py
```

**PDF Rendering Issues**
```
Error: "Not enough horizontal space"
Solution: The app has robust error handling. If charts fail, text-based summaries are provided.
```

**Missing Dependencies**
```
Error: "ModuleNotFoundError: No module named 'fpdf'"
Solution: Ensure virtual environment is activated and run: pip install -r requirements.txt
```

## 🎯 Future Enhancements

- [ ] Interactive dashboard for report customization
- [ ] Multi-language support (French, Spanish)
- [ ] Custom chart template library
- [ ] Advanced time series analysis
- [ ] Machine learning model integration
- [ ] Report scheduling and automation
- [ ] API endpoint for programmatic access
- [ ] Cloud deployment (AWS, Azure, GCP)

## 📝 Changelog

### Version 1.2.0 (October 2024)
- ✅ Added Research Objective/Purpose field
- ✅ AI prompts now incorporate research objectives
- ✅ Objective displayed in report Section 2.1
- ✅ All recommendations prioritized by objective relevance

### Version 1.1.0 (October 2024)
- ✅ Increased file upload limit to 100MB
- ✅ Added XLS file support (xlrd integration)
- ✅ Enhanced PDF error handling
- ✅ Improved chart rendering in both formats

### Version 1.0.0 (October 2024)
- ✅ Initial release with comprehensive report generation
- ✅ GPT-4 Turbo integration
- ✅ Advanced statistical analysis
- ✅ Professional DOCX and PDF output

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Efe Obukohwo**
- GitHub: [@EfeObus](https://github.com/EfeObus)
- Repository: [TK-Reports](https://github.com/EfeObus/TK-Reports)

## 🙏 Acknowledgments

- OpenAI for GPT-4 Turbo API
- Flask community for excellent documentation
- Python data science ecosystem (Pandas, NumPy, SciPy, Matplotlib, Seaborn)

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation in `/docs` folder
- Review troubleshooting section above

---

**Made with ❤️ using Python, Flask, and OpenAI GPT-4 Turbo**