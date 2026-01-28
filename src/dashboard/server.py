import os
import re
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# --- Configuration ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # J-OS Root
LOG_DIR = os.path.join(PROJECT_ROOT, "log")

# --- Setup Static & Templates ---
current_dir = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

vendor_dir = os.path.join(PROJECT_ROOT, "src", "vendor")
if os.path.exists(vendor_dir):
     app.mount("/vendor", StaticFiles(directory=vendor_dir), name="vendor")

templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

# --- Models ---
class SaveRequest(BaseModel):
    path: str
    content: str

class CompleteRequest(BaseModel):
    path: str
    line_text: str

class AppendRequest(BaseModel):
    path: str
    type: str # TASK, IDEA, BUG, NOTE
    description: str

# ... Helper Functions ...

# ...

@app.post("/api/append")
async def append_task(req: AppendRequest):
    full_path = os.path.join(LOG_DIR, req.path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(LOG_DIR)):
         raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        # Generate ID: Simple hex timestamp (last 3 chars) to be short & unique-ish for this context
        import time
        task_id = hex(int(time.time()))[-3:] 
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Format: - (id) [Date] **[TYPE]** Description
        new_line = f"\n- ({task_id}) [{today}] **[{req.type.upper()}]** {req.description}"
        
        with open(full_path, "a", encoding="utf-8") as f:
            f.write(new_line)
            
        return {"status": "success", "message": "Task appended", "id": task_id}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Helper Functions ---
def get_log_files():
    files = []
    for root, dirs, filenames in os.walk(LOG_DIR):
        if "archive" in dirs: dirs.remove("archive")
        if "reports" in dirs: dirs.remove("reports")
        if "Brain" in dirs: dirs.remove("Brain")
        if ".git" in dirs: dirs.remove(".git")
        
        for filename in filenames:
            # Filter: Must be .md, not AI_rules, and either contain '_log', be 'inbox.md', or be in a 'meetings' folder
            if filename.endswith(".md") and not filename.startswith("AI_rules"):
                is_log = "_log" in filename.lower() or filename.lower() == "inbox.md"
                is_meeting = "meetings" in os.path.basename(root).lower()
                
                if is_log or is_meeting:
                    full_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(full_path, LOG_DIR)
                    
                    # Sort Logic: Inbox last (We can handle generic naming here)
                    files.append({
                        "name": filename,
                        "rel_path": rel_path,
                        "full_path": full_path,
                        "category": os.path.basename(root) if root != LOG_DIR else "Root"
                    })
    
    # Sort files: "inbox.md" at the end, others alphabetical
    files.sort(key=lambda x: (x['name'].lower() == 'inbox.md', x['name']))
    return files

def parse_tasks(content):
    """
    Extracts structured tasks from markdown content.
    Regex for: - (ID) [Date] **[Type]** Description
    """
    tasks = []
    # Regex: 
    # ^\s*-\s+      : Start with dash and spaces
    # \((.*?)\)     : Capture Group 1: ID (e.g. w52)
    # \s+\[(.*?)\]  : Capture Group 2: Date
    # \s+\*\*\[(.*?)\]\*\* : Capture Group 3: Type (e.g. TASK)
    # \s+(.*)$      : Capture Group 4: Description
    
    pattern = re.compile(r'^\s*-\s+\((.*?)\)\s+\[(.*?)\]\s+\*\*\[(.*?)\]\*\*\s+(.*)$', re.MULTILINE)
    
    for match in pattern.finditer(content):
        # Check if already completed (strikethrough)
        desc = match.group(4)
        if "~~" in desc and "✅" in desc:
            continue # Skip completed
            
        tasks.append({
            "id": match.group(1),
            "date": match.group(2),
            "type": match.group(3),
            "description": desc,
            "raw_line": match.group(0).strip(),
            "line_index": content[:match.start()].count('\n')
        })
    return tasks

