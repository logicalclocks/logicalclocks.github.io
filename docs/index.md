---
hide:
- navigation
- toc
- title
full_width: true
---

<style>
  /* Typography system */
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }
  
  .md-typeset h1 {
    font-size: 2.5rem;
    font-weight: 600;
    line-height: 1.2;
    margin-bottom: 1.5rem;
  }
  
  .hero-title {
    font-size: 2.5rem !important;
    font-weight: 600;
    line-height: 1.2;
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
    line-height: 1.5; 
    color: var(--md-hopsworks-text-light);
  }
  
  .section-title {
    font-size: 1.6rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    text-align: center;
  }
  
  /* Spacing system */
  .section {
    margin: 60px auto;
    max-width: 1200px;
    padding: 0 24px;
  }
  
  /* Feature cards */
  .feature-grid {
    display: grid; 
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
    max-width: 1200px;
    margin: 80px auto;
    padding: 0 24px;
  }
  
  .feature-card {
    padding: 32px;
    border: 1px solid var(--md-hopsworks-border);
    background-color: var(--md-hopsworks-card-bg);
    height: 100%;
  }
  
  .feature-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-top: 0;
    margin-bottom: 24px;
    color: var(--md-hopsworks-text);
    padding-bottom: 0;
  }
  
  /* Remove green underline */
  .feature-title::after {
    display: none;
  }
  
  /* Feature links */
  .feature-link {
    display: block;
    font-size: 0.95rem;
    color: var(--md-hopsworks-primary);
    margin-bottom: 16px;
    padding-left: 16px;
    line-height: 1.5;
    position: relative;
    text-decoration: none;
  }
  
  .feature-link::before {
    content: "";
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 6px;
    height: 6px;
    background-color: var(--md-hopsworks-primary);
  }
  
  /* Component styling */
  .tier-component {
    padding: 20px;
    margin-bottom: 16px;
    border: 1px solid var(--md-hopsworks-border);
    background-color: var(--md-hopsworks-card-bg);
  }
  
  .component-title {
    font-size: 1rem;
    font-weight: 500;
    margin: 0 0 10px 0;
    line-height: 1.4;
    padding: 0;
    display: flex;
    align-items: center;
  }
  
  .component-icon {
    margin-right: 10px;
    color: var(--md-hopsworks-primary);
  }
  
  .component-description {
    margin: 0;
    line-height: 1.5;
    color: var(--md-hopsworks-text-light);
  }
  
  /* Consistent buttons */
  .hero-button {
    display: inline-block;
    padding: 12px 24px;
    font-size: 0.95rem;
    font-weight: 500;
    text-decoration: none;
    transition: all 0.2s ease;
    border: 1px solid var(--md-hopsworks-primary);
  }
  
  .hero-button.primary {
    background-color: var(--md-hopsworks-primary);
    color: white;
  }
  
  .hero-button.secondary {
    background-color: transparent;
    color: var(--md-hopsworks-primary);
  }
  
  .hero-button:hover {
    opacity: 0.9;
  }
  
  /* Code blocks */
  code {
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
    padding: 0.2em 0.4em;
    font-size: 0.9em;
    background-color: var(--md-hopsworks-code-bg);
  }
  
  /* Responsive adjustments */
  @media (max-width: 960px) {
    .feature-grid {
      grid-template-columns: repeat(2, 1fr);
    }
    
    .hero-title {
      font-size: 2rem !important;
    }
  }
  
  @media (max-width: 600px) {
    .feature-grid {
      grid-template-columns: 1fr;
    }
  }
</style>

