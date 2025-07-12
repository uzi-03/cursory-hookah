#!/usr/bin/env python3
"""
Setup script for Cursory Hookah - Gear Compatibility & Discovery
"""

import os
import subprocess
import sys

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, check=True, cwd=cwd, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def setup_backend():
    """Setup the Flask backend"""
    print("Setting up Flask backend...")
    
    # Check if Python is available
    success, output = run_command("python --version")
    if not success:
        print("❌ Python not found. Please install Python 3.7+")
        return False
    
    # Install Python dependencies
    print("Installing Python dependencies...")
    success, output = run_command("pip install -r backend/requirements.txt")
    if not success:
        print(f"❌ Failed to install Python dependencies: {output}")
        return False
    
    print("✅ Backend setup complete!")
    return True

def setup_frontend():
    """Setup the React frontend"""
    print("Setting up React frontend...")
    
    # Check if Node.js is available
    success, output = run_command("node --version")
    if not success:
        print("❌ Node.js not found. Please install Node.js 14+")
        return False
    
    # Check if npm is available
    success, output = run_command("npm --version")
    if not success:
        print("❌ npm not found. Please install npm")
        return False
    
    # Install Node.js dependencies
    print("Installing Node.js dependencies...")
    success, output = run_command("npm install", cwd="frontend")
    if not success:
        print(f"❌ Failed to install Node.js dependencies: {output}")
        return False
    
    print("✅ Frontend setup complete!")
    return True

def main():
    """Main setup function"""
    print("🚬 Setting up Cursory Hookah - Gear Compatibility & Discovery")
    print("=" * 60)
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed!")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("❌ Frontend setup failed!")
        sys.exit(1)
    
    print("\n🎉 Setup complete!")
    print("\nTo run the application:")
    print("1. Start the backend: cd backend && python run.py")
    print("2. Start the frontend: cd frontend && npm start")
    print("3. Open http://localhost:3000 in your browser")
    print("\nThe backend will be available at http://localhost:5000")

if __name__ == "__main__":
    main() 