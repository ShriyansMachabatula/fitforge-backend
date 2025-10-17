# Environment Variable Setup Commands

Complete reference for setting environment variables across different platforms.

## .env.example File Content

```bash
# ===========================================
# FitForge Backend Environment Configuration
# ===========================================

# Database Configuration
DATABASE_URL=postgresql://admin:admin@127.0.0.1:5432/fitforge

# Application Settings
DEBUG=false
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development

# Security
SECRET_KEY=changeme-generate-a-secure-secret-key-for-production

# JWT Settings (for future authentication)
JWT_SECRET_KEY=changeme-jwt-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8080

# Logging
LOG_LEVEL=INFO
```

---

## Setup Instructions

### 1. Create .env file from example

**Mac/Linux:**
```bash
cp .env.example .env
```

**Windows PowerShell:**
```powershell
Copy-Item .env.example .env
```

**Windows CMD:**
```cmd
copy .env.example .env
```

### 2. Generate Secure Secret Key

**All Platforms (using Python):**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and replace `SECRET_KEY` value in `.env`.

---

## Running Server with Environment Variables

### Method 1: Using .env file (Recommended) ✅

The application automatically loads `.env` via `python-dotenv`.

**Mac/Linux/Windows:**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Or using run.py:**
```bash
python run.py
```

---

### Method 2: Inline Environment Variables

**Mac/Linux (Bash/Zsh):**
```bash
# Single line with backslashes
DATABASE_URL="postgresql://admin:admin@127.0.0.1:5432/fitforge" \
SECRET_KEY="your-secret-key-here" \
DEBUG=true \
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or all on one line
DATABASE_URL="postgresql://admin:admin@127.0.0.1:5432/fitforge" SECRET_KEY="your-secret-key" python -m uvicorn app.main:app --reload
```

**Windows PowerShell:**
```powershell
# Set each variable separately
$env:DATABASE_URL="postgresql://admin:admin@127.0.0.1:5432/fitforge"
$env:SECRET_KEY="your-secret-key-here"
$env:DEBUG="true"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or chain with semicolons (single line)
$env:DATABASE_URL="postgresql://admin:admin@127.0.0.1:5432/fitforge"; $env:SECRET_KEY="your-secret-key"; python -m uvicorn app.main:app --reload
```

**Windows CMD:**
```cmd
set DATABASE_URL=postgresql://admin:admin@127.0.0.1:5432/fitforge
set SECRET_KEY=your-secret-key-here
set DEBUG=true
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### Method 3: Export Variables (Session-wide)

**Mac/Linux (Bash/Zsh):**
```bash
# Export variables (available for entire terminal session)
export DATABASE_URL="postgresql://admin:admin@127.0.0.1:5432/fitforge"
export SECRET_KEY="your-secret-key-here"
export DEBUG="true"
export HOST="0.0.0.0"
export PORT="8000"

# Then run the server
python -m uvicorn app.main:app --reload
```

**Windows PowerShell:**
```powershell
# Set session-wide variables
$env:DATABASE_URL="postgresql://admin:admin@127.0.0.1:5432/fitforge"
$env:SECRET_KEY="your-secret-key-here"
$env:DEBUG="true"
$env:HOST="0.0.0.0"
$env:PORT="8000"

# Then run the server
python -m uvicorn app.main:app --reload
```

**Windows CMD:**
```cmd
set DATABASE_URL=postgresql://admin:admin@127.0.0.1:5432/fitforge
set SECRET_KEY=your-secret-key-here
set DEBUG=true
set HOST=0.0.0.0
set PORT=8000
python -m uvicorn app.main:app --reload
```

---

### Method 4: Using .env file in specific location

If your `.env` is in a different location:

**Mac/Linux:**
```bash
export DOTENV_PATH="/path/to/your/.env"
python -m uvicorn app.main:app --reload
```

**Windows PowerShell:**
```powershell
$env:DOTENV_PATH="C:\path\to\your\.env"
python -m uvicorn app.main:app --reload
```

---

## Production Deployment

### Using systemd (Linux)

Create `/etc/systemd/system/fitforge.service`:

```ini
[Unit]
Description=FitForge Backend API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/fitforge-backend
Environment="DATABASE_URL=postgresql://admin:admin@127.0.0.1:5432/fitforge"
Environment="SECRET_KEY=your-production-secret-key"
Environment="DEBUG=false"
Environment="ENVIRONMENT=production"
ExecStart=/opt/fitforge-backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable fitforge
sudo systemctl start fitforge
```

---

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DATABASE_URL=${DATABASE_URL}
ENV SECRET_KEY=${SECRET_KEY}

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t fitforge-backend .
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://admin:admin@postgres:5432/fitforge" \
  -e SECRET_KEY="your-secret-key" \
  fitforge-backend
```

---

## Verification Commands

### Check environment variables are loaded:

**Mac/Linux:**
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('DATABASE_URL:', os.getenv('DATABASE_URL')); print('SECRET_KEY:', os.getenv('SECRET_KEY'))"
```

**Windows PowerShell:**
```powershell
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('DATABASE_URL:', os.getenv('DATABASE_URL')); print('SECRET_KEY:', os.getenv('SECRET_KEY'))"
```

### Test server is running:
```bash
curl http://localhost:8000/api/health
```

### View all environment variables:

**Mac/Linux:**
```bash
env | grep -E "DATABASE_URL|SECRET_KEY|DEBUG"
```

**Windows PowerShell:**
```powershell
Get-ChildItem Env: | Where-Object { $_.Name -match "DATABASE_URL|SECRET_KEY|DEBUG" }
```

**Windows CMD:**
```cmd
set | findstr "DATABASE_URL SECRET_KEY DEBUG"
```

---

## Troubleshooting

### Issue: "DATABASE_URL environment variable is not set"

**Solution 1:** Make sure `.env` file exists
```bash
ls -la .env  # Mac/Linux
dir .env     # Windows
```

**Solution 2:** Check .env file content
```bash
cat .env     # Mac/Linux
type .env    # Windows
```

**Solution 3:** Manually set the variable
```bash
export DATABASE_URL="postgresql://admin:admin@127.0.0.1:5432/fitforge"  # Mac/Linux
$env:DATABASE_URL="postgresql://admin:admin@127.0.0.1:5432/fitforge"   # PowerShell
```

### Issue: Variables not persisting between sessions

**Mac/Linux:** Add to `~/.bashrc` or `~/.zshrc`:
```bash
echo 'export DATABASE_URL="postgresql://admin:admin@127.0.0.1:5432/fitforge"' >> ~/.bashrc
source ~/.bashrc
```

**Windows PowerShell:** Add to PowerShell profile:
```powershell
Add-Content $PROFILE '$env:DATABASE_URL="postgresql://admin:admin@127.0.0.1:5432/fitforge"'
. $PROFILE
```

---

## Security Best Practices

1. **Never commit .env to git** - It's already in `.gitignore`
2. **Use strong secret keys** - Generate with `secrets.token_urlsafe(32)`
3. **Different keys for each environment** - dev, staging, production
4. **Rotate keys periodically** - Especially after team member changes
5. **Use environment-specific .env files** - `.env.development`, `.env.production`
6. **Store production secrets securely** - Use AWS Secrets Manager, Azure Key Vault, etc.

---

**Last Updated**: 2025-10-17
**Tested On**: macOS, Windows 10/11 (PowerShell), Linux (Ubuntu)