<!-- Hero Section -->
<div class="hero-section" style="position: relative; overflow: hidden; width: 100vw; max-width: 100vw; margin-left: calc(-50vw + 50%);">
  <div class="hero-content">
    <h1 class="hero-title">Hopsworks Documentation</h1>
    <p class="hero-subtitle">Complete guides for building production ML systems with <br> the Hopsworks AI platform</p>
    
        <!-- Button array for getting started options -->
    <div style="display: flex; gap: 16px; margin-top: 40px; justify-content: center; flex-wrap: wrap;">
      <a href="https://app.hopsworks.ai" target="_blank" class="hero-button primary" style="min-width: 200px;">Hopsworks Serverless</a>
      <a href="./tutorials" class="hero-button secondary" style="min-width: 170px;">Browse Tutorials</a>
      <a href="./concepts/fs" class="hero-button secondary" style="min-width: 170px;">Explore Capabilities</a>
    </div>
    
    <!-- Python Installation Section with consistent width -->
    <div style="max-width: 800px; margin: 60px auto 0; text-align: center; padding: 0 24px;">
      <h3 style="font-size: 1.3rem; margin-bottom: 20px; font-weight: 600;">Access Hopsworks from Python</h3>
      
      <p style="margin-bottom: 20px; color: var(--md-hopsworks-text-light);">
        Install the Hopsworks Python library to interact with the platform from your Python environment.
        The Python profile ensures all required dependencies are installed.
      </p>
      
      <div class="highlight" style="margin: 24px auto; max-width: 500px;">
      <pre style="margin: 0;"><code class="language-bash">pip install hopsworks[python]</code></pre>
      </div>
      
      <a href="./user_guides/client_installation/" class="hero-button secondary" style="display: inline-block; min-width: 200px;">
        Client Installation Guide
      </a>
    </div>
  </div>
</div>


<!-- Quick Access Section -->
<div class="feature-grid">
  <div class="feature-card">
    <h3 class="feature-title">Getting Started</h3>
    <div class="feature-links">
      <a href="./concepts/hopsworks/" class="feature-link">Platform Overview</a>
      <a href="./setup_installation/" class="feature-link">Installation Guide</a>
      <a href="./user_guides/client_installation/index/" class="feature-link">Client Setup</a>
      <a href="./tutorials/" class="feature-link">Tutorials</a>
    </div>
  </div>
  
  <div class="feature-card">
    <h3 class="feature-title">Popular Guides</h3>
    <div class="feature-links">
      <a href="./concepts/fs/feature_group/fg_overview/" class="feature-link">Feature Groups</a>
      <a href="./concepts/fs/feature_view/fv_overview/" class="feature-link">Feature Views</a>
      <a href="./concepts/mlops/serving/" class="feature-link">Model Serving</a>
      <a href="./concepts/mlops/opensearch/" class="feature-link">Vector Database</a>
    </div>
  </div>
  
  <div class="feature-card">
    <h3 class="feature-title">Developer Resources</h3>
    <div class="feature-links">
      <a href="https://docs.hopsworks.ai/hopsworks-api/dev" class="feature-link">API Reference</a>
      <a href="https://docs.hopsworks.ai/hopsworks-api/dev/javadoc" class="feature-link">Java SDK</a>
      <a href="./user_guides/integrations/python/" class="feature-link">Python SDK</a>
      <a href="./user_guides/integrations/index/" class="feature-link">Integrations</a>
    </div>
  </div>
</div>

