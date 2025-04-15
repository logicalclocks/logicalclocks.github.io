/**
 * Lightweight background animation with floating nodes
 * Only runs on the index page
 */

document.addEventListener('DOMContentLoaded', function() {
  // Only run on the index page
  const currentPath = window.location.pathname;
  console.log("Current path:", currentPath);
  
  // Check if we're on the homepage/index
  // This will match paths like /, /index.html, /latest/, /latest/index.html
  if (!currentPath.endsWith('/') && 
      !currentPath.endsWith('/index.html') && 
      !currentPath.match(/\/(?:latest|[\d\.]+)\/?$/) && 
      !currentPath.match(/\/(?:latest|[\d\.]+)\/index\.html$/)) {
    console.log("Not on index page, skipping animation");
    return;
  }
  
  // Create canvas element
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  
  // Add CSS class for styling
  canvas.className = 'bg-animation-canvas';
  
  // Additional inline styles (these can be moved to CSS if preferred)
  canvas.style.opacity = '0.7'; // Increased opacity for visibility
  
  // Find the hero section and insert the canvas into it
  const heroSection = document.querySelector('.hero-section');
  if (heroSection) {
    // Make hero section position relative if it's not already
    if (getComputedStyle(heroSection).position !== 'relative') {
      heroSection.style.position = 'relative';
    }
    
    // Make sure overflow is hidden
    heroSection.style.overflow = 'hidden';
    
    // Insert at the beginning of the hero section
    heroSection.insertBefore(canvas, heroSection.firstChild);
    console.log("Canvas inserted into hero section");
  } else {
    console.warn("Hero section not found, inserting into body");
    // Fallback to body insertion
    document.body.insertBefore(canvas, document.body.firstChild);
  }
  
  // Resize canvas to full window width
  function resizeCanvas() {
    // Always use window width to ensure full width
    canvas.width = window.innerWidth;
    
    // Use hero section height if available
    if (heroSection) {
      canvas.height = heroSection.offsetHeight;
    } else {
      canvas.height = window.innerHeight;
    }
    
    console.log(`Canvas resized to ${canvas.width}x${canvas.height}`);
  }
  
  // Initialize nodes
  const NODES_COUNT = 25; // Increased node count
  const nodes = [];
  
  function initNodes() {
    nodes.length = 0;
    
    for (let i = 0; i < NODES_COUNT; i++) {
      nodes.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 4 + 2, // Larger radius for better visibility
        speedX: (Math.random() - 0.5) * 0.3, // Slightly faster movement
        speedY: (Math.random() - 0.5) * 0.3,
        opacity: Math.random() * 0.6 + 0.4 // Higher opacity
      });
    }
  }
  
  // Draw nodes and connections
  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Get primary color from CSS variable (Hopsworks green)
    const primaryColor = getComputedStyle(document.documentElement)
      .getPropertyValue('--md-hopsworks-primary')
      .trim() || '#1eb382';
    
    // Update and draw nodes
    for (let i = 0; i < nodes.length; i++) {
      const node = nodes[i];
      
      // Move nodes
      node.x += node.speedX;
      node.y += node.speedY;
      
      // Bounce off edges
      if (node.x < 0 || node.x > canvas.width) node.speedX *= -1;
      if (node.y < 0 || node.y > canvas.height) node.speedY *= -1;
      
      // Draw node
      ctx.beginPath();
      ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${hexToRgb(primaryColor)}, ${node.opacity})`;
      ctx.fill();
      
      // Draw connections to nearby nodes
      for (let j = i + 1; j < nodes.length; j++) {
        const otherNode = nodes[j];
        const dx = node.x - otherNode.x;
        const dy = node.y - otherNode.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        // Only connect close nodes
        if (distance < 200) { // Increased connection distance
          ctx.beginPath();
          ctx.moveTo(node.x, node.y);
          ctx.lineTo(otherNode.x, otherNode.y);
          // Make lines more visible based on distance
          const lineOpacity = (1 - distance / 200) * 0.4; // More visible lines
          ctx.strokeStyle = `rgba(${hexToRgb(primaryColor)}, ${lineOpacity})`;
          ctx.lineWidth = 1; // Thicker lines
          ctx.stroke();
        }
      }
    }
    
    requestAnimationFrame(draw);
  }
  
  // Helper function to convert hex to rgb
  function hexToRgb(hex) {
    // Remove # if present
    hex = hex.replace(/^#/, '');
    
    // Parse hex components to RGB
    const bigint = parseInt(hex, 16);
    const r = (bigint >> 16) & 255;
    const g = (bigint >> 8) & 255;
    const b = bigint & 255;
    
    return `${r}, ${g}, ${b}`;
  }
  
  // Initialize canvas and animation
  window.addEventListener('resize', resizeCanvas);
  resizeCanvas();
  initNodes();
  draw();
});