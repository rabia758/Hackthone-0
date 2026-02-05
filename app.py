import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, redirect, url_for
import markdown

app = Flask(__name__)

# Configuration - you can set this via environment variable or default to current directory
VAULT_PATH = Path(os.getenv('VAULT_PATH', './AI_Employee_Vault'))
NEEDS_ACTION_DIR = VAULT_PATH / 'Needs_Action'
PENDING_APPROVAL_DIR = VAULT_PATH / 'Pending_Approval'
APPROVED_DIR = VAULT_PATH / 'Approved'
DONE_DIR = VAULT_PATH / 'Done'
REJECTED_DIR = VAULT_PATH / 'Rejected'
SOCIAL_DRAFT_DIR = VAULT_PATH / 'social' / 'Draft'
LOGS_DIR = VAULT_PATH / 'Logs'

def get_file_counts():
    """Get counts for different directories"""
    counts = {}
    counts['needs_action'] = len(list(NEEDS_ACTION_DIR.glob('*.md'))) if NEEDS_ACTION_DIR.exists() else 0
    counts['pending_approval'] = len(list(PENDING_APPROVAL_DIR.glob('*.md'))) if PENDING_APPROVAL_DIR.exists() else 0
    counts['approved'] = len(list(APPROVED_DIR.glob('*.md'))) if APPROVED_DIR.exists() else 0
    counts['done'] = len(list(DONE_DIR.glob('*.md'))) if DONE_DIR.exists() else 0
    counts['rejected'] = len(list(REJECTED_DIR.glob('*.md'))) if REJECTED_DIR.exists() else 0
    return counts

def get_recent_activity():
    """Get recent activity from all directories"""
    activity = []

    # Look at all directories for recent files
    dirs_to_check = [
        ('Needs Action', NEEDS_ACTION_DIR),
        ('Pending Approval', PENDING_APPROVAL_DIR),
        ('Approved', APPROVED_DIR),
        ('Done', DONE_DIR),
        ('Rejected', REJECTED_DIR)
    ]

    for dir_name, dir_path in dirs_to_check:
        if dir_path.exists():
            for file_path in dir_path.glob('*.md'):
                try:
                    stat = file_path.stat()
                    mod_time = datetime.fromtimestamp(stat.st_mtime)
                    activity.append({
                        'filename': file_path.name,
                        'directory': dir_name,
                        'modified': mod_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'size': stat.st_size
                    })
                except:
                    continue

    # Sort by modification time (most recent first) and return top 20
    activity.sort(key=lambda x: x['modified'], reverse=True)
    return activity[:20]

def get_pending_approval_files():
    """Get all files from pending approval directory"""
    files = []
    if PENDING_APPROVAL_DIR.exists():
        for file_path in PENDING_APPROVAL_DIR.glob('*.md'):
            try:
                stat = file_path.stat()
                mod_time = datetime.fromtimestamp(stat.st_mtime)

                # Determine file type based on content or path
                file_type = 'unknown'
                content = file_path.read_text(encoding='utf-8')

                if 'email' in content.lower():
                    file_type = 'email'
                elif 'whatsapp' in content.lower():
                    file_type = 'whatsapp'
                elif 'social' in content.lower():
                    file_type = 'social'
                elif 'file_drop' in content.lower():
                    file_type = 'file_drop'

                files.append({
                    'filename': file_path.name,
                    'filepath': str(file_path),
                    'modified': mod_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'size': stat.st_size,
                    'type': file_type
                })
            except:
                continue

    return sorted(files, key=lambda x: x['modified'], reverse=True)

def get_needs_action_files():
    """Get all files from needs action directory"""
    files = []
    if NEEDS_ACTION_DIR.exists():
        for file_path in NEEDS_ACTION_DIR.glob('*.md'):
            try:
                stat = file_path.stat()
                mod_time = datetime.fromtimestamp(stat.st_mtime)

                # Determine file type based on content or path
                file_type = 'unknown'
                content = file_path.read_text(encoding='utf-8')

                if 'email' in content.lower():
                    file_type = 'email'
                elif 'whatsapp' in content.lower():
                    file_type = 'whatsapp'
                elif 'social' in content.lower():
                    file_type = 'social'
                elif 'file_drop' in content.lower():
                    file_type = 'file_drop'

                files.append({
                    'filename': file_path.name,
                    'filepath': str(file_path),
                    'modified': mod_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'size': stat.st_size,
                    'type': file_type
                })
            except:
                continue

    return sorted(files, key=lambda x: x['modified'], reverse=True)

def get_social_drafts():
    """Get all files from social draft directory"""
    files = []
    if SOCIAL_DRAFT_DIR.exists():
        for file_path in SOCIAL_DRAFT_DIR.glob('*.md'):
            try:
                stat = file_path.stat()
                mod_time = datetime.fromtimestamp(stat.st_mtime)

                files.append({
                    'filename': file_path.name,
                    'filepath': str(file_path),
                    'modified': mod_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'size': stat.st_size
                })
            except:
                continue

    return sorted(files, key=lambda x: x['modified'], reverse=True)

