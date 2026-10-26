import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("""  const isAdding = (encAddingForExId === ex.id);

  return `
    <div class="gym-enc-detail-card" id="encDetailView">""")

print(text[idx:idx+800])
