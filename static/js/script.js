// TK Reports JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // File upload validation
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');
    
    if (fileInput && uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            const file = fileInput.files[0];
            
            if (!file) {
                e.preventDefault();
                alert('Please select a file to upload.');
                return false;
            }
            
            // Check file size (100MB limit)
            const maxSize = 100 * 1024 * 1024; // 100MB in bytes
            if (file.size > maxSize) {
                e.preventDefault();
                alert('File size exceeds 100MB limit. Please select a smaller file.');
                return false;
            }
            
            // Check file extension
            const allowedExtensions = ['csv', 'xlsx', 'xls', 'tsv'];
            const fileName = file.name.toLowerCase();
            const fileExtension = fileName.split('.').pop();
            
            if (!allowedExtensions.includes(fileExtension)) {
                e.preventDefault();
                alert('Invalid file type. Please upload a CSV or Excel file.');
                return false;
            }
            
            // Show loading indicator
            showLoadingIndicator();
        });
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

function showLoadingIndicator() {
    // Create loading overlay
    const overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    `;
    
    overlay.innerHTML = `
        <div class="text-center text-white">
            <div class="spinner-border mb-3" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <h4>Processing your dataset...</h4>
            <p>This may take a few moments. Please wait.</p>
        </div>
    `;
    
    document.body.appendChild(overlay);
}

// File size formatter
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Display selected file info
const fileInputElement = document.getElementById('fileInput');
if (fileInputElement) {
    fileInputElement.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            console.log('Selected file:', file.name);
            console.log('File size:', formatFileSize(file.size));
            console.log('File type:', file.type);
        }
    });
}