def get_logs():
    """Get recent log entries"""
    logs = []
    if LOGS_DIR.exists():
        for file_path in LOGS_DIR.glob('*.json'):
            try:
                content = file_path.read_text(encoding='utf-8')
                log_data = json.loads(content)

                # Handle different log formats
                if isinstance(log_data, list):
                    logs.extend(log_data)
                elif isinstance(log_data, dict):
                    logs.append(log_data)

            except:
                continue

    # Sort by timestamp and return last 50
    logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return logs[:50]

@app.route('/')
def dashboard():
    """Dashboard page showing overview"""
    counts = get_file_counts()
    activity = get_recent_activity()

    # Read Dashboard.md if it exists
    dashboard_content = ""
    dashboard_path = VAULT_PATH / 'Dashboard.md'
    if dashboard_path.exists():
        content = dashboard_path.read_text(encoding='utf-8')
        dashboard_content = markdown.markdown(content, extensions=['tables'])

    return render_template('dashboard.html',
                         counts=counts,
                         activity=activity,
                         dashboard_content=dashboard_content)

@app.route('/pending_approval')
def pending_approval():
    """Pending approval page showing files awaiting approval"""
    files = get_pending_approval_files()
    return render_template('pending_approval.html', files=files)

@app.route('/needs_action')
def needs_action():
    """Needs action page showing files requiring attention"""
    files = get_needs_action_files()
    return render_template('needs_action.html', files=files)

@app.route('/social_drafts')
def social_drafts():
    """Social drafts page showing draft content"""
    files = get_social_drafts()
    return render_template('social_drafts.html', files=files)

@app.route('/logs')
def logs():
    """Logs page showing recent activity"""
    logs = get_logs()
    return render_template('logs.html', logs=logs)

@app.route('/view_file/<path:filepath>')
def view_file(filepath):
    """View individual markdown file"""
    try:
        file_path = Path(filepath)
        if not file_path.exists():
            return "File not found", 404

        content = file_path.read_text(encoding='utf-8')
        html_content = markdown.markdown(content, extensions=['tables'])

        return render_template('view_file.html',
                             filename=file_path.name,
                             content=html_content,
                             filepath=str(file_path))
    except Exception as e:
        return f"Error reading file: {str(e)}", 500

@app.route('/approve_file', methods=['POST'])
def approve_file():
    """Approve a file and move it to approved directory"""
    try:
        filepath = request.form.get('filepath')
        if not filepath:
            return jsonify({'success': False, 'error': 'No file path provided'})

        file_path = Path(filepath)
        if not file_path.exists():
            return jsonify({'success': False, 'error': 'File does not exist'})

        # Move file to approved directory
        destination = APPROVED_DIR / file_path.name
        shutil.move(str(file_path), str(destination))

        # Log the action
        log_action('approve', file_path.name, str(file_path.parent), str(APPROVED_DIR))

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/reject_file', methods=['POST'])
def reject_file():
    """Reject a file and move it to rejected directory"""
    try:
        filepath = request.form.get('filepath')
        if not filepath:
            return jsonify({'success': False, 'error': 'No file path provided'})

        file_path = Path(filepath)
        if not file_path.exists():
            return jsonify({'success': False, 'error': 'File does not exist'})

        # Move file to rejected directory
        destination = REJECTED_DIR / file_path.name
        shutil.move(str(file_path), str(destination))

        # Log the action
        log_action('reject', file_path.name, str(file_path.parent), str(REJECTED_DIR))

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/send_for_approval', methods=['POST'])
def send_for_approval():
    """Move social draft to pending approval"""
    try:
        filepath = request.form.get('filepath')
        if not filepath:
            return jsonify({'success': False, 'error': 'No file path provided'})

        file_path = Path(filepath)
        if not file_path.exists():
            return jsonify({'success': False, 'error': 'File does not exist'})

        # Move file to pending approval directory (create social subdirectory if needed)
        social_approval_dir = PENDING_APPROVAL_DIR / 'social'
        social_approval_dir.mkdir(parents=True, exist_ok=True)

        destination = social_approval_dir / file_path.name
        shutil.move(str(file_path), str(destination))

        # Log the action
        log_action('send_for_approval', file_path.name, str(file_path.parent), str(social_approval_dir))

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def log_action(action, filename, source_dir, dest_dir):
    """Log an action to the logs directory"""
    try:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'filename': filename,
            'source_directory': source_dir,
            'destination_directory': dest_dir,
            'user': 'local_user'  # Could be replaced with actual user if needed
        }

        # Create logs directory if it doesn't exist
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        # Write to a log file with today's date
        today_log = LOGS_DIR / f"{datetime.now().strftime('%Y-%m-%d')}_actions.json"

        # Read existing log or create empty list
        if today_log.exists():
            try:
                existing_logs = json.loads(today_log.read_text(encoding='utf-8'))
                if not isinstance(existing_logs, list):
                    existing_logs = []
            except:
                existing_logs = []
        else:
            existing_logs = []

        # Append new log entry
        existing_logs.append(log_entry)

        # Write back to file
        today_log.write_text(json.dumps(existing_logs, indent=2), encoding='utf-8')

    except Exception as e:
        print(f"Error logging action: {str(e)}")

if __name__ == '__main__':
    # Create directories if they don't exist
    for dir_path in [NEEDS_ACTION_DIR, PENDING_APPROVAL_DIR, APPROVED_DIR, DONE_DIR, REJECTED_DIR, SOCIAL_DRAFT_DIR, LOGS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

    app.run(debug=True, host='127.0.0.1', port=5000)