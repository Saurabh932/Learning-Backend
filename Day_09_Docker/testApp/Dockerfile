# 1. Base image
FROM python:3.11-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy only requirements first
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy rest of the application
COPY . .

# 6. Expose the port Flask runs on
EXPOSE 3000

# 7. Defauld command
CMD ["python", "app.py"]