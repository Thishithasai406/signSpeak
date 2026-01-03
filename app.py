from flask import Flask, render_template, jsonify
import subprocess
import sys
import os

# Try to import psutil for better process checking
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

app = Flask(__name__)

# Global variable to track if prediction.py is running
prediction_process = None

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/launch-prediction', methods=['POST'])
def launch_prediction():
    """Launch prediction.py as a separate process - optimized for speed"""
    global prediction_process
    
    try:
        # Get the path to prediction.py
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction.py')
        
        # Launch prediction.py immediately - ensure working directory is correct
        project_dir = os.path.dirname(os.path.abspath(__file__))
        
        if sys.platform == 'win32':
            # Use pythonw.exe to hide console window - only show GUI
            python_exe = sys.executable
            pythonw_exe = python_exe.replace('python.exe', 'pythonw.exe')
            if not os.path.exists(pythonw_exe):
                pythonw_exe = python_exe
            
            # Launch without console window and track the process
            # Log errors to a file for debugging
            log_file = os.path.join(project_dir, 'prediction_errors.log')
            try:
                with open(log_file, 'w') as log:
                    log.write(f"Starting prediction.py at {os.path.basename(script_path)}\n")
                    log.write(f"Working directory: {project_dir}\n")
                    log.write(f"Model file exists: {os.path.exists(os.path.join(project_dir, 'cnn8grps_rad1_model.h5'))}\n")
            except:
                pass
            
            # Open log file in append mode for stdout/stderr
            log_stdout = open(log_file, 'a')
            log_stderr = open(log_file, 'a')
            
            prediction_process = subprocess.Popen(
                [pythonw_exe, script_path],
                cwd=project_dir,
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP,
                stdout=log_stdout,
                stderr=log_stderr,
                stdin=subprocess.DEVNULL,
                start_new_session=True
            )
        else:
            # On Linux/Mac
            subprocess.Popen(
                [sys.executable, script_path],
                cwd=project_dir,  # Set working directory to project folder
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True
            )
        
        # Return immediately without checking status
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500

@app.route('/check-prediction', methods=['GET'])
def check_prediction():
    """Check if prediction.py is still running"""
    global prediction_process
    
    # Check if any python/pythonw process is running prediction.py
    if HAS_PSUTIL:
        try:
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction.py')
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = proc.info.get('cmdline', [])
                    if cmdline and any('prediction.py' in str(arg) for arg in cmdline):
                        # Check if process is still alive
                        if proc.is_running():
                            return jsonify({"running": True}), 200
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception:
            pass
    
    # Fallback: check our tracked process
    if prediction_process is not None:
        try:
            if prediction_process.poll() is None:
                return jsonify({"running": True}), 200
        except:
            pass
    
    return jsonify({"running": False}), 200

if __name__ == '__main__':
    # Run Flask app on localhost
    app.run(host='127.0.0.1', port=5000, debug=True)

