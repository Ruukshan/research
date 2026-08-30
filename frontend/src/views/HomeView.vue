<template>
  <div class="home-view container">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-badge">
        <span class="badge badge-synthetic">Academic Research Project</span>
        <span class="hero-subbadge">Sri Lankan GCE A/L Decision Support</span>
      </div>

      <h1 class="hero-title">
        Smart Career Pathway Recommendation System <br />
        <span class="gradient-text">for Advanced Level Students</span>
      </h1>

      <p class="hero-subtitle">
        Empowering Sri Lankan Grade 11–13 students with personalized, ranked, and explainable
        career pathways through machine learning stream prediction, hybrid recommendation fusion, and SHAP explainability.
      </p>

      <div class="hero-actions">
        <router-link to="/assessment" class="btn btn-primary btn-lg">
          Begin Student Assessment ➔
        </router-link>
        <router-link to="/dashboard" class="btn btn-secondary btn-lg">
          View Research Dashboard
        </router-link>
      </div>

      <div class="disclaimer-banner mt-4">
        <span>⚖️</span>
        <p>
          <strong>Decision Support Only:</strong> This system provides AI-assisted recommendations. It is designed to complement,
          not replace, guidance from teachers, career counsellors, parents, and official university admission handbooks.
        </p>
      </div>
    </section>

    <!-- Research Methodology & Pipeline Section -->
    <section class="pipeline-section mt-6">
      <div class="section-header text-center">
        <h2 class="section-title">Core Research Contribution</h2>
        <p class="section-desc">A five-tier hybrid architecture connecting student aptitude to higher education and occupational outcomes.</p>
      </div>

      <div class="pipeline-grid mt-4">
        <div class="pipeline-card">
          <div class="pipeline-step-num">01</div>
          <div class="pipeline-icon">📝</div>
          <h3>Student Profile Intake</h3>
          <p>Captures GCE O/L grades, basket electives, extracurricular leadership, and 6 Holland RIASEC personality traits.</p>
        </div>

        <div class="pipeline-card">
          <div class="pipeline-step-num">02</div>
          <div class="pipeline-icon">🧠</div>
          <h3>ML Stream Classifier</h3>
          <p>Multi-class probabilistic model comparing Random Forest, XGBoost, and Deep Neural Networks across 5 A/L streams.</p>
        </div>

        <div class="pipeline-card">
          <div class="pipeline-step-num">03</div>
          <div class="pipeline-icon">⚙️</div>
          <h3>Hybrid Score Fusion</h3>
          <p>Blends ML Stream Probability + Content-Based Pathway Similarity + Collaborative User Filtering with configurable weights.</p>
        </div>

        <div class="pipeline-card">
          <div class="pipeline-step-num">04</div>
          <div class="pipeline-icon">🏆</div>
          <h3>Ranked Top-5 Pathways</h3>
          <p>Delivers diverse, highly relevant Sri Lankan state university degrees, professional paths, and emerging careers.</p>
        </div>

        <div class="pipeline-card">
          <div class="pipeline-step-num">05</div>
          <div class="pipeline-icon">🔍</div>
          <h3>SHAP Explainability</h3>
          <p>Transparent feature attribution revealing positive and negative drivers behind individual predictions.</p>
        </div>
      </div>
    </section>

    <!-- Five A/L Streams Grid -->
    <section class="streams-section mt-6">
      <div class="section-header">
        <h2 class="section-title">Supported Sri Lankan A/L Streams</h2>
        <p class="section-desc">Comprehensive pathways mapped across all five national curriculum streams.</p>
      </div>

      <div class="grid-3 mt-4">
        <div class="stream-card stream-physical">
          <div class="stream-badge">Physical Science</div>
          <h4>Engineering, AI & Computing</h4>
          <p>Combined Mathematics, Physics, Chemistry, and ICT paths leading to chartered engineering and technology innovation.</p>
        </div>

        <div class="stream-card stream-biological">
          <div class="stream-badge">Biological Science</div>
          <h4>Medicine, Biotech & Agriculture</h4>
          <p>Biology, Chemistry, Physics, and Agriculture tracks targeting clinical medicine, genetics, and sustainable bio-sciences.</p>
        </div>

        <div class="stream-card stream-commerce">
          <div class="stream-badge">Commerce</div>
          <h4>Accounting, Finance & Trade</h4>
          <p>Accounting, Business Studies, and Economics programs empowering future corporate leaders, auditors, and trade strategists.</p>
        </div>

        <div class="stream-card stream-arts">
          <div class="stream-badge">Arts & Humanities</div>
          <h4>Law, Media & Creative Arts</h4>
          <p>Languages, Social Sciences, Law, and Design nurturing advocates, broadcast journalists, and creative visionaries.</p>
        </div>

        <div class="stream-card stream-technology">
          <div class="stream-badge">Technology</div>
          <h4>Engineering Tech & Biosystems</h4>
          <p>Hands-on applied tracks in Engineering Technology (ET), Science for Tech (SFT), and BICT fueling modern industry automation.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero-section {
  padding: 4rem 0 2rem;
  text-align: center;
  max-width: 900px;
  margin: 0 auto;
}

.hero-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.hero-subbadge {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.hero-title {
  font-size: 2.75rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1.2;
  margin-bottom: 1.25rem;
}

.gradient-text {
  background: linear-gradient(135deg, #818cf8 0%, #06b6d4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 1.15rem;
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 2rem;
}

.hero-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-lg {
  padding: 0.9rem 2rem;
  font-size: 1.05rem;
}

.mt-4 { margin-top: 1.5rem; }
.mt-6 { margin-top: 4rem; }
.text-center { text-align: center; }

/* Pipeline */
.pipeline-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.25rem;
}

.pipeline-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  position: relative;
  transition: var(--transition-smooth);
}

.pipeline-card:hover {
  transform: translateY(-4px);
  border-color: rgba(99, 102, 241, 0.4);
}

.pipeline-step-num {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--primary);
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.pipeline-icon {
  font-size: 1.75rem;
  margin-bottom: 0.75rem;
}

.pipeline-card h3 {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.pipeline-card p {
  font-size: 0.825rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* Streams Grid */
.stream-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 1.75rem;
  transition: var(--transition-smooth);
}

.stream-card:hover {
  transform: translateY(-3px);
}

.stream-badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.2rem 0.6rem;
  border-radius: var(--radius-sm);
  margin-bottom: 0.75rem;
}

.stream-physical .stream-badge { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
.stream-biological .stream-badge { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.stream-commerce .stream-badge { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }
.stream-arts .stream-badge { background: rgba(236, 72, 153, 0.15); color: #f472b6; }
.stream-technology .stream-badge { background: rgba(6, 182, 212, 0.15); color: #22d3ee; }

.stream-card h4 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.stream-card p {
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
}
</style>
