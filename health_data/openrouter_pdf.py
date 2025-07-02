

    except Exception as e:
        print(f'is_pdf_searchable error: {e}')
        return False



# Utility: Extract text from searchable PDF
def extract_text_from_pdf(pdf):
    # Read PDF bytes
    if isinstance(pdf, str):
        if not os.path.isfile(pdf):
            print(f'extract_text_from_pdf error: file path does not exist: {pdf}')
            return ''
        with open(pdf, 'rb') as f:
            pdf_bytes = f.read()
    elif hasattr(pdf, 'read'):
        pdf.seek(0)
        pdf_bytes = pdf.read()
        pdf.seek(0)
    else:
        print(f'extract_text_from_pdf error: unsupported input type {type(pdf)}')
        return ''

    # --- Try PyPDF2 ---
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        if not reader.pages:
            print('extract_text_from_pdf error: PDF has no pages (PyPDF2)')
        else:
            text = "\n".join([page.extract_text() or '' for page in reader.pages])
            if text.strip():
                print('extract_text_from_pdf: extracted text using PyPDF2')
                return text
    except Exception as e:
        print(f'extract_text_from_pdf warning: PyPDF2 failed with {e}')

    # --- Fallback to PyMuPDF (fitz) ---
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "\n".join([page.get_text() or '' for page in doc])
        if text.strip():
            print('extract_text_from_pdf: extracted text using PyMuPDF')
            return text
    except Exception as e:
        print(f'extract_text_from_pdf fallback error (PyMuPDF): {e}')

    print('extract_text_from_pdf: no extractable text found in PDF')
    return ''

# Utility: PDF to base64 images (for vision model)
def pdf_to_base64_images(pdf):
    if isinstance(pdf, str):
        if not os.path.isfile(pdf):
            print(f'pdf_to_base64_images error: file path does not exist: {pdf}')
            return []
        doc = fitz.open(pdf)
    elif hasattr(pdf, 'read'):
        pdf.seek(0)
        pdf_bytes = pdf.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        pdf.seek(0)
    else:
        print(f'pdf_to_base64_images error: unsupported input type {type(pdf)}')
        return []
    images = []
    for page in doc:
        pix = page.get_pixmap()
        img_bytes = pix.tobytes("png")
        b64 = base64.b64encode(img_bytes).decode()
        images.append(f"data:image/png;base64,{b64}")
    return images

