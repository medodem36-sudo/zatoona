import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target1 = """  const isAdding = (encAddingForExId === ex.id);

  return `
    <div class="gym-enc-detail-card" id="encDetailView">"""

print("Target 1 found:", target1 in text)

target2 = """      customExercises[newKey] = {
        key: newKey,
        catalogId: selectedEx.id,
        fromCatalog: true,
        split: split,
        name: selectedEx.nameAr || selectedEx.name,
        equip: getEncyclopediaEquipLabel(selectedEx.equipment),
        target: (selectedEx.primaryMuscles || []).map(m => getEncyclopediaMuscleLabel(m)).join('، '),
        sets: setsVal,
        reps: repsVal,
        optional: false,
        optNote: '',
        tip: (selectedEx.instructions && selectedEx.instructions[0]) || '',
        breath: '',
        steps: Array.isArray(selectedEx.instructions) ? selectedEx.instructions : [],
        mistakes: [],
        link: '',
        img: '',
        credit: ''
      };"""

print("Target 2 found:", target2 in text)
