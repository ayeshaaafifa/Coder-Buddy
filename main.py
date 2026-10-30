import sys
from graph import app

def main():
    # prompt default set kar diya hai agar aap argument na dein
    query = "Create a modern, responsive calculator web application using HTML, CSS, and plain JavaScript."
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        
    print(f"Starting application generation for: '{query}'")
    
    initial_state = {"query": query}
    app.invoke(initial_state, {"recursion_limit": 50})
    
    print("\n[SUCCESS] Project generation complete! Check the 'generated_project' folder.")

if __name__ == "__main__":
    main()
