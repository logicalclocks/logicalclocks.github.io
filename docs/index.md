---
hide:
- navigation
- toc
- title
full_width: true
---

<style>
  .md-typeset h1 {
      font-size: 2em;
  }
</style>

<!-- Documentation Header -->
<div class="hero-section">
  <div class="hero-content">
    <h1 class="hero-title">Hopsworks Documentation</h1>
    <p class="hero-subtitle">Complete guides, tutorials, and references for the Hopsworks AI Lakehouse platform</p>
    <div class="hero-buttons">
      <a href="https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb" class="hero-button primary">Try Quickstart</a>
      <a href="./tutorials/index/" class="hero-button secondary">Browse Tutorials</a>
      <a href="./concepts/fs/index/" class="hero-button secondary">Read Concepts</a>
    </div>
  </div>
</div>

<!-- Documentation Overview -->
<div class="platform-description">
  <h2 class="description-title">About Hopsworks AI Platform</h2>
  <p class="description-text">
    Hopsworks is a modular AI platform with a Python-centric Feature Store and enterprise MLOps capabilities. This documentation will help you get started, learn concepts, follow guides, and configure your deployment.
  </p>
</div>

<!-- Documentation Categories Grid -->
<div class="feature-grid">
  <div class="feature-card">
    <h3 class="feature-title">Getting Started</h3>
    <p class="feature-description">Begin your journey with Hopsworks</p>
    <div class="feature-links">
      <a href="https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb" class="feature-link">Quickstart Notebook</a>
      <a href="./tutorials/index/" class="feature-link">Tutorials</a>
      <a href="./setup_installation/" class="feature-link">Installation Guide</a>
      <a href="./concepts/hopsworks/" class="feature-link">Platform Overview</a>
    </div>
  </div>
  
  <div class="feature-card">
    <h3 class="feature-title">Feature Store</h3>
    <p class="feature-description">Learn about feature engineering & serving</p>
    <div class="feature-links">
      <a href="./concepts/fs/index/" class="feature-link">Architecture</a>
      <a href="./concepts/fs/feature_group/fg_overview/" class="feature-link">Feature Groups</a>
      <a href="./concepts/fs/feature_view/fv_overview/" class="feature-link">Feature Views</a>
      <a href="./user_guides/fs/index/" class="feature-link">User Guide</a>
    </div>
  </div>
  
  <div class="feature-card">
    <h3 class="feature-title">MLOps</h3>
    <p class="feature-description">Model training, registry & serving</p>
    <div class="feature-links">
      <a href="./concepts/mlops/training/" class="feature-link">Model Training</a>
      <a href="./concepts/mlops/registry/" class="feature-link">Model Registry</a>
      <a href="./concepts/mlops/serving/" class="feature-link">Model Serving</a>
      <a href="./user_guides/mlops/index/" class="feature-link">User Guide</a>
    </div>
  </div>
  
  <div class="feature-card">
    <h3 class="feature-title">Projects & Development</h3>
    <p class="feature-description">Organize teams and ML workspaces</p>
    <div class="feature-links">
      <a href="./concepts/projects/governance/" class="feature-link">Governance</a>
      <a href="./user_guides/projects/project/create_project/" class="feature-link">Create Project</a>
      <a href="./user_guides/projects/jupyter/python_notebook/" class="feature-link">Run Notebooks</a>
      <a href="./user_guides/projects/jobs/python_job/" class="feature-link">Run Jobs</a>
    </div>
  </div>
  
  <div class="feature-card">
    <h3 class="feature-title">Administration</h3>
    <p class="feature-description">Deploy and manage Hopsworks clusters</p>
    <div class="feature-links">
      <a href="./setup_installation/admin/index/" class="feature-link">Admin Overview</a>
      <a href="./setup_installation/admin/user/" class="feature-link">User Management</a>
      <a href="./setup_installation/admin/project/" class="feature-link">Project Management</a>
      <a href="./setup_installation/admin/monitoring/grafana/" class="feature-link">Monitoring</a>
    </div>
  </div>
  
  <div class="feature-card">
    <h3 class="feature-title">API References</h3>
    <p class="feature-description">Technical documentation for developers</p>
    <div class="feature-links">
      <a href="https://docs.hopsworks.ai/hopsworks-api/dev" class="feature-link">Hopsworks API</a>
      <a href="https://docs.hopsworks.ai/hopsworks-api/dev/javadoc" class="feature-link">Feature Store JavaDoc</a>
      <a href="./user_guides/client_installation/index/" class="feature-link">Client Installation</a>
      <a href="./user_guides/integrations/index/" class="feature-link">Integrations</a>
    </div>
  </div>
</div>

<!-- How to use this documentation -->
<div class="getting-started-section">
  <div class="getting-started-content">
    <h2 class="getting-started-title">How to Use This Documentation</h2>
    <p class="getting-started-description">Navigate through our documentation with these simple steps</p>
    
    <div class="steps-timeline">
      <div class="timeline-track"></div>
      
      <div class="timeline-step">
        <div class="timeline-number">1</div>
        <div class="timeline-content">
          <h3 class="timeline-title">Start with Concepts</h3>
          <p class="timeline-description">Learn about the architecture and core components of Hopsworks</p>
        </div>
      </div>
      
      <div class="timeline-step">
        <div class="timeline-number">2</div>
        <div class="timeline-content">
          <h3 class="timeline-title">Follow User Guides</h3>
          <p class="timeline-description">Step-by-step instructions for specific tasks and workflows</p>
        </div>
      </div>
      
      <div class="timeline-step">
        <div class="timeline-number">3</div>
        <div class="timeline-content">
          <h3 class="timeline-title">Try Tutorials</h3>
          <p class="timeline-description">Complete end-to-end examples with sample code and explanations</p>
        </div>
      </div>
      
      <div class="timeline-step">
        <div class="timeline-number">4</div>
        <div class="timeline-content">
          <h3 class="timeline-title">Consult API References</h3>
          <p class="timeline-description">Technical details for programmatic access to Hopsworks</p>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Key Components Overview (Simplified Architecture) -->
