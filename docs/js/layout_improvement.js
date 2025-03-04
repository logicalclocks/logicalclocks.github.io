document.addEventListener('DOMContentLoaded', function() {
  // Add toggle functionality for the table of contents
  const tocSidebar = document.querySelector('.md-sidebar--secondary');
  if (tocSidebar) {
    tocSidebar.addEventListener('click', function(e) {
      if (e.target === tocSidebar || e.target === tocSidebar.querySelector('::before')) {
        if (window.innerWidth >= 1220) {
          tocSidebar.classList.toggle('md-sidebar--collapsed');
        } else {
          tocSidebar.classList.toggle('md-sidebar--expanded');
        }
      }
    });
  }
  
  // Apply full-width class to content area if page has full_width frontmatter
  const contentInner = document.querySelector('.md-content__inner');
  if (document.body.hasAttribute('data-full-width')) {
    contentInner.classList.add('full-width');
  }
});
