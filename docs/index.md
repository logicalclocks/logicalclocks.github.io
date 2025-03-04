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

<!-- Modern Architecture Diagram -->
<div class="platform-architecture">
  <div class="architecture-header">
    <h2 class="arch-title">Hopsworks AI Platform Architecture</h2>
    <p class="arch-subtitle">A comprehensive ML platform with a modular design approach for data storage, feature engineering, model management, and deployment</p>
  </div>
  
  <div class="architecture-tiers">
    <div class="architecture-tier">
      <div class="tier-header">
        <h3 class="tier-title">AI Lakehouse</h3>
        <p class="tier-description">Unified storage with table formats</p>
      </div>
      <div class="tier-components">
        <div class="tier-component">
          <h4 class="component-title">Storage Connectors</h4>
          <p class="component-description">Snowflake, BigQuery, Redshift, S3, ADLS</p>
        </div>
        <div class="tier-component">
          <h4 class="component-title">Table Format</h4>
          <p class="component-description">Hudi tables with time travel capabilities</p>
        </div>
        <div class="tier-component">
          <h4 class="component-title">Compute Portability</h4>
          <p class="component-description">Python, Spark, Flink, SQL</p>
        </div>
      </div>
    </div>
    
    <div class="architecture-tier">
      <div class="tier-header">
        <h3 class="tier-title">MLOps Platform</h3>
        <p class="tier-description">Full machine learning lifecycle</p>
      </div>
      <div class="tier-components">
        <div class="tier-component">
          <h4 class="component-title">Model Registry</h4>
          <p class="component-description">Version, store, and manage ML models</p>
        </div>
        <div class="tier-component">
          <h4 class="component-title">Model Serving</h4>
          <p class="component-description">KServe-based online and batch inference</p>
        </div>
        <div class="tier-component">
          <h4 class="component-title">GPU Management</h4>
          <p class="component-description">Optimize training and inference workloads</p>
        </div>
        <div class="tier-component">
          <h4 class="component-title">Vector Database</h4>
          <p class="component-description">Similarity search via OpenSearch</p>
        </div>
      </div>
    </div>
    
    <div class="architecture-tier">
      <div class="tier-header">
        <h3 class="tier-title">Feature Store</h3>
        <p class="tier-description">Feature engineering and serving</p>
      </div>
      <div class="tier-components">
        <div class="tier-component">
          <h4 class="component-title">Feature Groups</h4>
          <p class="component-description">Logical collections of features</p>
        </div>
        <div class="tier-component">
          <h4 class="component-title">Feature Views</h4>
          <p class="component-description">Training data and inference vectors</p>
        </div>
        <div class="tier-component">
          <h4 class="component-title">Data Validation</h4>
          <p class="component-description">Statistics, expectations and monitoring</p>
        </div>
        <div class="tier-component">
          <h4 class="component-title">Online Storage</h4>
          <p class="component-description">High-throughput feature vectors via RonDB</p>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Interlude Text -->
<div class="interlude-text">
  <h2 class="interlude-title">Python-centric ML Platform</h2>
  <p class="interlude-description">
    Hopsworks breaks the monolithic model development pipeline into separate feature and training pipelines, enabling both feature reuse and better tested ML assets. Use the frameworks you already know to build production pipelines, from feature engineering to model deployment.
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

<!-- Deployment Options -->
<div class="deployment-options">
  <a href="./setup_installation/aws/getting_started/" class="deployment-option">
    <div class="placeholder-icon"></div>
    <h3 class="deployment-title">AWS</h3>
  </a>
  
  <a href="./setup_installation/azure/getting_started/" class="deployment-option">
    <div class="placeholder-icon"></div>
    <h3 class="deployment-title">Azure</h3>
  </a>
  
  <a href="./setup_installation/gcp/getting_started/" class="deployment-option">
    <div class="placeholder-icon"></div>
    <h3 class="deployment-title">Google Cloud</h3>
  </a>
  
  <a href="./setup_installation/on_prem/contact_hopsworks/" class="deployment-option">
    <div class="placeholder-icon"></div>
    <h3 class="deployment-title">On-Premise</h3>
  </a>
</div>

# Hopsworks AI Platform

Hopsworks is a modular AI platform with a Python-centric Feature Store and comprehensive MLOps capabilities.