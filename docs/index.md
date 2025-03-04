---
hide:
- navigation
- toc
- title
full_width: true
---

<style>
  .md-typeset h1 {
      font-size: 0em;
  }
</style>

<!-- Hero Section with improved content -->
<div class="hero-section">
  <div class="hero-content">
    <h1 class="hero-title">Hopsworks AI Lakehouse</h1>
    <p class="hero-subtitle">A production-grade ML platform with a Python-centric Feature Store and enterprise MLOps capabilities</p>
    <div class="hero-buttons">
      <a href="https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb" class="hero-button primary">Try Quickstart</a>
      <a href="./concepts/fs/index/" class="hero-button secondary">Explore Features</a>
      <a href="https://www.hopsworks.ai/mlops-dictionary?utm_source=web&utm_medium=docs" class="hero-button secondary">MLOps Dictionary</a>
    </div>
  </div>
</div>

<!-- Modern Architecture Diagram -->
<div class="platform-architecture">
  <div class="architecture-header">
    <h2 class="arch-title">Platform Architecture</h2>
    <p class="arch-subtitle">A comprehensive ML platform with modular components for the entire machine learning lifecycle</p>
  </div>
  
  <div class="architecture-tiers">
    <div class="architecture-tier">
      <div class="tier-header">
        <div class="tier-title-container">
          <span class="tier-icon">▧</span>
          <h3 class="tier-title">AI Lakehouse</h3>
        </div>
        <p class="tier-description">Unified storage with table formats</p>
      </div>
      <div class="tier-components">
        <div class="tier-component">
          <h4 class="component-title"><span class="component-icon">⬦</span> Storage Connectors</h4>
          <p class="component-description">Seamlessly connect to Snowflake, BigQuery, Redshift, S3, ADLS</p>
        </div>
        <div class="tier-component">
          <h4 class="component-title"><span class="component-icon">◨</span> Table Formats</h4>
          <p class="component-description">Support for Hudi, Delta, Iceberg with time travel</p>
        </div>
        <div class="tier-component">
          <h4 class="component-title"><span class="component-icon">⬗</span> Compute Portability</h4>
          <p class="component-description">Python, Spark, Flink, SQL</p>
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
          <h4 class="component-title"><span class="component-icon">⚬</span> GPU Management</h4>
          <p class="component-description">Optimize training and inference workloads</p>
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
        <div class="tier-component">
          <h4 class="component-title"><span class="component-icon">◉</span> Online Storage</h4>
          <p class="component-description">High-throughput feature vectors via RonDB</p>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Getting Started Section -->
<div class="getting-started-section">
  <div class="getting-started-content">
    <h2 class="getting-started-title">Getting Started with Hopsworks</h2>
    <p class="getting-started-description">Begin your ML journey with these simple steps</p>
    
    <div class="steps-timeline">
      <div class="timeline-track"></div>
      
      <div class="timeline-step">
        <div class="timeline-number">1</div>
        <div class="timeline-content">
          <h3 class="timeline-title"><a href="https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb">Try the Quickstart</a></h3>
          <p class="timeline-description">Explore key features with our interactive Colab notebook</p>
        </div>
      </div>
      
      <div class="timeline-step">
        <div class="timeline-number">2</div>
        <div class="timeline-content">
          <h3 class="timeline-title"><a href="./setup_installation/">Deploy Hopsworks</a></h3>
          <p class="timeline-description">Set up on your preferred cloud provider or on-premises</p>
        </div>
      </div>
      
      <div class="timeline-step">
        <div class="timeline-number">3</div>
        <div class="timeline-content">
          <h3 class="timeline-title"><a href="./concepts/fs/feature_group/feature_pipelines/">Build Feature Pipeline</a></h3>
          <p class="timeline-description">Create reusable features for your ML models</p>
        </div>
      </div>
      
      <div class="timeline-step">
        <div class="timeline-number">4</div>
        <div class="timeline-content">
          <h3 class="timeline-title"><a href="./concepts/mlops/serving/">Deploy Models</a></h3>
          <p class="timeline-description">Serve models with online and batch inference</p>
        </div>
      </div>
    </div>
    
    <div class="hero-buttons getting-started-buttons">
      <a href="https://colab.research.google.com/github/logicalclocks/hopsworks-tutorials/blob/master/quickstart.ipynb" class="hero-button primary">Launch Quickstart</a>
      <a href="./tutorials/index/" class="hero-button secondary">Browse Tutorials</a>
    </div>
  </div>
</div>

