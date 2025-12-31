# ========== Document Grading ==========
GRADE_PROMPT = (
    "You are a grader assessing relevance of a retrieved document.\n\n"
    "Retrieved document:\n{context}\n\n"
    "User question:\n{question}\n\n"
    "If the document is relevant, respond 'yes'. Otherwise respond 'no'."
)

# ========== Question Rewrite ==========
REWRITE_PROMPT = (
    "Look at the input and reason about the user's intent.\n"
    "Original question:\n{question}\n\n"
    "Rewrite the question to better retrieve relevant information."
)

# ========== Answer Generation ==========
GENERATE_SYSTEM_PROMPT = (
    "You are an assistant for question-answering tasks for "
    "C.V. Raman Global University (CGU), Bhubaneswar, Odisha, India."
)

# ========== Hallucination Detection ==========
HALLUCINATION_PROMPT = (
    "You are a hallucination detector.\n\n"
    "Question:\n{question}\n\n"
    "Answer:\n{answer}\n\n"
    "If the answer is incorrect, fabricated, or off-topic, respond 'yes'. "
    "Otherwise respond 'no'."
)
