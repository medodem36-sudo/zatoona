with open('docs/PROJECT_STATUS.md', 'r', encoding='utf-8') as f:
    text = f.read()

# remove extra trailing newlines to leave exactly one newline at EOF
clean_text = text.rstrip() + '\n'

with open('docs/PROJECT_STATUS.md', 'w', encoding='utf-8') as f:
    f.write(clean_text)

print('Cleaned EOF newline.')
