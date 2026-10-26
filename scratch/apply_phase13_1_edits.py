import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Target for renderSimpleChecklist
target1 = """function renderSimpleChecklist(containerId, items, state, onToggle){
  const el = document.getElementById(containerId);
  el.innerHTML = '';
  items.forEach((text, idx)=>{
    const key = 'i'+idx;
    const on = !!state[key];
    const row = document.createElement('div');
    row.className = 'check-row';
    row.innerHTML = `
      <div class="toggle-group"><button class="tbtn ${on?'on-right':''}" data-key="${key}">✓</button></div>
    `;
    row.querySelector('.tbtn').addEventListener('click', ()=> onToggle(key));
    el.appendChild(row);
  });
}"""

replacement1 = """function renderSimpleChecklist(containerId, items, state, onToggle){
  const el = document.getElementById(containerId);
  if(!el) return;
  el.innerHTML = '';
  items.forEach((text, idx)=>{
    const key = 'i'+idx;
    const on = !!state[key];
    const row = document.createElement('div');
    row.className = 'check-row';
    row.id = containerId + 'Row-' + key;
    const label = (typeof text === 'object' && text !== null) ? (text.text || text.label || JSON.stringify(text)) : String(text);
    const safeLabel = typeof escapeHtml === 'function' ? escapeHtml(label) : label;
    row.innerHTML = `
      <div class="check-left"><div class="cname">${safeLabel}</div></div>
      <div class="toggle-group"><button type="button" class="tbtn ${on?'on-right':''}" data-key="${key}" aria-label="${safeLabel}">✓</button></div>
    `;
    const btn = row.querySelector('.tbtn');
    btn.addEventListener('click', (e)=>{
      e.stopPropagation();
      onToggle(key);
    });
    row.style.cursor = 'pointer';
    row.addEventListener('click', (e)=>{
      if(e.target === btn || btn.contains(e.target)) return;
      onToggle(key);
    });
    el.appendChild(row);
  });
}"""

# 2. Target for renderScheduleChecklist
target2 = """function renderScheduleChecklist(dayIdx, settings){
  const items = scheduleChecklistItems(dayIdx, settings);
  const el = document.getElementById('scheduleChecklist');
  el.innerHTML = '';
  items.forEach(item=>{
    const on = !!scheduleCheckState[item.key];
    const row = document.createElement('div');
    row.className = 'check-row';
    row.innerHTML = `
      <div class="toggle-group"><button class="tbtn ${on?'on-right':''}" data-key="${item.key}">✓</button></div>
    `;
    row.querySelector('.tbtn').addEventListener('click', ()=>{
      scheduleCheckState[item.key] = !scheduleCheckState[item.key];
      const iso = toISO(weekDates[dayIdx]);
      saveScheduleCheck(iso, scheduleCheckState);
      weekDotsSchedule[iso] = computeDotClassSchedule(scheduleCheckState, items.length);
      renderScheduleChecklist(dayIdx, settings);
      renderTabs();
    });
    el.appendChild(row);
  });
}"""

replacement2 = """function renderScheduleChecklist(dayIdx, settings){
  const items = scheduleChecklistItems(dayIdx, settings);
  const el = document.getElementById('scheduleChecklist');
  if(!el) return;
  el.innerHTML = '';
  items.forEach(item=>{
    const on = !!scheduleCheckState[item.key];
    const row = document.createElement('div');
    row.className = 'check-row';
    row.id = 'scheduleCheckRow-' + item.key;
    const safeLabel = typeof escapeHtml === 'function' ? escapeHtml(item.label) : item.label;
    const iconHtml = item.icon ? `<span class="cicon" style="margin-left:8px;font-size:1.05rem;vertical-align:middle;">${typeof escapeHtml === 'function' ? escapeHtml(item.icon) : item.icon}</span>` : '';
    row.innerHTML = `
      <div class="check-left"><div class="cname">${iconHtml}<span>${safeLabel}</span></div></div>
      <div class="toggle-group"><button type="button" class="tbtn ${on?'on-right':''}" data-key="${item.key}" aria-label="${safeLabel}">✓</button></div>
    `;
    const btn = row.querySelector('.tbtn');
    const toggle = ()=>{
      scheduleCheckState[item.key] = !scheduleCheckState[item.key];
      const iso = toISO(weekDates[dayIdx]);
      saveScheduleCheck(iso, scheduleCheckState);
      weekDotsSchedule[iso] = computeDotClassSchedule(scheduleCheckState, items.length);
      renderScheduleChecklist(dayIdx, settings);
      renderTabs();
    };
    btn.addEventListener('click', (e)=>{
      e.stopPropagation();
      toggle();
    });
    row.style.cursor = 'pointer';
    row.addEventListener('click', (e)=>{
      if(e.target === btn || btn.contains(e.target)) return;
      toggle();
    });
    el.appendChild(row);
  });
}"""

count1 = content.count(target1)
count2 = content.count(target2)
print(f"Target 1 occurrences in index.html: {count1}")
print(f"Target 2 occurrences in index.html: {count2}")

if count1 == 1 and count2 == 1:
    content = content.replace(target1, replacement1)
    content = content.replace(target2, replacement2)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    with open('zatoona.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: index.html and zatoona.html updated and synchronized!")
else:
    print("ERROR: Targets not matched exactly 1 time.")
    sys.exit(1)
