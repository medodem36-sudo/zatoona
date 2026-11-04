import sys, re
sys.stdout.reconfigure(encoding='utf-8')

# Let's design the JS function initSectionAccordions()
js_code = """
function initSectionAccordions(){
  const views = document.querySelectorAll('.view, div[id$="View"]');
  views.forEach(view => {
    // Find all .section-title inside this view
    const titles = view.querySelectorAll('.section-title');
    if(!titles || titles.length === 0) return;

    titles.forEach((title, idx) => {
      if(title.dataset.accordionBound) return;
      title.dataset.accordionBound = 'true';
      title.classList.add('collapsible-section-title', 'collapsed');

      // Add arrow indicator if not present
      let arrow = title.querySelector('.section-title-arrow');
      if(!arrow){
        arrow = document.createElement('span');
        arrow.className = 'section-title-arrow';
        arrow.setAttribute('aria-hidden', 'true');
        arrow.textContent = '▾';
        title.appendChild(arrow);
      }

      // Collect sibling elements until next .section-title or end of view
      const siblings = [];
      let next = title.nextElementSibling;
      while(next && !next.classList.contains('section-title') && !next.classList.contains('view')){
        // Skip hidden debug or modal overlays if any
        if(!next.classList.contains('modal-overlay')){
          siblings.push(next);
        }
        next = next.nextElementSibling;
      }

      // Tag siblings and collapse by default
      siblings.forEach(el => {
        el.classList.add('section-accordion-body', 'collapsed');
      });

      // Click event on title
      title.addEventListener('click', (e) => {
        // Don't trigger if clicked on an inner interactive button
        if(e.target.closest('button, a, input, select, textarea')) return;
        
        const isCollapsed = title.classList.contains('collapsed');
        if(isCollapsed){
          title.classList.remove('collapsed');
          siblings.forEach(el => el.classList.remove('collapsed'));
        } else {
          title.classList.add('collapsed');
          siblings.forEach(el => el.classList.add('collapsed'));
        }
        if(typeof triggerCustomHaptic === 'function') triggerCustomHaptic('light');
      });
    });
  });
}
"""
print("Accordion logic defined successfully.")
