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
  
  // Initialize image zoom functionality
  initImageZoom();
});

/**
 * Image Zoom Functionality
 * Makes images in documentation zoomable by clicking on them
 */
function initImageZoom() {
  // Create modal container
  const modal = document.createElement('div');
  modal.className = 'img-modal';
  modal.setAttribute('role', 'dialog');
  modal.setAttribute('aria-modal', 'true');
  modal.setAttribute('aria-label', 'Image zoom view');
  
  // Create modal image
  const modalImg = document.createElement('img');
  modalImg.className = 'modal-content';
  modalImg.setAttribute('alt', '');
  
  // Create close button
  const closeBtn = document.createElement('span');
  closeBtn.className = 'close-zoom';
  closeBtn.innerHTML = '&times;';
  closeBtn.setAttribute('title', 'Close (Esc)');
  
  // Create loading spinner
  const spinner = document.createElement('div');
  spinner.className = 'zoom-loading-spinner';
  
  // Create help text
  const helpText = document.createElement('div');
  helpText.className = 'zoom-info-text';
  helpText.textContent = 'Click or press Esc to close';
  
  // Add elements to modal
  modal.appendChild(closeBtn);
  modal.appendChild(spinner);
  modal.appendChild(modalImg);
  modal.appendChild(helpText);
  
  // Add modal to page
  document.body.appendChild(modal);
  
  // Hide spinner when image loads
  modalImg.onload = function() {
    spinner.style.display = 'none';
  };
  
  // Process all suitable images in the document
  function processImages() {
    // Select all content images
    const images = document.querySelectorAll('.md-content img:not([data-zoom-processed])');
    
    images.forEach(img => {
      // Skip small images, icons and emojis
      if (img.complete && (img.naturalWidth < 100 || img.naturalHeight < 100)) {
        img.setAttribute('data-zoom-processed', 'skip');
        return;
      }
      
      if (img.classList.contains('twemoji') || 
          img.classList.contains('emojione') ||
          img.alt === 'Logo') {
        img.setAttribute('data-zoom-processed', 'skip');
        return;
      }
      
      // Mark as zoomable
      img.setAttribute('data-zoomable', 'true');
      img.setAttribute('data-zoom-processed', 'true');
      img.style.cursor = 'zoom-in';
      img.title = 'Click to zoom';
      
      // Create wrapper and zoom indicator
      const parent = img.parentElement;
      
      // Don't process images that are in links
      if (parent.tagName === 'A') {
        img.setAttribute('data-zoom-processed', 'skip');
        return;
      }
      
      // Prepare container
      let container;
      if (parent.tagName !== 'DIV' && parent.tagName !== 'FIGURE' && parent.tagName !== 'P') {
        container = document.createElement('div');
        container.className = 'zoom-image-container';
        img.parentNode.insertBefore(container, img);
        container.appendChild(img);
      } else {
        container = parent;
        container.classList.add('zoom-image-container');
      }
      
      // Add zoom indicator
      const indicator = document.createElement('div');
      indicator.className = 'zoom-indicator';
      indicator.innerHTML = '🔍';
      container.appendChild(indicator);
      
      // Add click handler
      img.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Show modal
        modal.style.display = 'block';
        
        // Show loading spinner while image loads
        spinner.style.display = 'block';
        
        // Set image source
        modalImg.src = this.src;
        modalImg.alt = this.alt || '';
        
        // Hide spinner if image is already cached
        if (modalImg.complete) {
          spinner.style.display = 'none';
        }
      });
    });
  }
  
  // Process images initially
  processImages();
  
  // Set up observer for dynamically loaded content
  const observer = new MutationObserver(function(mutations) {
    let newContent = false;
    mutations.forEach(function(mutation) {
      if (mutation.addedNodes.length) {
        newContent = true;
      }
    });
    
    if (newContent) {
      processImages();
    }
  });
  
  // Start observing
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
  
  // Close modal when clicking X
  closeBtn.addEventListener('click', function() {
    modal.style.display = 'none';
  });
  
  // Close modal when clicking anywhere
  modal.addEventListener('click', function(e) {
    if (e.target === modal) {
      modal.style.display = 'none';
    }
  });
  
  // Close modal with Escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && modal.style.display === 'block') {
      modal.style.display = 'none';
    }
  });
}