<!-- Visual Divider -->
<div class="visual-divider">
  <div class="divider-line"></div>
</div>

<!-- Platform Description -->
<div class="platform-description">
  <h2 class="description-title">Modern ML Platform for Every Team</h2>
  <p class="description-text">
    Hopsworks breaks the monolithic ML development pipeline into separate feature and training pipelines, enabling both feature reuse and better tested ML assets. Use the frameworks you already know to build production pipelines, from feature engineering to model deployment.
  </p>
</div>

<!-- Feature Navigation Grid -->
<div class="feature-grid">
  <div class="feature-card">
    <h3 class="feature-title">Feature Store</h3>
    <p class="feature-description">Store, version, and serve machine learning features</p>
    <div class="feature-links">
      <a href="./concepts/fs/index/" class="feature-link">Architecture</a>
      <a href="./concepts/fs/feature_group/fg_overview/" class="feature-link">Feature Groups</a>
      <a href="./concepts/fs/feature_view/fv_overview/" class="feature-link">Feature Views</a>
      <a href="./user_guides/fs/index/" class="feature-link">User Guide</a>
    </div>
  </div>
  
  <div class="feature-card">
    <h3 class="feature-title">Model Registry</h3>
    <p class="feature-description">Version and manage your ML models</p>
    <div class="feature-links">
      <a href="./concepts/mlops/registry/" class="feature-link">Architecture</a>
      <a href="./user_guides/mlops/registry/index/" class="feature-link">User Guide</a>
      <a href="./user_guides/mlops/registry/frameworks/tf/" class="feature-link">TensorFlow</a>
      <a href="./user_guides/mlops/registry/frameworks/skl/" class="feature-link">Scikit-learn</a>
    </div>
  </div>
  
  <div class="feature-card">
    <h3 class="feature-title">Model Serving</h3>
    <p class="feature-description">Deploy models for online and batch inference</p>
    <div class="feature-links">
      <a href="./concepts/mlops/serving/" class="feature-link">Architecture</a>
      <a href="./user_guides/mlops/serving/index/" class="feature-link">User Guide</a>
      <a href="./user_guides/mlops/serving/deployment/" class="feature-link">Deployment</a>
      <a href="./user_guides/mlops/serving/predictor/" class="feature-link">Predictor</a>
    </div>
  </div>
  
  <div class="feature-card">
    <h3 class="feature-title">Data Lineage</h3>
    <p class="feature-description">Track data and model provenance</p>
    <div class="feature-links">
      <a href="./concepts/projects/search/#lineage" class="feature-link">Architecture</a>
      <a href="./user_guides/fs/provenance/provenance/" class="feature-link">Feature Provenance</a>
      <a href="./user_guides/mlops/provenance/provenance/" class="feature-link">Model Provenance</a>
    </div>
  </div>
  
  <div class="feature-card">
    <h3 class="feature-title">Compute Engines</h3>
    <p class="feature-description">Run workloads on various compute engines</p>
    <div class="feature-links">
      <a href="./user_guides/fs/compute_engines/" class="feature-link">Overview</a>
      <a href="./user_guides/projects/jupyter/python_notebook/" class="feature-link">Python</a>
      <a href="./user_guides/projects/jupyter/spark_notebook/" class="feature-link">Spark</a>
      <a href="./user_guides/projects/jupyter/ray_notebook/" class="feature-link">Ray</a>
    </div>
  </div>
  
  <div class="feature-card">
    <h3 class="feature-title">Projects & Collaboration</h3>
    <p class="feature-description">Organize teams and ML assets</p>
    <div class="feature-links">
      <a href="./concepts/projects/governance/" class="feature-link">Governance</a>
      <a href="./concepts/projects/storage/" class="feature-link">Storage & Sharing</a>
      <a href="./user_guides/projects/project/create_project/" class="feature-link">Create Project</a>
      <a href="./user_guides/projects/project/add_members/" class="feature-link">Add Members</a>
    </div>
  </div>
</div>

<!-- Deployment Options with descriptions -->
<div class="deployment-section">
  <h2 class="deployment-section-title">Deployment Options</h2>
  <p class="deployment-section-description">Choose the deployment that best fits your organization</p>
  
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

<!-- Community Links -->
<div class="deployment-section community-section">
  <h2 class="deployment-section-title">Join the Hopsworks Community</h2>
  <p class="deployment-section-description">Connect with other users and get support</p>
  
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
  </div>
</div>

# Hopsworks AI Platform

Hopsworks is a modular AI platform with a Python-centric Feature Store and comprehensive MLOps capabilities.