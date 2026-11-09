with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

def show_snippet(title, idx, before=100, after=200):
    print(f"=== {title} ===")
    print(text[max(0, idx-before):min(len(text), idx+after)].encode('ascii', 'backslashreplace').decode('ascii'))
    print()

show_snippet("1. scheduleFullGenBtn", text.find('id="scheduleFullGenBtn"'))
show_snippet("2. cardLifeBalanceWheel", text.find('id="cardLifeBalanceWheel"'))
show_snippet("3. backupReminderSettingsRow", text.find('id="backupReminderSettingsRow"'), 50, 450)
show_snippet("4. modalCheatRecovery", text.find('id="modalCheatRecovery"'), 100, 200)
show_snippet("5. renderOverview", text.find('function renderOverview(){'), 20, 300)
