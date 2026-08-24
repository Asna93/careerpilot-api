import json

from decouple import config
from openai import OpenAI

client = OpenAI(api_key=config('OPENAI_API_KEY'))


def analyze_resume_with_ai(resume_text: str, job_description: str) -> dict:
    """
    Analyze resume against job description using OpenAI ChatGPT.
    Returns a dict with match_score, matching_skills, missing_skills, etc.
    """

    prompt = f"""
    You are an expert HR and recruiting analyst. Analyze the following resume against the job description.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}

    Please provide analysis in JSON format with these exact fields:
    {{
        "match_score": <0-100 integer>,
        "match_level": "<low|moderate|strong>",
        "matching_skills": [<list of 5-8 skills found in both>],
        "missing_skills": [<list of 4-6 important skills not in resume>],
        "strengths": [<list of 3-4 resume strengths relevant to job>],
        "areas_for_improvement": [<list of 3-4 areas to improve>],
        "keyword_suggestions": [<list of 8-10 keywords to add to resume>],
        "overall_recommendation": "<2-3 sentence recommendation>"
    }}

    Return ONLY valid JSON, no other text.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=1000,
        response_format={"type": "json_object"},
    )

    result_text = response.choices[0].message.content
    return json.loads(result_text)


def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from a PDF or DOCX file.
    """
    if file_path.endswith('.pdf'):
        import PyPDF2

        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    elif file_path.endswith('.docx'):
        from docx import Document

        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text

    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")
