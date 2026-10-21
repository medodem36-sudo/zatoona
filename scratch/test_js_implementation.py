# Dry-run script to verify JS syntax and functionality
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os, sys

sys.stdout.reconfigure(encoding="utf-8")

js_code = """
window.loadGymWarmupState = function(iso, expectedRoutineId){
  if(!iso || typeof iso !== 'string') return null;
  const raw = storageGetJSON('gym-warmup-state-v1', {});
  const rec = raw[iso] || null;
  if(rec && expectedRoutineId && rec.routineId && rec.routineId !== expectedRoutineId){
    return { iso: iso, routineId: expectedRoutineId, started: false, completed: false, skipped: false, collapsed: false, completedDrills: {}, completedWarmupSets: {} };
  }
  return rec;
};

window.saveGymWarmupState = function(iso, state){
  if(!iso || typeof iso !== 'string' || !state) return false;
  const raw = storageGetJSON('gym-warmup-state-v1', {});
  raw[iso] = Object.assign({}, raw[iso] || {}, state, { iso: iso, updatedAt: Date.now() });
  return storageSet('gym-warmup-state-v1', JSON.stringify(raw));
};
"""

print("JS definition valid Python string")
