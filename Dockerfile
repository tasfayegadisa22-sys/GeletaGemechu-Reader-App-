# 1. መሰረታዊ የፓይዘን ኮምፒውተር ማምጣት
FROM python:3.10-slim

# 2. እንደ አስተዳዳሪ ሆነን የፎቶ ማንበቢያውን (Tesseract) እና ቋንቋዎቹን መጫን
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-amh \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# 3. የስራ ቦታ መፍጠር
WORKDIR /app

# 4. አስፈላጊ የፓይዘን ላይብረሪዎችን መጫን
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. የኛን ኮዶች በሙሉ ወደ ሰርቨሩ ማስገባት
COPY . .

# 6. መተግበሪያውን ማስነሳት
CMD ["python", "main.py"]