<div class="platform-architecture">
  <div class="architecture-header">
    <h2 class="arch-title">Platform Components</h2>
    <p class="arch-subtitle">Explore the key components of the Hopsworks AI Platform</p>
  </div>
  
  <div class="architecture-tiers">
    <div class="architecture-tier">
      <div class="tier-header">
        <div class="tier-title-container">
          <span class="tier-icon">◩</span>
          <h3 class="tier-title">Feature Store</h3>
        </div>
        <p class="tier-description">Feature engineering and serving</p>
      </div>
      <div class="tier-components">
        <div class="tier-component">
          <h4 class="component-title"><span class="component-icon">◫</span> Feature Groups</h4>
          <p class="component-description">Logical collections of features</p>
        </div>
        <div class="tier-component">
          <h4 class="component-title"><span class="component-icon">◨</span> Feature Views</h4>
          <p class="component-description">Training data and inference vectors</p>
        </div>
        <div class="tier-component">
          <h4 class="component-title"><span class="component-icon">▣</span> Data Validation</h4>
          <p class="component-description">Statistics, expectations and monitoring</p>
        </div>
      </div>
    </div>
    
    <div class="architecture-tier">
      <div class="tier-header">
        <div class="tier-title-container">
          <span class="tier-icon">◆</span>
          <h3 class="tier-title">MLOps Platform</h3>
        </div>
        <p class="tier-description">Full machine learning lifecycle</p>
      </div>
      <div class="tier-components">
        <div class="tier-component">
          <h4 class="component-title"><span class="component-icon">◧</span> Model Registry</h4>
          <p class="component-description">Version, store, and manage ML models</p>
        </div>
        <div class="tier-component">
          <h4 class="component-title"><span class="component-icon">⇄</span> Model Serving</h4>
          <p class="component-description">KServe-based online and batch inference</p>
        </div>
        <div class="tier-component">
          <h4 class="component-title"><span class="component-icon">◎</span> Vector Database</h4>
          <p class="component-description">Similarity search via OpenSearch</p>
        </div>
      </div>
    </div>
    
    <div class="architecture-tier">
      <div class="tier-header">
        <div class="tier-title-container">
          <span class="tier-icon">▧</span>
          <h3 class="tier-title">Infrastructure</h3>
        </div>
        <p class="tier-description">Compute and storage foundation</p>
      </div>
      <div class="tier-components">
        <div class="tier-component">
          <h4 class="component-title"><span class="component-icon">⬦</span> Storage Connectors</h4>
          <p class="component-description">Connect to Snowflake, BigQuery, S3, ADLS</p>
        </div>
        <div class="tier-component">
          <h4 class="component-title"><span class="component-icon">⬗</span> Compute Engines</h4>
          <p class="component-description">Python, Spark, Flink, SQL</p>
        </div>
        <div class="tier-component">
          <h4 class="component-title"><span class="component-icon">⚬</span> GPU Management</h4>
          <p class="component-description">Optimize training and inference workloads</p>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Deployment Options with Documentation Links -->
<div class="deployment-section">
  <h2 class="deployment-section-title">Deployment Documentation</h2>
  <p class="deployment-section-description">Setup guides for different environments</p>
  
  <div class="deployment-options">
    <a href="./setup_installation/aws/getting_started/" class="deployment-option">
      <div class="cloud-icon"></div>
      <h3 class="deployment-title">AWS</h3>
      <p class="deployment-description">Deploy on Amazon Web Services</p>
    </a>
    
    <a href="./setup_installation/azure/getting_started/" class="deployment-option">
      <div class="cloud-icon"></div>
      <h3 class="deployment-title">Azure</h3>
      <p class="deployment-description">Deploy on Microsoft Azure</p>
    </a>
    
    <a href="./setup_installation/gcp/getting_started/" class="deployment-option">
      <div class="cloud-icon"></div>
      <h3 class="deployment-title">Google Cloud</h3>
      <p class="deployment-description">Deploy on Google Cloud Platform</p>
    </a>
    
    <a href="./setup_installation/on_prem/contact_hopsworks/" class="deployment-option">
      <div class="cloud-icon"></div>
      <h3 class="deployment-title">On-Premise</h3>
      <p class="deployment-description">Deploy in your data center</p>
    </a>
  </div>
</div>

<!-- Community and Support Resources -->
<div class="deployment-section community-section">
  <h2 class="deployment-section-title">Get Help & Join the Community</h2>
  <p class="deployment-section-description">Resources for questions and collaboration</p>
  
  <div class="community-links">
    <a href="https://github.com/logicalclocks/hopsworks" class="community-link">
      <span class="community-icon"></span>
      GitHub
    </a>
    <a href="https://community.hopsworks.ai/" class="community-link">
      <span class="community-icon"></span>
      Community Forum
    </a>
    <a href="https://bit.ly/publichopsworks" class="community-link">
      <span class="community-icon"></span>
      Slack Channel
    </a>
    <a href="https://www.hopsworks.ai/mlops-dictionary?utm_source=web&utm_medium=docs" class="community-link">
      <span class="community-icon"></span>
      MLOps Dictionary
    </a>
  </div>
</div>