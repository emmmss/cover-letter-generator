def build_prompt(cv_text: str, job_description: str, past_letter_text: str = "") -> str:
    return f"""
You're a cover letter generator AI.

Here's the job description:
{job_description}

Here is the candidate's CV:
{cv_text}

Here is a past cover letter (if any):
{past_letter_text}

Now generate a tailored, professional cover letter for this job.
"""
