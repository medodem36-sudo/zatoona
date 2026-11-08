import re
import sys

sample = """عامل ايه يا معلم
•
User: "عامل ايه يا معلم" (How are you doing, teacher/boss/master?)

* Intent: Casual greeting, checking in.
* Context: The user is interacting with "Coach 

* Name: Coach Zaitouna.
* Personality: Egyptian, "gad'a" (brave/reliable), brotherly, direct, practical, motivating, enthusiastic.
* Language: 100% natural Egyptian Arabic. No formal/robotic phrasing.
* Constraint: Short response (2-3 lines max), direct, "Zaitouna" style.
* Data context: Today is 2026-11-08. User hasn't logged anything yet (0 prayers, 0 water, etc.).

* *Option 1 (Too formal/robotic):* أنا بخير شكراً لسؤالك. كيف يمكنني مساعدتك اليوم؟ (Discarded - violates Rule 1).
* *Option 2 (Too long):* الحمد لله يا صاحبي أنا زي الفل ومستعد نكسر الدنيا
"""

def sanitize_ai_coach_response(text, user_prompt=''):
    if not text:
        return ''
    
    # 1. If text has options, find non-discarded candidates
    opt_matches = re.findall(r'\*?\*?Option\s*\d+[^:]*:\*?\*?\s*([^\n\(\)]+?)(?:\s*\([^\)]*discarded[^\)]*\)|$)', text, re.I | re.M)
    candidates = [m.strip(' *\"\'') for m in opt_matches if m.strip(' *\"\'') and not re.search(r'discarded|violates|formal|robotic', m, re.I)]

    # 2. Extract dialogue quotes in Egyptian
    dialogue_quotes = re.findall(r'\"([^\"]*[\u0600-\u06FF]{3,}[^\"]*)\"', text)
    
    meta_patterns = [
        r'^\s*•?\s*User:\s*',
        r'^\s*\*?\s*(Intent|Context|Name|Personality|Language|Constraint|Data context|Opening|Closing|The \"Coach\" vibe|The \"Checking\" part|Specific prompts|Check-in|Call to action|Option \d+)\b',
        r'^\s*\*?\*?Option\s*\d+',
        r'^\s*\(Discarded\b',
        r'^\s*•?\s*$'
    ]
    
    lines = text.strip().split('\n')
    cleaned_lines = []
    for line in lines:
        l = line.strip()
        if not l:
            continue
        # Drop exact repeat of user prompt
        if user_prompt and l == user_prompt.strip():
            continue
        is_meta = any(re.search(pat, l, re.I) for pat in meta_patterns)
        if not is_meta:
            cleaned_lines.append(l)
            
    res = '\n'.join(cleaned_lines).strip()
    
    # If cleaned result is empty or contaminated with analysis remnants, fallback to candidates or quotes
    if len(res) < 10 or 'Intent:' in res or 'Option' in res:
        if candidates:
            res = candidates[-1]
        elif dialogue_quotes:
            res = ' '.join(dialogue_quotes)
        else:
            res = 'الحمد لله يا صاحبي أنا زي الفل ومستعد نكسر الدنيا سوا! يومك ماشي إزاي؟'
            
    return res

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    res = sanitize_ai_coach_response(sample, "عامل ايه يا معلم")
    print("Sanitized text:")
    print(res)