<!-- Platform Architecture -->
<div class="section">
  <div style="display: flex; gap: 30px; flex-wrap: wrap; justify-content: space-between;">
    <div style="flex: 1; min-width: 320px; padding: 0 0 30px;">
      <div style="display: flex; align-items: center; margin-bottom: 16px;">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 12px; color: var(--md-hopsworks-primary);">
          <path d="M3 3h18v18H3z"></path>
          <path d="M3 9h18"></path>
          <path d="M9 21V9"></path>
        </svg>
        <h3 style="margin: 0; font-size: 1.3rem; font-weight: 600;">Feature Store</h3>
      </div>
      <p style="margin-top: 0; margin-bottom: 24px; color: var(--md-hopsworks-text-light); line-height: 1.5;">Feature engineering and serving</p>
      <div style="display: flex; flex-direction: column; gap: 16px;">
        <div class="tier-component" style="padding: 20px;">
          <h4 class="component-title" style="margin-top: 0; margin-bottom: 10px;">
            <svg class="component-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
            </svg>
            <a href="./concepts/fs/feature_group/fg_overview/">Feature Groups</a>
          </h4>
          <p class="component-description" style="margin: 0; line-height: 1.5;">Organize and version your features</p>
        </div>
        <div class="tier-component" style="padding: 20px;">
          <h4 class="component-title" style="margin-top: 0; margin-bottom: 10px;">
            <svg class="component-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="9" y1="3" x2="9" y2="21"></line>
            </svg>
            <a href="./concepts/fs/feature_view/fv_overview/">Feature Views</a>
          </h4>
          <p class="component-description" style="margin: 0; line-height: 1.5;">Create training sets and feature vectors</p>
        </div>
        <div class="tier-component" style="padding: 20px;">
          <h4 class="component-title" style="margin-top: 0; margin-bottom: 10px;">
            <svg class="component-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;">
              <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
            </svg>
            <a href="./concepts/fs/feature_group/fg_statistics/">Data Validation</a>
          </h4>
          <p class="component-description" style="margin: 0; line-height: 1.5;">Statistics, expectations, and monitoring</p>
        </div>
      </div>
    </div>
    <div style="flex: 1; min-width: 320px; padding: 0 0 30px;">
      <div style="display: flex; align-items: center; margin-bottom: 16px;">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 12px; color: var(--md-hopsworks-primary);">
          <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
          <rect x="8" y="7" width="8" height="8" rx="1"></rect>
          <path d="M6 11h12"></path>
        </svg>
        <h3 style="margin: 0; font-size: 1.3rem; font-weight: 600;">MLOps</h3>
      </div>
      <p style="margin-top: 0; margin-bottom: 24px; color: var(--md-hopsworks-text-light); line-height: 1.5;">Model management and operations</p>
      <div style="display: flex; flex-direction: column; gap: 16px;">
        <div class="tier-component" style="padding: 20px;">
          <h4 class="component-title" style="margin-top: 0; margin-bottom: 10px;">
            <svg class="component-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;">
              <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
              <path d="M2 17l10 5 10-5"></path>
              <path d="M2 12l10 5 10-5"></path>
            </svg>
            <a href="./concepts/mlops/registry/">Model Registry</a>
          </h4>
          <p class="component-description" style="margin: 0; line-height: 1.5;">Version, store, and manage ML models</p>
        </div>
        <div class="tier-component" style="padding: 20px;">
          <h4 class="component-title" style="margin-top: 0; margin-bottom: 10px;">
            <svg class="component-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
            </svg>
            <a href="./concepts/mlops/serving/">Model Serving</a>
          </h4>
          <p class="component-description" style="margin: 0; line-height: 1.5;">Deploy models for online and batch inference</p>
        </div>
        <div class="tier-component" style="padding: 20px;">
          <h4 class="component-title" style="margin-top: 0; margin-bottom: 10px;">
            <svg class="component-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;">
              <circle cx="12" cy="12" r="10"></circle>
              <circle cx="12" cy="12" r="6"></circle>
              <circle cx="12" cy="12" r="2"></circle>
            </svg>
            <a href="./concepts/mlops/opensearch/">Vector Database</a>
          </h4>
          <p class="component-description" style="margin: 0; line-height: 1.5;">Similarity search and vector embeddings</p>
        </div>
      </div>
    </div>
    <div style="flex: 1; min-width: 320px; padding: 0 0 30px;">
      <div style="display: flex; align-items: center; margin-bottom: 16px;">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 12px; color: var(--md-hopsworks-primary);">
          <path d="M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
          <path d="M15 3h6v6"></path>
          <line x1="10" y1="14" x2="21" y2="3"></line>
        </svg>
        <h3 style="margin: 0; font-size: 1.3rem; font-weight: 600;">Infrastructure</h3>
      </div>
      <p style="margin-top: 0; margin-bottom: 24px; color: var(--md-hopsworks-text-light); line-height: 1.5;">Platform foundation and connectivity</p>
      <div style="display: flex; flex-direction: column; gap: 16px;">
        <div class="tier-component" style="padding: 20px;">
          <h4 class="component-title" style="margin-top: 0; margin-bottom: 10px;">
            <svg class="component-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;">
              <path d="M20 16V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v9m16 0H4m16 0 1.28 2.55a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45L4 16"></path>
            </svg>
            <a href="./user_guides/fs/storage_connector/index/">Storage Connectors</a>
          </h4>
          <p class="component-description" style="margin: 0; line-height: 1.5;">Connect to external data platforms</p>
        </div>
        <div class="tier-component" style="padding: 20px;">
          <h4 class="component-title" style="margin-top: 0; margin-bottom: 10px;">
            <svg class="component-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;">
              <path d="M18 6 6 18"></path>
              <path d="m6 6 12 12"></path>
            </svg>
            <a href="./user_guides/fs/compute_engines/">Compute Engines</a>
          </h4>
          <p class="component-description" style="margin: 0; line-height: 1.5;">Python, Spark, Flink processing</p>
        </div>
        <div class="tier-component" style="padding: 20px;">
          <h4 class="component-title" style="margin-top: 0; margin-bottom: 10px;">
            <svg class="component-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;">
              <rect x="2" y="3" width="20" height="18" rx="2"></rect>
              <path d="M8 7v10"></path>
              <path d="M16 7v10"></path>
              <path d="M12 7v10"></path>
            </svg>
            <a href="./setup_installation/admin/project/">Resource Management</a>
          </h4>
          <p class="component-description" style="margin: 0; line-height: 1.5;">GPU allocation and project governance</p>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Kubernetes Installer Section -->
