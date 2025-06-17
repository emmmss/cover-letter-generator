def build_prompt(context):
    vars = context["vars"]
    cv_text = vars.get("cv_text", "")
    job_description = vars.get("job_description", "")
    past_letter_text = vars.get("past_letter_text", "")
    example_texts = vars.get("example_texts", "")

    # Build and return your final prompt string
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

def build_refinement_prompt(job_description: str, original_letter: str, feedback: str) -> str:
    return f"""
You're a cover letter refinement AI.

Here's the job description:
{job_description}

Here is the original cover letter:
{original_letter}

Here is user feedback for improving it:
{feedback}

Now refine the cover letter to better match the feedback. Preserve the tone and structure unless instructed otherwise.
"""
