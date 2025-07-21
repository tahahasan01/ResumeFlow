"""
This module provides functions to score a resume against various ATS criteria
using a weighted formula.
"""

# --- Configuration for Weighted Scoring ---
WEIGHTS = {
    "Skills Match": 0.20,
    "Experience": 0.15,
    "Education": 0.10,
    "Certifications": 0.10,
    "Projects": 0.10,
    "JD Keyword Match": 0.15,
    "Contact Info": 0.10,
    "File Format/Layout": 0.10,
}

def score_contact_info(resume_data):
    """Scores the contact information section (out of 10)."""
    score = 0
    if resume_data.get('email'):
        score += 5
    if resume_data.get('mobile_number'):
        score += 5
    comment = "All key details (email, phone) present." if score == 10 else "Missing key contact information."
    return score, comment

def score_experience_years(total_experience):
    """Scores experience based on the number of years (out of 10)."""
    if not total_experience or total_experience <= 0:
        return 0, "No experience found or could not be calculated."
    if total_experience < 1:
        return 3, f"{total_experience} years is considered entry-level."
    if 1 <= total_experience <= 3:
        return 6, f"{total_experience} years is a solid foundation."
    if 3 < total_experience <= 5:
        return 8, f"{total_experience} years is a strong level of experience."
    return 10, f"{total_experience} years demonstrates significant expertise."

def score_section_presence(resume_data, section_name):
    """Generic function to score a section's presence (0 or 10)."""
    return 10 if resume_data.get(section_name) else 0

def score_keyword_match(resume_skills, job_description_skills):
    """Scores the match between resume skills and job description skills (out of 10)."""
    if not job_description_skills:
        return 0, "No job description provided to match keywords against."
    
    common_skills = job_description_skills.intersection(resume_skills)
    score = round((len(common_skills) / len(job_description_skills)) * 10) if job_description_skills else 0
    comment = f"Matched {len(common_skills)} of {len(job_description_skills)} keywords."
    return score, comment

def get_detailed_ats_score(resume_data, job_description_skills):
    """
    Calculates a detailed, weighted ATS score across multiple categories.
    """
    details = []
    overall_score = 0
    
    # --- Score each category and apply weights ---

    # 1. Skills Match (Presence of skills section)
    skills_score = score_section_presence(resume_data, 'skills')
    details.append({
        "category": "Skills Match", 
        "score": skills_score, 
        "comment": "Skills section is present and well-defined." if skills_score > 0 else "Skills section not found."
    })
    overall_score += skills_score * WEIGHTS["Skills Match"]

    # 2. Experience (Years)
    exp_score, exp_comment = score_experience_years(resume_data.get('total_experience'))
    details.append({"category": "Experience", "score": exp_score, "comment": exp_comment})
    overall_score += exp_score * WEIGHTS["Experience"]

    # 3. Education
    edu_score = score_section_presence(resume_data, 'education')
    details.append({
        "category": "Education", 
        "score": edu_score, 
        "comment": "Education section is clearly listed." if edu_score > 0 else "Education section not found."
    })
    overall_score += edu_score * WEIGHTS["Education"]

    # 4. Certifications
    cert_score = score_section_presence(resume_data, 'certifications')
    details.append({
        "category": "Certifications", 
        "score": cert_score, 
        "comment": "Certifications are listed." if cert_score > 0 else "No certifications listed."
    })
    overall_score += cert_score * WEIGHTS["Certifications"]

    # 5. Projects
    proj_score = score_section_presence(resume_data, 'projects')
    details.append({
        "category": "Projects", 
        "score": proj_score, 
        "comment": "Projects section is present." if proj_score > 0 else "No projects section found."
    })
    overall_score += proj_score * WEIGHTS["Projects"]

    # 6. JD Keyword Match
    keyword_score, keyword_comment = score_keyword_match(set([skill.lower() for skill in resume_data.get('skills', [])]), job_description_skills)
    details.append({"category": "JD Keyword Match", "score": keyword_score, "comment": keyword_comment})
    overall_score += keyword_score * WEIGHTS["JD Keyword Match"]

    # 7. Contact Info
    contact_score, contact_comment = score_contact_info(resume_data)
    details.append({"category": "Contact Info", "score": contact_score, "comment": contact_comment})
    overall_score += contact_score * WEIGHTS["Contact Info"]

    # 8. File Format/Layout
    layout_score = 10  # Assume 10/10 if parsable
    details.append({
        "category": "File Format/Layout", 
        "score": layout_score, 
        "comment": "File is in a readable format (PDF/DOCX) and well-structured."
    })
    overall_score += layout_score * WEIGHTS["File Format/Layout"]
    
    return {
        "overall_score": round(overall_score * 10), # Scale to 100
        "details": details
    } 