<div class="callout-box" >
  <h2 style="font-size: 1.6rem; font-weight: 600; margin-top: 0; margin-bottom: 2rem; text-align: center;">Hopsworks K8s Installer</h2>
  <div style="max-width: 1200px; margin: 0 auto;">
    <p style="text-align: center; margin-bottom: 20px;">Hopsworks is an enterprise-grade distributed AI Lakehouse platform with a feature store. Deploy a distributed system on your Kubernetes cluster with our installer:</p>
    
    <!-- Code block outside of HTML structure to ensure proper rendering -->
</div>

<div style="max-width: 1200px; margin: 0 auto;">
```bash
curl -O https://raw.githubusercontent.com/logicalclocks/hopsworks-k8s-installer/master/install-hopsworks.py
python3 install-hopsworks.py
```
</div>
</div>

<div class="callout-box" style="margin-top: 24px;">
  <div style="display: grid; grid-template-columns: 3fr 2fr; gap: 24px; align-items: flex-start; max-width: 1200px; margin: 0 auto;">
    <div>
      <h4 style="margin-top: 0; font-size: 1.1rem; margin-bottom: 16px;">Minimum Requirements:</h4>
      <ul>
        <li>Supported Platforms: AWS (EKS), Google Cloud (GKE), Azure (AKS), or OVHCloud</li>
        <li>Kubernetes cluster version ≥ 1.27.0</li>
        <li>Minimum of 4-5 nodes recommended</li>
        <li>Administrative access to your cloud platform</li>
      </ul>
      <h4 style="font-size: 1.1rem; margin-bottom: 16px;">Required Tools:</h4>
      <ul>
        <li>Kubernetes CLI (<code>kubectl</code>)</li>
        <li>Package manager (<code>helm</code>)</li>
        <li>Respective cloud CLI tool (<code>aws</code>/<code>gcloud</code>/<code>az</code>)</li>
        <li>Other libraries (<code>boto3, PyYAML</code>)</li>
      </ul>
      
      <a href="https://github.com/logicalclocks/hopsworks-k8s-installer" target="_blank" class="hero-button secondary" style="display: inline-block; margin-top: 16px; padding: 8px 16px; font-size: 0.9rem;">
        View on GitHub ↗
      </a>
    </div>
    
    <div style="background-color: var(--md-hopsworks-card-bg); padding: 24px; border: 1px solid var(--md-hopsworks-border);">
      <h4 style="margin-top: 0; font-size: 1.1rem; color: var(--md-hopsworks-primary); margin-bottom: 16px;">Enterprise Deployment</h4>
      <p>For production and development deployment of Hopsworks Enterprise, we offer options on global or sovereign clouds with Enterprise SLAs.</p>
      
      <h4 style="font-size: 1.1rem; color: var(--md-hopsworks-primary); margin-bottom: 16px;">Deployment Options</h4>
      <ul style="padding-left: 20px; margin-bottom: 16px;">
        <li>Serverless (fastest way to start)</li>
        <li>Any cloud provider</li>
        <li>On-premises infrastructure</li>
        <li>Hybrid setups</li>
      </ul>
      
      <a href="https://app.hopsworks.ai" target="_blank" class="hero-button primary" style="display: block; text-align: center; margin-top: 16px;">
        Hopsworks Serverless
      </a>
      <a href="https://www.hopsworks.ai/contact" target="_blank" class="hero-button secondary" style="display: block; text-align: center; margin-top: 12px;">
        Contact for Enterprise License
      </a>
      <a href="https://www.hopsworks.ai/evaluation-license" target="_blank" class="hero-button secondary" style="display: block; text-align: center; margin-top: 12px;">
        Evaluation License  
      </a>
    </div>
  </div>
</div>

