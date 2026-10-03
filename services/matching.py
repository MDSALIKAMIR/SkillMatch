"""
SkillMatch core matching engine.
Pure-Python, no external/AI API required — this is the heart of the MVP.
"""
from flask import current_app


def calculate_match(student_skills, required_skills):
    """
    student_skills: set/list of skill names the student has (lowercase)
    required_skills: set/list of skill names the opportunity requires (lowercase)

    Returns a dict:
        {
            'percentage': int,
            'matched': [skill, ...],
            'missing': [skill, ...],
            'label': 'Excellent Match' | 'Good Match' | 'Partial Match' | 'Low Match',
            'css_class': 'match-excellent' | ...
        }
    """
    student_set = {s.strip().lower() for s in student_skills if s.strip()}
    required_set = {s.strip().lower() for s in required_skills if s.strip()}

    if not required_set:
        return {
            'percentage': 0,
            'matched': [],
            'missing': [],
            'label': 'No Requirements Listed',
            'css_class': 'match-low',
        }

    matched = sorted(required_set & student_set)
    missing = sorted(required_set - student_set)

    percentage = round((len(matched) / len(required_set)) * 100)

    label, css_class = classify_match(percentage)

    return {
        'percentage': percentage,
        'matched': matched,
        'missing': missing,
        'label': label,
        'css_class': css_class,
    }


def classify_match(percentage):
    excellent = current_app.config.get('MATCH_EXCELLENT', 80)
    good = current_app.config.get('MATCH_GOOD', 60)
    partial = current_app.config.get('MATCH_PARTIAL', 40)

    if percentage >= excellent:
        return 'Excellent Match', 'match-excellent'
    elif percentage >= good:
        return 'Good Match', 'match-good'
    elif percentage >= partial:
        return 'Partial Match', 'match-partial'
    else:
        return 'Low Match', 'match-low'


def rank_opportunities(student_profile, opportunities):
    """
    Score and sort a list of Opportunity objects for a given StudentProfile.
    Sort priority: skill match % desc, then work preference, then location, then stipend.
    Returns a list of dicts: {'opportunity': Opportunity, 'match': match_dict}
    """
    student_skills = student_profile.skill_names()
    ranked = []

    for opp in opportunities:
        match = calculate_match(student_skills, opp.required_skill_names())

        work_pref_score = 1 if (
            student_profile.work_mode in (None, 'Any') or student_profile.work_mode == opp.work_mode
        ) else 0

        location_score = 1 if (
            student_profile.preferred_location and opp.location and
            student_profile.preferred_location.strip().lower() in opp.location.strip().lower()
        ) else 0

        reward = opp.stipend if opp.type == 'Internship' else opp.salary

        ranked.append({
            'opportunity': opp,
            'match': match,
            '_work_pref_score': work_pref_score,
            '_location_score': location_score,
            '_reward': reward or 0,
        })

    ranked.sort(
        key=lambda r: (
            r['match']['percentage'],
            r['_work_pref_score'],
            r['_location_score'],
            r['_reward'],
        ),
        reverse=True
    )
    return ranked


def resume_skill_suggestions(matched_skills, missing_skills, has_projects, has_github):
    """
    Simple rule-based (non-AI) suggestions for the resume analyzer / skill gap module.
    """
    suggestions = []
    if missing_skills:
        top = ', '.join(missing_skills[:3])
        suggestions.append(f"Consider learning: {top} — these are frequently requested skills.")
    if not has_projects:
        suggestions.append("Add at least 1-2 projects with measurable results (e.g. 'reduced load time by 30%').")
    if not has_github:
        suggestions.append("Add your GitHub profile link — recruiters check this often.")
    if not suggestions:
        suggestions.append("Your profile looks solid! Keep it updated as you learn new skills.")
    return suggestions
