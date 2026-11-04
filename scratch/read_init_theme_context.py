with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 474750
print(text[pos:pos+600])
