<template>
  <div class="home-view container">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-badge">
        <span class="badge badge-real">
          <span>🎓</span> KIU Software Engineering Research
        </span>
        <span class="hero-subbadge">Sri Lankan GCE A/L Career Intelligence System</span>
      </div>

      <h1 class="hero-title">
        Smart Career Pathway Recommendation System <br />
        <span class="gradient-text">for Advanced Level Students</span>
      </h1>

      <p class="hero-subtitle">
        Empowering Sri Lankan Grade 11–13 students with personalized, ranked, and explainable
        higher-education pathways through multi-class ML classification, hybrid score fusion, and SHAP explainability.
      </p>

      <div class="hero-actions">
        <router-link to="/assessment" class="btn btn-primary btn-lg">
          Begin Student Assessment ➔
        </router-link>
        <router-link to="/dashboard" class="btn btn-secondary btn-lg">
          Explore Research Dashboard
        </router-link>
      </div>

      <div class="disclaimer-banner mt-4">
        <span>⚖️</span>
        <p>
          <strong>Academic Decision Support:</strong> This system provides AI-assisted recommendations. It is designed to complement,
          not replace, guidance from teachers, career counsellors, parents, and official university admission handbooks.
        </p>
      </div>
    </section>

    <!-- Research Methodology & Pipeline Section -->
    <section class="pipeline-section mt-8">
      <div class="section-header text-center">
        <h2 class="section-title">Core Research Contribution</h2>
        <p class="section-desc">A five-tier hybrid architecture connecting student aptitude to higher education and occupational outcomes.</p>
      </div>

      <div class="pipeline-grid mt-6">
        <div class="pipeline-card glass-card">
          <div class="pipeline-step-num">01</div>
          <div class="pipeline-icon">📝</div>
          <h3>Student Profile Intake</h3>
          <p>Captures GCE O/L grades, basket electives, extracurricular leadership, and 6 Holland RIASEC personality traits.</p>
        </div>

        <div class="pipeline-card glass-card">
          <div class="pipeline-step-num">02</div>
          <div class="pipeline-icon">🧠</div>
          <h3>ML Stream Classifier</h3>
          <p>Multi-class probabilistic model comparing Random Forest, XGBoost, and Deep Neural Networks across 5 A/L streams.</p>
        </div>

        <div class="pipeline-card glass-card">
          <div class="pipeline-step-num">03</div>
          <div class="pipeline-icon">⚙️</div>
          <h3>Hybrid Score Fusion</h3>
          <p>Blends ML Stream Probability + Content-Based Pathway Similarity + Collaborative User Filtering with configurable weights.</p>
        </div>

        <div class="pipeline-card glass-card">
          <div class="pipeline-step-num">04</div>
          <div class="pipeline-icon">🏆</div>
          <h3>Ranked Top-5 Pathways</h3>
          <p>Delivers diverse, highly relevant Sri Lankan state university degrees, professional paths, and emerging careers.</p>
        </div>

        <div class="pipeline-card glass-card">
          <div class="pipeline-step-num">05</div>
          <div class="pipeline-icon">🔍</div>
          <h3>SHAP Explainability</h3>
          <p>Transparent feature attribution revealing positive and negative drivers behind individual predictions.</p>
        </div>
      </div>
    </section>

    <!-- Five A/L Streams Grid -->
    <section class="streams-section mt-8">
      <div class="section-header">
        <h2 class="section-title">Supported Sri Lankan A/L Streams</h2>
        <p class="section-desc">Comprehensive pathways mapped across all five national curriculum streams.</p>
      </div>

      <div class="streams-grid mt-6">
        <div class="stream-card glass-card stream-physical">
          <div class="stream-header">
            <span class="stream-badge">Physical Science (Maths)</span>
            <span class="stream-code">Stream 01</span>
          </div>
          <h4>Engineering, AI & Computing</h4>
          <p>Combined Mathematics, Physics, Chemistry, and ICT paths leading to chartered engineering and technology innovation.</p>
          <div class="stream-chips">
            <span>Software Eng</span>
            <span>Civil Eng</span>
            <span>Data Science</span>
          </div>
        </div>

        <div class="stream-card glass-card stream-biological">
          <div class="stream-header">
            <span class="stream-badge">Biological Science</span>
            <span class="stream-code">Stream 02</span>
          </div>
          <h4>Medicine, Biotech & Agriculture</h4>
          <p>Biology, Chemistry, Physics, and Agriculture tracks targeting clinical medicine, genetics, and sustainable bio-sciences.</p>
          <div class="stream-chips">
            <span>MBBS / Medicine</span>
            <span>Genetics</span>
            <span>Biomedical</span>
          </div>
        </div>

        <div class="stream-card glass-card stream-commerce">
          <div class="stream-header">
            <span class="stream-badge">Commerce</span>
            <span class="stream-code">Stream 03</span>
          </div>
          <h4>Accounting, Finance & Trade</h4>
          <p>Accounting, Business Studies, and Economics programs empowering future corporate leaders, auditors, and trade strategists.</p>
          <div class="stream-chips">
            <span>CA / CIMA</span>
            <span>Investment</span>
            <span>FinTech</span>
          </div>
        </div>

        <div class="stream-card glass-card stream-arts">
          <div class="stream-header">
            <span class="stream-badge">Arts & Humanities</span>
            <span class="stream-code">Stream 04</span>
          </div>
          <h4>Law, Media & Creative Arts</h4>
          <p>Languages, Social Sciences, Law, and Design nurturing advocates, broadcast journalists, and creative visionaries.</p>
          <div class="stream-chips">
            <span>LLB Law</span>
            <span>Mass Media</span>
            <span>UX Design</span>
          </div>
        </div>

        <div class="stream-card glass-card stream-technology">
          <div class="stream-header">
            <span class="stream-badge">Technology Stream</span>
            <span class="stream-code">Stream 05</span>
          </div>
          <h4>Engineering Tech & Biosystems</h4>
          <p>Hands-on applied tracks in Engineering Technology (ET), Science for Tech (SFT), and BICT fueling modern industry automation.</p>
          <div class="stream-chips">
            <span>Robotics Tech</span>
            <span>Food Tech</span>
            <span>Cybersecurity</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero-section {
  padding: 4.5rem 0 2rem;
  text-align: center;
  max-width: 920px;
  margin: 0 auto;
}

