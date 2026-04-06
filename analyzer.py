import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL, CV_SUMMARY

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

def get_job_description(url):
    """بيجيب الـ job description من الرابط"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # بياخد النص كله من الصفحة
        text = soup.get_text(separator="\n", strip=True)
        # بياخد أول 3000 حرف بس
        return text[:3000]
    except Exception as e:
        return f"Error fetching job: {str(e)}"

def analyze_job(job_url, job_title, company):
    """بيحلل الـ job ويعمل match مع الـ CV"""
    
    print(f"⏳ Fetching job description...")
    job_description = get_job_description(job_url)
    
    print(f"🤖 Analyzing with AI...")
    prompt = f"""
You are a career advisor. Analyze this job posting against the candidate's CV.

JOB TITLE: {job_title}
COMPANY: {company}
JOB DESCRIPTION:
{job_description}

CANDIDATE CV:
{CV_SUMMARY}

Provide a JSON response with exactly this format:
{{
    "match_score": <number 0-100>,
    "matching_skills": ["skill1", "skill2"],
    "missing_skills": ["skill1", "skill2"],
    "recommendation": "Apply / Consider / Skip",
    "summary": "2 sentence summary of fit"
}}

Return ONLY the JSON, no other text.
"""
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    # تست بسيط
    result = analyze_job(
        "https://www.linkedin.com/jobs/view/1234567890",
        "AI Automation Engineer",
        "Test Company"
    )
    print(result)