import os
import yaml
import traceback
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from utils.data_processor import DataProcessor
from utils.ai_engine import AIEngine
from utils.report_generator import ReportGenerator

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'tk-reports-secret-key-2024')

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'tsv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load config.yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Landing page with file upload form"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and process dataset"""
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload CSV or Excel files only.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Get report metadata
        report_format = request.form.get('format', 'pdf')
        report_title = request.form.get('report_title', 'Data Insight Report')
        prepared_for = request.form.get('prepared_for', '')
        prepared_by = request.form.get('prepared_by', 'TK Reports')
        objective = request.form.get('objective', '')
        
        # Process the dataset
        flash('File uploaded successfully. Processing dataset...', 'info')
        return redirect(url_for('generate_report', 
                                filename=unique_filename, 
                                format=report_format,
                                title=report_title,
                                prepared_for=prepared_for,
                                prepared_by=prepared_by,
                                objective=objective))
    
    except Exception as e:
        flash(f'Error uploading file: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/generate/<filename>')
def generate_report(filename):
    """Generate the insight report"""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        report_format = request.args.get('format', 'pdf')
        report_title = request.args.get('title', 'Data Insight Report')
        prepared_for = request.args.get('prepared_for', '')
        prepared_by = request.args.get('prepared_by', 'TK Reports')
        objective = request.args.get('objective', '')
        
        # Create metadata dictionary
        report_metadata = {
            'title': report_title,
            'prepared_for': prepared_for,
            'prepared_by': prepared_by,
            'objective': objective,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'locale': config['report']['locale']
        }
        
        # Step 1: Process and analyze data
        flash('Analyzing dataset...', 'info')
        processor = DataProcessor(filepath)
        data_summary = processor.analyze()
        
        # Add objective to data summary for AI context
        data_summary['objective'] = objective
        
        # Step 2: Generate AI narrative
        flash('Generating AI insights...', 'info')
        ai_engine = AIEngine(config['openai'])
        narrative = ai_engine.generate_insights(data_summary)
        
        # Step 3: Generate charts
        flash('Creating visualizations...', 'info')
        charts = processor.generate_charts()
        
        # Step 4: Build the report
        flash('Building report...', 'info')
        report_gen = ReportGenerator(config['report'])
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if report_format == 'docx' or 'docx' in config['report']['export_formats']:
            docx_path = os.path.join(
                app.config['OUTPUT_FOLDER'],
                f"tk_report_{timestamp}.docx"
            )
            report_gen.create_docx_report(
                filepath=docx_path,
                data_summary=data_summary,
                narrative=narrative,
                charts=charts,
                metadata=report_metadata
            )
        
        if report_format == 'pdf' or 'pdf' in config['report']['export_formats']:
            pdf_path = os.path.join(
                app.config['OUTPUT_FOLDER'],
                f"tk_report_{timestamp}.pdf"
            )
            report_gen.create_pdf_report(
                filepath=pdf_path,
                data_summary=data_summary,
                narrative=narrative,
                charts=charts,
                metadata=report_metadata
            )
        
        # Return result page with download link
        result_file = f"tk_report_{timestamp}.{report_format}"
        flash('Report generated successfully!', 'success')
        return render_template(
            'result.html',
            filename=result_file,
            format=report_format,
            summary=data_summary,
            narrative=narrative
        )
    
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error generating report: {str(e)}")
        print(error_trace)
        flash(f'Error generating report: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/download/<filename>')
def download_file(filename):
    """Download generated report"""
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    flash('File is too large. Maximum size is 100MB.', 'error')
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    flash('An internal error occurred. Please try again.', 'error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5016)
