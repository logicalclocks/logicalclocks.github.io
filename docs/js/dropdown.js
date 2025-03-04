document.addEventListener('DOMContentLoaded', function() {
  // Reorganize navigation links
  const tabsContainer = document.querySelector('.md-tabs__list');
  if (!tabsContainer) return; // Safety check
  
  const navItems = Array.from(tabsContainer.children);
  
  // Find navigation items we want to reorder
  const gettingStartedIndex = navItems.findIndex(item => 
    item.textContent.trim().includes('Getting Started')
  );
  
  const communityIndex = navItems.findIndex(item => 
    item.textContent.trim().includes('Community')
  );
  
  const apiLinkIndex = navItems.findIndex(item => 
    item.textContent.trim().includes('API')
  );
  
  // Only proceed if we found items to reposition
  if (apiLinkIndex !== -1) {
    // Create API dropdown replacement
    setupApiDropdown(tabsContainer, apiLinkIndex);
    
    // Reorder external links if found
    if (gettingStartedIndex !== -1 && communityIndex !== -1) {
      reorderNavLinks(tabsContainer, gettingStartedIndex, communityIndex);
    }
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

/**
 * Reorders navigation links to move external links to the end
 */
function reorderNavLinks(tabsContainer, gettingStartedIndex, communityIndex) {
  // To avoid index shifting, we need to adjust indices when removing
  // Clone the items first so we can re-add them in the right order
  const gettingStartedItem = tabsContainer.children[gettingStartedIndex].cloneNode(true);
  const communityItem = tabsContainer.children[communityIndex].cloneNode(true);
  
  // Check if there's an API item which we created
  // Note: :has() selector might not be supported in all browsers, using alternative
  const apiItem = Array.from(tabsContainer.querySelectorAll('li')).find(li => 
    li.querySelector('#api-modal-btn')
  );
  
  // Remove items (in reverse order to avoid index shifting)
  if (communityIndex > gettingStartedIndex) {
    tabsContainer.removeChild(tabsContainer.children[communityIndex]);
    tabsContainer.removeChild(tabsContainer.children[gettingStartedIndex]);
  } else {
    tabsContainer.removeChild(tabsContainer.children[gettingStartedIndex]);
    tabsContainer.removeChild(tabsContainer.children[communityIndex < gettingStartedIndex ? communityIndex : communityIndex - 1]);
  }
  
  // If we have our API item, move it as well
  if (apiItem) {
    tabsContainer.removeChild(apiItem);
  }
  
  // Add items in the desired order at the end
  if (apiItem) {
    tabsContainer.appendChild(apiItem);
  }
  tabsContainer.appendChild(gettingStartedItem);
  tabsContainer.appendChild(communityItem);
}