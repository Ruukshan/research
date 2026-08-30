<template>
  <footer class="footer">
    <div class="container footer-inner">
      <div class="footer-grid">
        <div class="footer-brand">
          <div class="footer-title">
            <span>🎓</span> Smart Career Pathway Recommendation System (SCPRS)
          </div>
          <p class="footer-desc">
            An Intelligent Decision Support Architecture for Sri Lankan GCE A/L Secondary Students,
            fusing Multi-Class ML Stream Classification, Hybrid Content & Collaborative Filtering, and SHAP Explainability.
          </p>
        </div>

        <div class="footer-links-col">
          <div class="footer-heading">Research Navigation</div>
          <div class="footer-links">
            <router-link to="/">Home Overview</router-link>
            <router-link to="/assessment">Student Intake Wizard</router-link>
            <router-link to="/dashboard">10-Fold CV Dashboard</router-link>
          </div>
        </div>

        <div class="footer-curriculum-col">
          <div class="footer-heading">5 A/L Streams</div>
          <div class="stream-pill-grid">
            <span class="stream-pill pill-physical">Physical Science</span>
            <span class="stream-pill pill-bio">Biological Science</span>
            <span class="stream-pill pill-comm">Commerce</span>
            <span class="stream-pill pill-arts">Arts</span>
            <span class="stream-pill pill-tech">Technology</span>
          </div>
        </div>
      </div>

      <div class="footer-disclaimer-box">
        <div class="disclaimer-header">
          <span class="warning-icon">⚖️</span> Academic Decision Support Notice & Ethics
        </div>
        <p class="disclaimer-text">
          "This system provides AI-assisted career pathway recommendations for educational decision support. 
          It should not replace advice from qualified teachers, counsellors, parents or official university admissions authorities (UGC)."
        </p>
      </div>

      <div class="footer-bottom">
        <span>© 2026 Academic Research Project. KIU Department of Software Engineering.</span>
        <span>Empirical Benchmark Model: <strong>Random Forest & XGBoost</strong> (1,200 Sample Dataset)</span>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  margin-top: 6rem;
  background: #03060d;
  border-top: 1px solid var(--border-subtle);
  padding: 3.5rem 0 2rem;
}

.footer-inner {
  display: flex;
  flex-direction: column;
  gap: 2.25rem;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 3rem;
}

.footer-title {
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: 1.15rem;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.footer-desc {
  font-size: 0.88rem;
  color: var(--text-muted);
  line-height: 1.6;
}

.footer-heading {
  font-family: var(--font-heading);
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-primary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.85rem;
}

.footer-links {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.footer-links a {
  font-size: 0.85rem;
  color: var(--text-secondary);
  transition: var(--transition-smooth);
}

.footer-links a:hover {
  color: var(--primary);
  transform: translateX(3px);
}

.stream-pill-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.stream-pill {
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.pill-physical { color: #60a5fa; border-color: rgba(59, 130, 246, 0.3); }
.pill-bio { color: #34d399; border-color: rgba(16, 185, 129, 0.3); }
.pill-comm { color: #fbbf24; border-color: rgba(245, 158, 11, 0.3); }
.pill-arts { color: #fb7185; border-color: rgba(244, 63, 94, 0.3); }
.pill-tech { color: #22d3ee; border-color: rgba(6, 182, 212, 0.3); }

.footer-disclaimer-box {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(245, 158, 11, 0.03) 100%);
  border: 1px solid rgba(245, 158, 11, 0.22);
  border-radius: var(--radius-md);
  padding: 1.1rem 1.4rem;
}

.disclaimer-header {
  font-family: var(--font-heading);
  font-size: 0.88rem;
  font-weight: 700;
  color: #fbbf24;
  margin-bottom: 0.35rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.disclaimer-text {
  font-size: 0.825rem;
  color: #fde68a;
  line-height: 1.55;
  opacity: 0.9;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.8rem;
  color: var(--text-muted);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  padding-top: 1.5rem;
}

@media (max-width: 850px) {
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}
</style>
