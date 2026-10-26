import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replacement 1: in renderEncyclopediaDetailHtml
target1 = """  const isAdding = (encAddingForExId === ex.id);

  return `
    <div class="gym-enc-detail-card" id="encDetailView">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px; flex-wrap:wrap; margin-bottom:12px;">
        <div>
          <div style="font-size:1.15rem; font-weight:700; color:var(--text); display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <span>${encEscape(ex.nameAr || ex.name)}</span>
            ${routineStatusBadge}
          </div>
          <div style="font-size:.82rem; color:var(--muted); font-weight:500; direction:ltr; text-align:right;">${encEscape(ex.name || '')}</div>
          ${aliasesText ? `<div style="font-size:.74rem; color:var(--accent); margin-top:3px;">أسماء شائعة: ${encEscape(aliasesText)}</div>` : ''}
        </div>
        <div style="display:flex; gap:6px; align-items:center; flex-wrap:wrap;">
          <button id="encAddToRoutineBtn" type="button" class="reset-btn" style="border-color:var(--primary); color:var(--primary); background:var(--primary-light); font-weight:700; font-size:.8rem; padding:5px 12px; cursor:pointer;" title="إضافة هذا التمرين لبرنامجك الرياضي">
            ➕ إضافة للروتين
          </button>
          <button id="encCloseDetailBtn" type="button" class="reset-btn" style="border-color:var(--line); font-size:.78rem; padding:5px 12px; cursor:pointer;">
            ← العودة للقائمة
          </button>
        </div>
      </div>

      ${encAddSuccessMessage ? `
        <div id="encAddSuccessAlert" style="background:var(--primary-light); border:1px solid var(--primary); color:var(--primary); padding:10px 14px; border-radius:10px; margin-bottom:12px; font-size:.82rem; font-weight:600; display:flex; align-items:center; justify-content:space-between; gap:8px;">
          <span>${encEscape(encAddSuccessMessage)}</span>
          <button type="button" class="reset-btn" id="encCloseSuccessAlertBtn" style="border:none; background:transparent; font-size:.9rem; cursor:pointer; color:var(--primary);">✕</button>
        </div>
      ` : ''}"""

# Normalise newlines for search if needed
norm_target1 = target1.replace('\r\n', '\n')
norm_content = content.replace('\r\n', '\n')

assert norm_target1 in norm_content, "target1 not found in content"

replacement1 = """  const defaultImg = (Array.isArray(ex.images) && ex.images.length > 0) ? ex.images[0] : (ex.img || '');
  const imgRecord = (typeof getExerciseImageRecord === 'function') ? getExerciseImageRecord(ex.id) : null;
  let encImgSrc = '';
  if(imgRecord && imgRecord.type === 'url' && imgRecord.url){
    encImgSrc = imgRecord.url;
  } else if(imgRecord && imgRecord.type === 'local' && imgRecord.mediaId && typeof activeExerciseBlobUrls !== 'undefined' && activeExerciseBlobUrls.has(imgRecord.mediaId)){
    encImgSrc = activeExerciseBlobUrls.get(imgRecord.mediaId);
  } else if(defaultImg){
    encImgSrc = defaultImg;
  }

  const isAdding = (encAddingForExId === ex.id);

  return `
    <div class="gym-enc-detail-card" id="encDetailView">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px; flex-wrap:wrap; margin-bottom:12px;">
        <div>
          <div style="font-size:1.15rem; font-weight:700; color:var(--text); display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <span>${encEscape(ex.nameAr || ex.name)}</span>
            ${routineStatusBadge}
          </div>
          <div style="font-size:.82rem; color:var(--muted); font-weight:500; direction:ltr; text-align:right;">${encEscape(ex.name || '')}</div>
          ${aliasesText ? `<div style="font-size:.74rem; color:var(--accent); margin-top:3px;">أسماء شائعة: ${encEscape(aliasesText)}</div>` : ''}
        </div>
        <div style="display:flex; gap:6px; align-items:center; flex-wrap:wrap;">
          <button id="encAddToRoutineBtn" type="button" class="reset-btn" style="border-color:var(--primary); color:var(--primary); background:var(--primary-light); font-weight:700; font-size:.8rem; padding:5px 12px; cursor:pointer;" title="إضافة هذا التمرين لبرنامجك الرياضي">
            ➕ إضافة للروتين
          </button>
          <button id="encCloseDetailBtn" type="button" class="reset-btn" style="border-color:var(--line); font-size:.78rem; padding:5px 12px; cursor:pointer;">
            ← العودة للقائمة
          </button>
        </div>
      </div>

      ${encAddSuccessMessage ? `
        <div id="encAddSuccessAlert" style="background:var(--primary-light); border:1px solid var(--primary); color:var(--primary); padding:10px 14px; border-radius:10px; margin-bottom:12px; font-size:.82rem; font-weight:600; display:flex; align-items:center; justify-content:space-between; gap:8px;">
          <span>${encEscape(encAddSuccessMessage)}</span>
          <button type="button" class="reset-btn" id="encCloseSuccessAlertBtn" style="border:none; background:transparent; font-size:.9rem; cursor:pointer; color:var(--primary);">✕</button>
        </div>
      ` : ''}

      ${encImgSrc ? `
        <div style="margin-bottom:14px; text-align:center; background:var(--card-alt); border-radius:12px; padding:10px; border:1px solid var(--line);">
          <img src="${encEscape(encImgSrc)}" alt="${encEscape(ex.nameAr || ex.name)}" style="max-width:100%; max-height:190px; height:auto; border-radius:8px; object-fit:contain;" onerror="this.parentElement.style.display='none';">
        </div>
      ` : ''}"""

# Replacement 2: in encConfirmAddBtn
target2 = """        steps: Array.isArray(selectedEx.instructions) ? selectedEx.instructions : [],
        mistakes: [],
        link: '',
        img: '',
        credit: ''"""

norm_target2 = target2.replace('\r\n', '\n')
assert norm_target2 in norm_content, "target2 not found in content"

replacement2 = """        steps: Array.isArray(selectedEx.instructions) ? selectedEx.instructions : [],
        mistakes: [],
        link: '',
        img: (Array.isArray(selectedEx.images) && selectedEx.images.length > 0) ? selectedEx.images[0] : (selectedEx.img || ''),
        credit: (selectedEx.license) ? `${selectedEx.source || ''} · ${selectedEx.license}` : (selectedEx.credit || '')"""

# Apply replacements to norm_content
norm_content = norm_content.replace(norm_target1, replacement1.replace('\r\n', '\n'), 1)
norm_content = norm_content.replace(norm_target2, replacement2.replace('\r\n', '\n'), 1)

# Restore CRLF
final_content = norm_content.replace('\n', '\r\n')

with open('index.html', 'w', encoding='utf-8', newline='') as f:
    f.write(final_content)

print("Updated index.html successfully.")
