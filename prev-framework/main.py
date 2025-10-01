"""
Main entry point for the Prev example application.

Run with: uvicorn main:app --reload
"""

from prev import Prev

# Create the application - it will automatically discover routes in the app/ directory
app = Prev(debug=True)

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