<!-- Hopsworks Academy Video Section -->
<div class="getting-started-section" style="margin-top: 30px;">
  <div class="getting-started-content" style="max-width: 1200px;">
    <h2 style="font-size: 1.6rem; font-weight: 600; margin-bottom: 1.5rem; text-align: center;">Hopsworks Academy</h2>
    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 24px; align-items: stretch;">
      <!-- Main Featured Video -->
      <div style="border: 1px solid var(--md-hopsworks-border); transition: all 0.2s ease;">
        <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
          <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" 
            src="https://www.youtube.com/embed/s20w8nKCK2o" 
            title="Introduction to Hopsworks" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
          </iframe>
        </div>
        <div style="padding: 20px; text-align: left;">
          <h3 style="margin: 0 0 10px 0; color: var(--md-hopsworks-text); font-size: 1.2rem; font-weight: 600; text-align: left;">Introduction to Hopsworks</h3>
          <p style="margin: 0 0 15px 0; color: var(--md-hopsworks-text-light); font-size: 0.9rem; line-height: 1.5; text-align: left;">Get started with the Hopsworks platform and learn about its core capabilities for ML projects.</p>
          <div style="display: flex; gap: 15px; font-size: 0.8rem; color: var(--md-hopsworks-text-light); text-align: left;">
            <div style="display: flex; align-items: center;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 5px;">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
              Playing Now
            </div>
          </div>
        </div>
      </div>
      
      <!-- Playlist Column -->
      <div style="border: 1px solid var(--md-hopsworks-border); height: 100%; overflow-y: auto;">
        <div style="position: sticky; top: 0; background: var(--md-hopsworks-card-bg); padding: 16px; border-bottom: 1px solid var(--md-hopsworks-border); z-index: 10; text-align: left;">
          <h3 style="margin: 0; color: var(--md-hopsworks-text); font-size: 1.1rem; font-weight: 600; text-align: left;">Featured Tutorials</h3>
        </div>
        
        <!-- Scrollable playlist items -->
        <div>
          <!-- Video 1 (Main video) -->
          <a href="https://www.youtube.com/watch?v=s20w8nKCK2o" target="_blank" style="display: flex; padding: 16px; text-decoration: none; border-bottom: 1px solid var(--md-hopsworks-border); transition: background-color 0.2s; background-color: rgba(30, 179, 130, 0.08);">
            <div style="width: 120px; min-width: 120px; position: relative; margin-right: 16px;">
              <img src="https://img.youtube.com/vi/s20w8nKCK2o/mqdefault.jpg" style="width: 100%; height: auto; display: block;">
            </div>
            <div style="text-align: left;">
              <h4 style="margin: 0 0 5px 0; color: var(--md-hopsworks-text); font-size: 0.9rem; font-weight: 500; line-height: 1.3; text-align: left;">Introduction to Hopsworks</h4>
              <p style="margin: 0; color: var(--md-hopsworks-text-light); font-size: 0.75rem; line-height: 1.3; text-align: left;">Get started with Hopsworks platform</p>
            </div>
          </a>
          
          <!-- Video 2 -->
          <a href="https://www.youtube.com/watch?v=v3n_8s_qpF8&list=PLgN6fhzkSui_YzFsY6E1f_U86OATEYLC6" target="_blank" style="display: flex; padding: 16px; text-decoration: none; border-bottom: 1px solid var(--md-hopsworks-border); transition: background-color 0.2s;">
            <div style="width: 120px; min-width: 120px; position: relative; margin-right: 16px;">
              <img src="https://img.youtube.com/vi/v3n_8s_qpF8/mqdefault.jpg" style="width: 100%; height: auto; display: block;">
            </div>
            <div style="text-align: left;">
              <h4 style="margin: 0 0 5px 0; color: var(--md-hopsworks-text); font-size: 0.9rem; font-weight: 500; line-height: 1.3; text-align: left;">Model Serving in Hopsworks</h4>
              <p style="margin: 0; color: var(--md-hopsworks-text-light); font-size: 0.75rem; line-height: 1.3; text-align: left;">Deploy models for online inference</p>
            </div>
          </a>
          
          <!-- Video 3 -->
          <a href="https://www.youtube.com/watch?v=N-hUC3b0IQs&list=PLgN6fhzkSui_YzFsY6E1f_U86OATEYLC6" target="_blank" style="display: flex; padding: 16px; text-decoration: none; border-bottom: 1px solid var(--md-hopsworks-border); transition: background-color 0.2s;">
            <div style="width: 120px; min-width: 120px; position: relative; margin-right: 16px;">
              <img src="https://img.youtube.com/vi/N-hUC3b0IQs/mqdefault.jpg" style="width: 100%; height: auto; display: block;">
            </div>
            <div style="text-align: left;">
              <h4 style="margin: 0 0 5px 0; color: var(--md-hopsworks-text); font-size: 0.9rem; font-weight: 500; line-height: 1.3; text-align: left;">Feature Store Workshop</h4>
              <p style="margin: 0; color: var(--md-hopsworks-text-light); font-size: 0.75rem; line-height: 1.3; text-align: left;">Introduction to the Hopsworks Feature Store</p>
            </div>
          </a>
          
          <!-- Video 4 -->
          <a href="https://www.youtube.com/watch?v=ccYe1MU4R2U&list=PLgN6fhzkSui_YzFsY6E1f_U86OATEYLC6" target="_blank" style="display: flex; padding: 16px; text-decoration: none; border-bottom: 1px solid var(--md-hopsworks-border); transition: background-color 0.2s;">
            <div style="width: 120px; min-width: 120px; position: relative; margin-right: 16px;">
              <img src="https://img.youtube.com/vi/ccYe1MU4R2U/mqdefault.jpg" style="width: 100%; height: auto; display: block;">
            </div>
            <div style="text-align: left;">
              <h4 style="margin: 0 0 5px 0; color: var(--md-hopsworks-text); font-size: 0.9rem; font-weight: 500; line-height: 1.3; text-align: left;">Feature Views Explained</h4>
              <p style="margin: 0; color: var(--md-hopsworks-text-light); font-size: 0.75rem; line-height: 1.3; text-align: left;">Creating and using Feature Views for ML</p>
            </div>
          </a>
          
          <!-- Video 5 -->
          <a href="https://www.youtube.com/watch?v=8Axs0q1AY7o&list=PLgN6fhzkSui_YzFsY6E1f_U86OATEYLC6" target="_blank" style="display: flex; padding: 16px; text-decoration: none; border-bottom: 1px solid var(--md-hopsworks-border); transition: background-color 0.2s;">
            <div style="width: 120px; min-width: 120px; position: relative; margin-right: 16px;">
              <img src="https://img.youtube.com/vi/8Axs0q1AY7o/mqdefault.jpg" style="width: 100%; height: auto; display: block;">
            </div>
            <div style="text-align: left;">
              <h4 style="margin: 0 0 5px 0; color: var(--md-hopsworks-text); font-size: 0.9rem; font-weight: 500; line-height: 1.3; text-align: left;">Getting Started with Hopsworks</h4>
              <p style="margin: 0; color: var(--md-hopsworks-text-light); font-size: 0.75rem; line-height: 1.3; text-align: left;">First steps with the Hopsworks platform</p>
            </div>
          </a>
          
          <!-- Video 6 -->
          <a href="https://www.youtube.com/watch?v=_X0U0z1TAcI&list=PLgN6fhzkSui_YzFsY6E1f_U86OATEYLC6" target="_blank" style="display: flex; padding: 16px; text-decoration: none; border-bottom: 1px solid var(--md-hopsworks-border); transition: background-color 0.2s;">
            <div style="width: 120px; min-width: 120px; position: relative; margin-right: 16px;">
              <img src="https://img.youtube.com/vi/_X0U0z1TAcI/mqdefault.jpg" style="width: 100%; height: auto; display: block;">
            </div>
            <div style="text-align: left;">
              <h4 style="margin: 0 0 5px 0; color: var(--md-hopsworks-text); font-size: 0.9rem; font-weight: 500; line-height: 1.3; text-align: left;">Data Validation in Feature Store</h4>
              <p style="margin: 0; color: var(--md-hopsworks-text-light); font-size: 0.75rem; line-height: 1.3; text-align: left;">Ensuring data quality in feature pipelines</p>
            </div>
          </a>
        </div>
      </div>
    </div>
    
    <div style="margin-top: 24px; text-align: center;">
      <a href="https://www.youtube.com/playlist?list=PLgN6fhzkSui_YzFsY6E1f_U86OATEYLC6" target="_blank" class="hero-button secondary" style="display: inline-block; padding: 12px 24px; font-size: 0.9rem; min-width: 220px;">
        View Full Academy Playlist
      </a>
    </div>
  </div>
