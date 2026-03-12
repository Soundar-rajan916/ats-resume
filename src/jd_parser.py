def parse_job_description(jd_text):

    jd_text = jd_text.lower()

    words = jd_text.split()

    return set(words)