import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app.services import prompt_builder

def test_build_prompt_basic():
    cv = "CV TEXT"
    job = "JOB DESC"
    past = "PAST LETTER"
    examples = "EXAMPLES"
    result = prompt_builder.build_prompt(cv, job, past, examples)
    assert "CV TEXT" in result
    assert "JOB DESC" in result
    assert "PAST LETTER" in result
    assert "EXAMPLES" in result
    assert "cover letter" in result.lower()

def test_build_prompt_empty_optional():
    cv = "CV"
    job = "JOB"
    result = prompt_builder.build_prompt(cv, job)
    assert "CV" in result
    assert "JOB" in result

def test_build_refinement_prompt():
    job = "Job Desc"
    orig = "Original Letter"
    feedback = "Feedback text"
    result = prompt_builder.build_refinement_prompt(job, orig, feedback)
    assert "Job Desc" in result
    assert "Original Letter" in result
    assert "Feedback text" in result
    assert "refine the cover letter" in result.lower()

