## Installation and Run

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
uvicorn main:app --reload
```

The API will be available at:

http://127.0.0.1:8000

## Example curl Output

```text
HTTP/1.1 200 OK
date: Sun, 13 Sep 2026 13:20:05 GMT
server: uvicorn
content-length: 15
content-type: application/json
```