</div>

<!-- Role-Based Documentation -->
<div class="feature-grid" style="margin-top: 30px;">
  <div class="feature-card">
    <h3 class="feature-title">For Data Engineers</h3>
    <p class="feature-description">Build and optimize feature pipelines</p>
    <div class="feature-links">
      <a href="./concepts/fs/feature_group/feature_pipelines/" class="feature-link">Feature Pipelines</a>
      <a href="./user_guides/fs/feature_group/create/" class="feature-link">Create Feature Groups</a>
      <a href="./user_guides/fs/feature_group/data_validation/" class="feature-link">Data Validation</a>
      <a href="./user_guides/fs/storage_connector/index/" class="feature-link">Storage Connectors</a>
    </div>
  </div>
  
  <div class="feature-card">
    <h3 class="feature-title">For Data Scientists</h3>
    <p class="feature-description">Build models using high-quality features</p>
    <div class="feature-links">
      <a href="./user_guides/fs/feature_view/training-data/" class="feature-link">Create Training Datasets</a>
      <a href="./user_guides/projects/jupyter/python_notebook/" class="feature-link">Jupyter Notebooks</a>
      <a href="./user_guides/mlops/registry/frameworks/tf/" class="feature-link">Register TensorFlow Models</a>
      <a href="./user_guides/fs/vector_similarity_search/" class="feature-link">Vector Similarity Search</a>
    </div>
  </div>
  
  <div class="feature-card">
    <h3 class="feature-title">For MLOps Engineers</h3>
    <p class="feature-description">Deploy and monitor ML systems</p>
    <div class="feature-links">
      <a href="./user_guides/mlops/serving/deployment/" class="feature-link">Deploy Models</a>
      <a href="./user_guides/mlops/serving/api-protocol/" class="feature-link">Serving APIs</a>
      <a href="./user_guides/fs/feature_view/feature_monitoring/" class="feature-link">Feature Monitoring</a>
      <a href="./user_guides/projects/scheduling/kube_scheduler/" class="feature-link">Kubernetes Scheduling</a>
    </div>
  </div>
