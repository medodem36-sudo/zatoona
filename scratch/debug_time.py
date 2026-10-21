import os, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

FILE_PATH = os.path.abspath('index.html')
FILE_URL = f"file:///{FILE_PATH.replace(os.sep, '/')}"

options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)
driver.get(FILE_URL)

res = driver.execute_script('''
    localStorage.clear();
    const now = new Date();
    function fmt(d){
        const y = d.getFullYear();
        const m = String(d.getMonth()+1).padStart(2,'0');
        const dd = String(d.getDate()).padStart(2,'0');
        return `${y}-${m}-${dd}`;
    }

    const dToday = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const d3Ago = new Date(dToday.getTime() - 3 * 86400000);
    const d12Ago = new Date(dToday.getTime() - 12 * 86400000);
    const d40Ago = new Date(dToday.getTime() - 40 * 86400000);

    const isoToday = fmt(dToday);
    const iso3Ago = fmt(d3Ago);
    const iso12Ago = fmt(d12Ago);
    const iso40Ago = fmt(d40Ago);

    storageSet('daynote:' + isoToday, 'اليوم');
    storageSet('daynote:' + iso3Ago, 'من 3 أيام');
    storageSet('daynote:' + iso12Ago, 'من 12 يوم');
    storageSet('daynote:' + iso40Ago, 'من 40 يوم');
    storageSet('secnote:meal', 'ملاحظة عامة');

    storageSet('note-attachments-v1', JSON.stringify({
        ['daynote:' + isoToday]: [{ mediaId: 'm1', fileName: 'f1.jpg' }]
    }));

    // Test 1: Time filter '7d'
    notesHubState.filterType = 'all';
    notesHubState.filterTime = '7d';
    notesHubState.filterHasAtt = false;
    notesHubState.searchQuery = '';
    renderNotesHub();
    const count7d = document.querySelectorAll('#notesTimelineList .note-hub-card').length;

    // Test 2: Time filter '30d'
    notesHubState.filterTime = '30d';
    renderNotesHub();
    const count30d = document.querySelectorAll('#notesTimelineList .note-hub-card').length;

    // Test 3: Time filter 'all'
    notesHubState.filterTime = 'all';
    renderNotesHub();
    const countAll = document.querySelectorAll('#notesTimelineList .note-hub-card').length;

    // Test 4: Combined Filter (7d + hasAtt)
    notesHubState.filterTime = '7d';
    notesHubState.filterHasAtt = true;
    renderNotesHub();
    const countComb = document.querySelectorAll('#notesTimelineList .note-hub-card').length;

    const secSectionHidden = document.getElementById('notesUndatedSection').classList.contains('hidden');

    return {
        count7d: count7d,
        count30d: count30d,
        countAll: countAll,
        countComb: countComb,
        secSectionHidden: secSectionHidden
    };
''')
print("Debug Full Sequence:", res)
driver.quit()