# DeepSeek R1 text LLM extraction
def extract_health_data_from_text(text):
    OPENROUTER_KEY = getattr(settings, 'OPENROUTER_KEY', None)
    if not OPENROUTER_KEY:
        raise Exception('OpenRouter API key not configured.')
    # Normalize line endings to match frontend count
    text = text.replace('\r\n', '\n')
    # Truncate text to avoid exceeding LLM context window
    max_chars = 8000
    truncation_warning = None
    if len(text) > max_chars:
        truncation_warning = f"Warning: Only the first {max_chars} characters of your PDF were sent for extraction. If you need more, please split your PDF and upload in parts."
        print(f'LLM input truncated from {len(text)} to {max_chars} characters.')
        text = text[:max_chars]
    prompt = (
        "Extract all health exam results from the following text. "
        "For each result, return a JSON array of objects with: "
        "test_date (YYYY-MM-DD), test_name, result_value, unit, reference_range_min, reference_range_max, flagged (true/false), note. "
        "If a value is missing, use null. Respond with only a valid JSON array, no explanation, no markdown, no extra text. "
        "Do not include any text before or after the JSON array.\n\n" + text
    )
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_KEY}"}
    data = {
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [
            {"role": "system", "content": prompt}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
    print('DeepSeek R1 raw response:', content)
    # Clean up hallucinated non-ASCII property names (e.g., "极细朊name")
    import re, json
    def clean_json_string(s):
        # Remove lines with non-ASCII property names
        lines = s.splitlines()
        cleaned = []
        for line in lines:
            if re.match(r'\s*"[a-zA-Z0-9_ ]+"\s*:', line) or line.strip().startswith('{') or line.strip().startswith('}') or line.strip().startswith('[') or line.strip().startswith(']') or line.strip().endswith(',') or line.strip() == '':
                cleaned.append(line)
        s = '\n'.join(cleaned)
        # Remove trailing commas before ] or }
        s = re.sub(r',\s*([\]\}])', r'\1', s)
        return s
    # Try to extract JSON array
    match = re.search(r'\[.*?\]', content, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str), truncation_warning
        except Exception:
            # Try cleaning and parsing again
            cleaned = clean_json_string(json_str)
            try:
                return json.loads(cleaned), truncation_warning
            except Exception as e:
                print('JSON parse error after cleaning:', e)
                # --- Robust fallback: parse objects one by one ---
                objs = []
                errors = 0
                skipped = []
                for obj_match in re.finditer(r'\{.*?\}', cleaned, re.DOTALL):
                    obj_str = obj_match.group(0)
                    try:
                        obj = json.loads(obj_str)
                        # Only accept if it has at least test_name and result_value
                        if 'test_name' in obj and 'result_value' in obj:
                            objs.append(obj)
                        else:
                            skipped.append(obj_str)
                    except Exception:
                        errors += 1
                        skipped.append(obj_str)
                        continue
                if objs:
                    warn = truncation_warning or ''
                    if errors or skipped:
                        warn = (warn or '') + f" Warning: {errors} result(s) were skipped due to formatting errors. Skipped: "
                        warn += '\n'.join(skipped[:3])
                        if len(skipped) > 3:
                            warn += f"\n...and {len(skipped)-3} more."
                    return objs, warn or None
                raise Exception(f'LLM returned invalid JSON. Error: {e}\nRaw output (truncated):\n{content[:1000]}...')
    raise Exception('Could not extract health data from DeepSeek R1 response. Raw output (truncated):\n' + content[:1000] + '...')

# Utility: Extract text from non-searchable PDF using EasyOCR
# Returns extracted text as a single string

def extract_text_from_pdf_with_easyocr(pdf):
    # Convert PDF pages to images (using PyMuPDF)
    if isinstance(pdf, str):
        if not os.path.isfile(pdf):
            print(f'extract_text_from_pdf_with_easyocr error: file path does not exist: {pdf}')
            return ''
        doc = fitz.open(pdf)
    elif hasattr(pdf, 'read'):
        pdf.seek(0)
        pdf_bytes = pdf.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        pdf.seek(0)
    else:
        print(f'extract_text_from_pdf_with_easyocr error: unsupported input type {type(pdf)}')
        return ''
    reader = easyocr.Reader(['en'])
    all_text = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap()
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))
        img_np = np.array(img)
        result = reader.readtext(img_np, detail=0)
        page_text = "\n".join(result)
        print(f'EasyOCR page {i} text length: {len(page_text)}')
        all_text.append(page_text)
    return "\n".join(all_text)

# Qwen 2.5-VL 72B vision extraction (as before)
def extract_health_data_from_pdf(pdf):
    OPENROUTER_KEY = getattr(settings, 'OPENROUTER_KEY', None)
    if not OPENROUTER_KEY:
        raise Exception('OpenRouter API key not configured.')
    print(f'PDF type: {type(pdf)}')
    if is_pdf_searchable(pdf):
        print('PDF is searchable. Using DeepSeek R1 (text LLM) for extraction.')
        text = extract_text_from_pdf(pdf)
        data = extract_health_data_from_text(text)
        print('DeepSeek R1 extracted data:', data)
        return data
    # else, use EasyOCR for non-searchable PDF, then DeepSeek LLM
    print('PDF is not searchable. Using EasyOCR to extract text, then DeepSeek R1 (text LLM) for extraction.')
    text = extract_text_from_pdf_with_easyocr(pdf)
    if not text.strip():
        raise Exception('No extractable text found in PDF using OCR.')
    data = extract_health_data_from_text(text)
    print('DeepSeek R1 extracted data (from OCR):', data)
    return data