</div>

<!-- Deployment Options -->
<div class="section">
  <h2 style="font-size: 1.6rem; font-weight: 600; margin-bottom: 1.5rem; text-align: center;">Deployment Options</h2>
  <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px;">
    <a href="./setup_installation/aws/getting_started/" style="text-decoration: none; border: 1px solid var(--md-hopsworks-border); padding: 32px 24px; text-align: center; transition: all 0.2s ease;">
      <img src="../images/icons8-aws-240.png" style="width: 72px; height: 72px; margin-bottom: 16px;">
      <h3 style="margin: 0 0 8px 0; font-size: 1.2rem; font-weight: 600; color: var(--md-hopsworks-text);">AWS</h3>
    </a>
    <a href="./setup_installation/azure/getting_started/" style="text-decoration: none; border: 1px solid var(--md-hopsworks-border); padding: 32px 24px; text-align: center; transition: all 0.2s ease;">
      <img src="../images/azure_logo.png" style="width: 72px; height: 72px; margin-bottom: 16px; object-fit: contain;">
      <h3 style="margin: 0 0 8px 0; font-size: 1.2rem; font-weight: 600; color: var(--md-hopsworks-text);">Azure</h3>
    </a>
    <a href="./setup_installation/gcp/getting_started/" style="text-decoration: none; border: 1px solid var(--md-hopsworks-border); padding: 32px 24px; text-align: center; transition: all 0.2s ease;">
      <img src="../images/gcp_logo.png" style="width: 72px; height: 72px; margin-bottom: 16px; object-fit: contain;">
      <h3 style="margin: 0 0 8px 0; font-size: 1.2rem; font-weight: 600; color: var(--md-hopsworks-text);">GCP</h3>
    </a>
    <a href="./setup_installation/on_prem/contact_hopsworks/" style="text-decoration: none; border: 1px solid var(--md-hopsworks-border); padding: 32px 24px; text-align: center; transition: all 0.2s ease;">
      <img src="../images/server_logo.png" style="width: 72px; height: 72px; margin-bottom: 16px; object-fit: contain;">
      <h3 style="margin: 0 0 8px 0; font-size: 1.2rem; font-weight: 600; color: var(--md-hopsworks-text);">On-Premise</h3>
    </a>
  </div>
</div>

