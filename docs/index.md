---
hide:
- navigation
- toc
- title
---

<style>
  .md-typeset h1 {
      font-size: 0em;
  }
</style>

<!-- Simplified Hopsworks Architecture Diagram -->
<div class="hopsworks-diagram">
  <div class="platform-header">
    <h2 class="platform-title">Feature Store & MLOps Platform</h2>
    <p class="platform-subtitle">Store, discover, and serve ML features and models</p>
  </div>
  
  <div class="architecture-row">
    <!-- Feature Store Section -->
    <div class="feature-store-section">
      <div class="section-header">
        <svg class="section-icon" viewBox="0 0 24 24">
          <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
          <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
          <line x1="12" y1="22.08" x2="12" y2="12"></line>
        </svg>
        <h3 class="section-title">Feature Store</h3>
      </div>
      
      <div class="api-container">
        <div class="api-column">
          <span class="api-label">Write API</span>
          <a href="./concepts/fs/feature_group/fg_overview/" class="api-link">Feature Groups</a>
          <a href="./concepts/fs/feature_group/external_fg/" class="api-link">External Feature Groups</a>
        </div>
        
        <div class="api-column">
          <span class="api-label">Read API</span>
          <a href="./concepts/fs/feature_view/fv_overview/" class="api-link">Feature Views</a>
          <a href="./concepts/fs/feature_view/offline_api/" class="api-link sub">Training Data</a>
          <a href="./concepts/fs/feature_view/online_api/" class="api-link sub">Feature Vectors</a>
        </div>
      </div>
      
      <div class="feature-tools">
        <a href="./concepts/projects/search/" class="feature-tool">
          <svg class="feature-tool-icon" viewBox="0 0 24 24">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <span>Search</span>
        </a>
        <a href="./concepts/fs/feature_group/versioning/" class="feature-tool">
          <svg class="feature-tool-icon" viewBox="0 0 24 24">
            <polyline points="16 18 22 12 16 6"></polyline>
            <polyline points="8 6 2 12 8 18"></polyline>
          </svg>
          <span>Versioning</span>
        </a>
        <a href="./concepts/fs/feature_group/feature_monitoring/" class="feature-tool">
          <svg class="feature-tool-icon" viewBox="0 0 24 24">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
          </svg>
          <span>Monitoring</span>
        </a>
      </div>
    </div>
    
    <!-- MLOps Section -->
    <div class="mlops-section">
      <div class="section-header">
        <svg class="section-icon" viewBox="0 0 24 24">
          <polyline points="22 12 16 12 14 15 10 15 8 12 2 12"></polyline>
          <path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"></path>
        </svg>
        <h3 class="section-title">MLOps</h3>
      </div>
      
      <div class="mlops-workflow">
        <a href="./concepts/mlops/training/" class="mlops-step">
          <svg class="mlops-step-icon" viewBox="0 0 24 24">
            <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
            <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
          </svg>
          <span class="mlops-step-label">Training</span>
        </a>
        
        <svg class="workflow-arrow" viewBox="0 0 24 24">
          <line x1="5" y1="12" x2="19" y2="12"></line>
          <polyline points="12 5 19 12 12 19"></polyline>
        </svg>
        
        <a href="./concepts/mlops/registry/" class="mlops-step">
          <svg class="mlops-step-icon" viewBox="0 0 24 24">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="3" y1="9" x2="21" y2="9"></line>
            <line x1="9" y1="21" x2="9" y2="9"></line>
          </svg>
          <span class="mlops-step-label">Registry</span>
        </a>
        
        <svg class="workflow-arrow" viewBox="0 0 24 24">
          <line x1="5" y1="12" x2="19" y2="12"></line>
          <polyline points="12 5 19 12 12 19"></polyline>
        </svg>
        
        <a href="./concepts/mlops/serving/" class="mlops-step">
          <svg class="mlops-step-icon" viewBox="0 0 24 24">
            <rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect>
            <rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect>
            <line x1="6" y1="6" x2="6.01" y2="6"></line>
            <line x1="6" y1="18" x2="6.01" y2="18"></line>
          </svg>
          <span class="mlops-step-label">Serving</span>
        </a>
      </div>
      
      <div class="mlops-features">
        <a href="./concepts/mlops/opensearch/" class="mlops-feature">
          <svg class="mlops-feature-icon" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="2" y1="12" x2="22" y2="12"></line>
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
          </svg>
          <span>Vector DB</span>
        </a>
        
        <a href="./concepts/projects/search#lineage" class="mlops-feature">
          <svg class="mlops-feature-icon" viewBox="0 0 24 24">
            <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
            <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
          </svg>
          <span>Lineage</span>
        </a>
        
        <a href="./concepts/projects/governance/" class="mlops-feature">
          <svg class="mlops-feature-icon" viewBox="0 0 24 24">
            <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
            <path d="M2 17l10 5 10-5"></path>
            <path d="M2 12l10 5 10-5"></path>
          </svg>
          <span>Projects</span>
        </a>
      </div>
    </div>
  </div>
  
  <div class="platform-row">
    <div class="tech-section">
      <div class="section-header">
        <svg class="section-icon" viewBox="0 0 24 24">
          <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
          <rect x="2" y="9" width="4" height="12"></rect>
          <circle cx="4" cy="4" r="2"></circle>
        </svg>
        <h3 class="section-title">Integrations</h3>
      </div>
      
      <div class="tech-grid">
        <a href="./concepts/fs/feature_group/feature_pipelines#feature-engineering-in-pandas" class="tech-item">
          <span class="tech-icon">🐼</span>
          <span>Pandas</span>
        </a>
        <a href="./concepts/fs/feature_group/feature_pipelines#feature-engineering-in-spark" class="tech-item">
          <span class="tech-icon">⚡</span>
          <span>Spark</span>
        </a>
        <a href="./concepts/fs/feature_group/feature_pipelines#feature-engineering-in-flink" class="tech-item">
          <span class="tech-icon">🌊</span>
          <span>Flink</span>
        </a>
        <a href="./concepts/fs/feature_group/feature_pipelines#feature-engineering-in-sql" class="tech-item">
          <span class="tech-icon">📊</span>
          <span>SQL</span>
        </a>
      </div>
      
      <div class="tech-grid">
        <a href="./user_guides/fs/storage_connector/creation/jdbc/" class="tech-item">
          <span class="tech-icon">🔌</span>
          <span>JDBC</span>
        </a>
        <a href="./user_guides/fs/storage_connector/creation/bigquery/" class="tech-item">
          <span class="tech-icon">📈</span>
          <span>BigQuery</span>
        </a>
        <a href="./user_guides/fs/storage_connector/creation/s3/" class="tech-item">
          <span class="tech-icon">☁️</span>
          <span>S3</span>
        </a>
        <a href="./user_guides/fs/storage_connector/creation/snowflake/" class="tech-item">
          <span class="tech-icon">❄️</span>
          <span>Snowflake</span>
        </a>
      </div>
    </div>
    
    <div class="deployment-section">
      <div class="section-header">
        <svg class="section-icon" viewBox="0 0 24 24">
          <rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect>
          <rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect>
          <line x1="6" y1="6" x2="6.01" y2="6"></line>
          <line x1="6" y1="18" x2="6.01" y2="18"></line>
        </svg>
        <h3 class="section-title">Deployment</h3>
      </div>
      
      <div class="cloud-providers">
        <a href="./setup_installation/azure/getting_started/" class="cloud-provider">
          <img src="images/icons8-azure.svg" alt="Azure" class="cloud-icon">
          <span>Azure</span>
        </a>
        <a href="./setup_installation/aws/getting_started/" class="cloud-provider">
          <img src="images/icons8-amazon-web-services.svg" alt="AWS" class="cloud-icon">
          <span>AWS</span>
        </a>
        <a href="./setup_installation/gcp/getting_started/" class="cloud-provider">
          <img src="images/icons8-google-cloud.svg" alt="Google Cloud" class="cloud-icon">
          <span>Google Cloud</span>
        </a>
        <a href="./setup_installation/on_prem/contact_hopsworks/" class="cloud-provider">
          <img src="images/icons8-database.svg" alt="On-Premise" class="cloud-icon">
          <span>On-Premise</span>
        </a>
      </div>
    </div>
  </div>
