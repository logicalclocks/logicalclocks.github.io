document.addEventListener('DOMContentLoaded', function() {
  // Setup API dropdown without reordering navigation
  const tabsContainer = document.querySelector('.md-tabs__list');
  if (!tabsContainer) return; // Safety check
  
  // Find API navigation item
  const apiLinkIndex = Array.from(tabsContainer.children).findIndex(item => 
    item.textContent.trim().includes('API')
  );
  
  // Only proceed if we found the API item
  if (apiLinkIndex !== -1) {
    // Create API dropdown replacement
    setupApiDropdown(tabsContainer, apiLinkIndex);
  }
});

/**
 * Sets up the API dropdown menu
 */
function setupApiDropdown(tabsContainer, apiLinkIndex) {
  // Get the original item to replace
  const apiLinkItem = tabsContainer.children[apiLinkIndex];
  
  // Create our new modal button
  const apiBtn = document.createElement('button');
  apiBtn.id = 'api-modal-btn';
  apiBtn.textContent = 'API';
  apiBtn.setAttribute('type', 'button');
  apiBtn.setAttribute('aria-haspopup', 'true');
  apiBtn.setAttribute('aria-expanded', 'false');
  
  // Create a list item to hold the button
  const apiListItem = document.createElement('li');
  apiListItem.className = 'md-tabs__item';
  
  // Copy height and padding style from original items to maintain consistency
  const originalItem = tabsContainer.children[0];
  if (originalItem) {
    const computedStyle = window.getComputedStyle(originalItem);
    apiListItem.style.height = computedStyle.height;
  }
  
  apiListItem.appendChild(apiBtn);
  
  // Replace the original API link with our button
  tabsContainer.replaceChild(apiListItem, apiLinkItem);
  
  // Create modal elements
  const modalContainer = document.createElement('div');
  modalContainer.id = 'api-modal-container';
  
  const modalContent = document.createElement('div');
  modalContent.id = 'api-modal-content';
  
  const modalHeader = document.createElement('div');
  modalHeader.id = 'api-modal-header';
  modalHeader.textContent = 'API Documentation';
  
  const closeBtn = document.createElement('span');
  closeBtn.id = 'api-modal-close';
  closeBtn.innerHTML = '&times;';
  modalHeader.appendChild(closeBtn);
  
  modalContent.appendChild(modalHeader);
  
  // Add API links
  const hopsworksApiLink = document.createElement('a');
  hopsworksApiLink.id = 'hopsworks_api_link';
  hopsworksApiLink.href = 'https://docs.hopsworks.ai/hopsworks-api/latest/generated/api/login/';
  hopsworksApiLink.textContent = 'Hopsworks API';
  modalContent.appendChild(hopsworksApiLink);
  
  const hsfsJavadocLink = document.createElement('a');
  hsfsJavadocLink.id = 'hsfs_javadoc_link';
  hsfsJavadocLink.href = 'https://docs.hopsworks.ai/hopsworks-api/latest/javadoc';
  hsfsJavadocLink.textContent = 'Feature Store JavaDoc';
  modalContent.appendChild(hsfsJavadocLink);
  
  modalContainer.appendChild(modalContent);
  document.body.appendChild(modalContainer);
  
  // Position and open modal when button is clicked
  apiBtn.addEventListener('click', function(e) {
    e.preventDefault();
    
    // Toggle dropdown visibility
    if (modalContainer.style.display === 'block') {
      modalContainer.style.display = 'none';
      apiBtn.setAttribute('aria-expanded', 'false');
    } else {
      // Get button position
      const rect = apiBtn.getBoundingClientRect();
      
      // Position the dropdown right under the button
      modalContainer.style.top = (rect.bottom + window.scrollY) + 'px';
      modalContainer.style.left = (rect.left + window.scrollX) + 'px';
      
      // Display the dropdown
      modalContainer.style.display = 'block';
      apiBtn.setAttribute('aria-expanded', 'true');
    }
    
    // Prevent event from bubbling to document
    e.stopPropagation();
  });
  
  // Close when close button is clicked
  closeBtn.addEventListener('click', function() {
    modalContainer.style.display = 'none';
    apiBtn.setAttribute('aria-expanded', 'false');
  });
  
  // Close when clicking anywhere else on the page
  document.addEventListener('click', function(e) {
    if (modalContainer.style.display === 'block' && 
        !modalContainer.contains(e.target) && 
        e.target !== apiBtn) {
      modalContainer.style.display = 'none';
      apiBtn.setAttribute('aria-expanded', 'false');
    }
  });
  
  // Close on escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && modalContainer.style.display === 'block') {
      modalContainer.style.display = 'none';
      apiBtn.setAttribute('aria-expanded', 'false');
    }
  });
}