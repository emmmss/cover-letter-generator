def build_prompt(cv_text: str, job_description: str, past_letter_text: str = "", example_texts: str = "") -> str:
    return f"""
You're a cover letter generator AI.

Here's the job description:
{job_description}

Here is the candidate's CV:
{cv_text}

Here are a past cover letters (if any):
{past_letter_text}
{example_texts}

Now generate a tailored, professional cover letter for this job.
"""