</div>

<img src="images/hopsworks-logo-2022.svg" loading="lazy" alt="" class="image_logo_02">

# Hopsworks: Feature Store & MLOps Platform

Hopsworks is a modular data platform with a Python-centric Feature Store and comprehensive MLOps capabilities. Use it as a standalone Feature Store or leverage its full suite of tools to manage your entire ML lifecycle.

## Feature Store

Hopsworks breaks the monolithic model development pipeline into separate feature and training pipelines, enabling both feature reuse and better tested ML assets. You can develop features in any Python, Spark, or Flink environment, either inside or outside Hopsworks.

Use the Python frameworks you already know to build production feature pipelines:
- Compute aggregations in Pandas
- Validate feature data with Great Expectations
- Reduce dimensionality with embeddings and PCA
- Test feature logic end-to-end with PyTest
- Transform features with Scikit-Learn, TensorFlow, and PyTorch

## Wide Range of Capabilities

- **Feature Pipelines**: Support for Python, PySpark, Spark, Flink, and SQL
- **Storage Flexibility**: Store offline features in Hopsworks as Hudi tables or connect to external systems (Snowflake, Databricks, Redshift, BigQuery)
- **Online Serving**: Industry-leading throughput and availability with RonDB

## MLOps on Hopsworks

Hopsworks provides comprehensive model management through KServe:
- Feature/prediction logging to Kafka 
- Secure, low-latency model deployments via Istio
- Model versioning with the Model Registry
- Vector database for similarity search through OpenSearch

## Project-based Collaboration

Hopsworks creates secure sandboxes for teams to collaborate and share ML assets:
- Fine-grained sharing across project boundaries
- End-to-end team responsibility from raw data to models
- Development, staging, and production environments
- Versioning, lineage, and provenance for all ML assets

## Available on Any Platform

Deploy Hopsworks anywhere:
- Cloud: AWS, Azure, GCP
- On-Premises: Ubuntu/Redhat compatible, including air-gapped environments
- Serverless: Fully managed platform for features and models

## Join the Community

- Get help in the [Hopsworks Community](https://community.hopsworks.ai/)
- Follow us on [Twitter](https://twitter.com/hopsworks)
- Check out our [product releases](https://github.com/logicalclocks/hopsworks/releases)
- Join our [Slack channel](https://join.slack.com/t/public-hopsworks/shared_invite/zt-24fc3hhyq-VBEiN8UZlKsDrrLvtU4NaA)