def read_file_content(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

# --- Routes ---
@app.get("/")
async def read_items(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/logs")
async def get_logs_api():
    logs = get_log_files()
    data = []
    
    for log in logs:
        content = read_file_content(log['full_path'])
        
        # Parse Tasks
        parsed_tasks = parse_tasks(content)
        
        data.append({
            "name": log['name'],
            "category": log['category'],
            "path": log['rel_path'],
            "content": content,
            "tasks": parsed_tasks,
            "id": log['rel_path'].replace("\\", "_").replace("/", "_").replace(".", "_")
        })
        
    return JSONResponse(content=data)

@app.post("/api/save")
async def save_file(req: SaveRequest):
    full_path = os.path.join(LOG_DIR, req.path)
    # Security check: ensure parsing stays within LOG_DIR
    if not os.path.abspath(full_path).startswith(os.path.abspath(LOG_DIR)):
         raise HTTPException(status_code=403, detail="Access denied")
         
    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(req.content)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/config")
async def get_config():
    tags = ["TASK", "IDEA", "BUG", "NOTE"] # Fallback
    
    rules_path = os.path.join(LOG_DIR, "AI_rules.md")
    if os.path.exists(rules_path):
        try:
            with open(rules_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Parse "PERMITTED TAGS" section
                # Look for "* `[TAG]`"
                # Regex: \* `\[(.*?)\]`
                matches = re.findall(r'\* `\[(.*?)\]`', content)
                if matches:
                    tags = matches
        except Exception as e:
            print(f"Error reading AI_rules: {e}")
            
    return JSONResponse(content={"tags": tags})

@app.post("/api/append")
async def append_task(req: AppendRequest):
    # Ensure path uses correct separators for OS
    safe_rel_path = req.path.replace('/', os.sep).replace('\\', os.sep)
    full_path = os.path.join(LOG_DIR, safe_rel_path)
    
    # Security Check
    if not os.path.abspath(full_path).startswith(os.path.abspath(LOG_DIR)):
         print(f"Access Denied: Is {full_path} inside {LOG_DIR}?")
         raise HTTPException(status_code=403, detail="Access denied")
    
    if not os.path.exists(full_path):
        print(f"File Not Found: {full_path}")
        raise HTTPException(status_code=404, detail=f"File not found: {safe_rel_path}")

    try:
        # Generate ID: Simple hex timestamp (last 3 chars)
        import time
        task_id = hex(int(time.time()))[-3:] 
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Format
        # Ensure newline prefix in case file doesn't end with one
        new_line = f"\n- ({task_id}) [{today}] **[{req.type.upper()}]** {req.description}"
        
        with open(full_path, "a", encoding="utf-8") as f:
            f.write(new_line)
            
        return {"status": "success", "message": "Task appended", "id": task_id}
            
    except Exception as e:
        print(f"Append Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/complete")
async def complete_task(req: CompleteRequest):
    full_path = os.path.join(LOG_DIR, req.path)
    if not os.path.abspath(full_path).startswith(os.path.abspath(LOG_DIR)):
         raise HTTPException(status_code=403, detail="Access denied")
         
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        found = False
        new_lines = []
        today = datetime.now().strftime("%Y-%m-%d")
        
        target_stripped = req.line_text.strip()
        
        for line in lines:
            if line.strip() == target_stripped:
                # Transform logic
                # Original: - (ID) [Date] **[Type]** Description
                # Target:   - (ID) [Date] **[Type]** ✅ **[DONE]** ~~Description~~ (Completed: YYYY-MM-DD)
                
                # We need to split the line to insert the done marker and strikethrough.
                # We can reuse the regex or simple string splitting.
                # Regex is safer to preserve parts.
                pattern = re.compile(r'^(\s*-\s+\(.*?\)\s+\[.*?\]\s+\*\*\[.*?\]\*\*)\s+(.*)$')
                match = pattern.match(line)
                
                if match:
                    prefix = match.group(1) # "- (ID) [Date] **[Type]**"
                    desc = match.group(2).strip() # "Description"
                    
                    new_line = f"{prefix} ✅ **[DONE]** ~~{desc}~~ (Completed: {today})\n"
                    new_lines.append(new_line)
                    found = True
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
                
        if found:
            with open(full_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            return {"status": "success", "message": "Task completed"}
        else:
            raise HTTPException(status_code=404, detail="Line not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print(f"J-OS Server running on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