.hero-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.hero-subbadge {
  font-family: var(--font-heading);
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 600;
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.15;
  margin-bottom: 1.35rem;
}

.hero-subtitle {
  font-size: 1.15rem;
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 2.25rem;
}

.hero-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.25rem;
  flex-wrap: wrap;
}

.btn-lg {
  padding: 0.95rem 2.2rem;
  font-size: 1.05rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 0.4rem;
}

.section-desc {
  color: var(--text-secondary);
  font-size: 1rem;
}

/* Pipeline */
.pipeline-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 1.25rem;
}

.pipeline-card {
  padding: 1.75rem 1.4rem;
  position: relative;
  transition: var(--transition-smooth);
}

.pipeline-card:hover {
  transform: translateY(-5px);
  border-color: rgba(59, 130, 246, 0.4);
  box-shadow: var(--shadow-glow-blue);
}

.pipeline-step-num {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--primary);
  font-weight: 800;
  margin-bottom: 0.6rem;
  letter-spacing: 0.05em;
}

.pipeline-icon {
  font-size: 2rem;
  margin-bottom: 0.85rem;
}

.pipeline-card h3 {
  font-size: 1.05rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.pipeline-card p {
  font-size: 0.84rem;
  color: var(--text-secondary);
  line-height: 1.55;
}

/* Streams Grid */
.streams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.stream-card {
  padding: 1.85rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-left: 4px solid var(--border-subtle);
  transition: var(--transition-smooth);
}

.stream-card:hover {
  transform: translateY(-4px);
}

.stream-physical { border-left-color: var(--stream-physical); }
.stream-physical:hover { box-shadow: var(--shadow-glow-blue); }

.stream-biological { border-left-color: var(--stream-biological); }
.stream-biological:hover { box-shadow: var(--shadow-glow-emerald); }

.stream-commerce { border-left-color: var(--stream-commerce); }
.stream-commerce:hover { box-shadow: 0 0 30px rgba(245, 158, 11, 0.22); }

.stream-arts { border-left-color: var(--stream-arts); }
.stream-arts:hover { box-shadow: 0 0 30px rgba(244, 63, 94, 0.22); }

.stream-technology { border-left-color: var(--stream-technology); }
.stream-technology:hover { box-shadow: var(--shadow-glow-cyan); }

.stream-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.85rem;
}

.stream-badge {
  font-family: var(--font-heading);
  font-size: 0.78rem;
  font-weight: 700;
  padding: 0.25rem 0.7rem;
  border-radius: var(--radius-sm);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.stream-physical .stream-badge { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
.stream-biological .stream-badge { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.stream-commerce .stream-badge { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }
.stream-arts .stream-badge { background: rgba(244, 63, 94, 0.15); color: #fb7185; }
.stream-technology .stream-badge { background: rgba(6, 182, 212, 0.15); color: #22d3ee; }

.stream-code {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--text-muted);
}

.stream-card h4 {
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.stream-card p {
  font-size: 0.88rem;
  color: var(--text-secondary);
  line-height: 1.55;
  margin-bottom: 1.25rem;
}

.stream-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.stream-chips span {
  font-family: var(--font-heading);
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-secondary);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.2rem;
  }
}
</style>
