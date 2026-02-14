from worker.model_dependencies import bytes_to_text, clean_text
import re


# Sections headers (used in regex)
SECTION_HEADERS = {
    "education": r"(?i)\b(education|academic|qualification|degree)\b",
    "experience": r"(?i)\b(technical\s*experience|experience|employment|work\s*history|professional\s*background)\b",
    "skills": r"(?i)\b(skills|technical\s*skills|competencies|proficiencies)\b",
    "projects": r"(?i)\b(projects|personal\s*projects)\b",
    "certifications": r"(?i)\b(certifications?|licenses?|accreditations?)\b",
    "summary": r"(?i)\b(summary|objective|profile|about\s*me)\b",
}

def parse_resume_raw(filename: str, file_bytes: bytes) -> dict:
    # Extract text from pdf
    text = clean_text(bytes_to_text(file_bytes=file_bytes,filename=filename))

    # --- Find all section header positions ---
    matches = []
    for section, pattern in SECTION_HEADERS.items():
        for match in re.finditer(pattern, text):
            matches.append((match.start(), match.end(), section, match.group()))

    # --- Sort by position in text ---
    matches.sort(key=lambda x: x[0])

    # --- Deduplicate: keep only the FIRST match per section ---
    seen = set()
    unique_matches = []
    for match in matches:
        section = match[2]
        if section not in seen:
            seen.add(section)
            unique_matches.append(match)
    matches = unique_matches

    # --- Re-sort after dedup (should already be sorted, but be safe) ---
    matches.sort(key=lambda x: x[0])

    # --- Capture text BEFORE the first header as contact info ---
    sections = {}

    # --- Extract text between headers ---
    for i, (start_pos, end_pos, section, header) in enumerate(matches):
        content_start = end_pos  # start right after the full match ends
        content_end = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        content = text[content_start:content_end].strip()

        # Only add non-empty sections
        if content:
            # If contact_info was already captured from pre-header text,
            # merge rather than overwrite
            if section == "contact_info" and "contact_info" in sections:
                sections["contact_info"] += "\n" + content
            else:
                sections[section] = content

    return sections


