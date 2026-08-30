<template>
  <footer class="footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <div class="footer-title">Smart Career Pathway Recommendation System</div>
        <p class="footer-desc">
          Final-Year Undergraduate Research Project on ML-Driven Educational Decision Support for Sri Lankan GCE A/L Students.
        </p>
      </div>

      <div class="footer-disclaimer-box">
        <div class="disclaimer-header">
          <span class="warning-icon">⚖️</span> Academic Decision Support Notice
        </div>
        <p class="disclaimer-text">
          "This system provides AI-assisted career pathway recommendations for educational decision support. 
          It should not replace advice from qualified teachers, counsellors, parents or career guidance professionals."
        </p>
      </div>

      <div class="footer-bottom">
        <span>© 2026 Academic Research Project. Developed for Sri Lankan Secondary Education Decision Support.</span>
        <span>Data Mode: <strong>Synthetic Development Dataset</strong> (v1.0)</span>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  margin-top: 5rem;
  background: #070a12;
  border-top: 1px solid var(--border-subtle);
  padding: 3rem 0 2rem;
}

.footer-inner {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.footer-title {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.footer-desc {
  font-size: 0.875rem;
  color: var(--text-muted);
  max-width: 600px;
}

.footer-disclaimer-box {
  background: rgba(245, 158, 11, 0.05);
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-radius: var(--radius-md);
  padding: 1rem 1.25rem;
}

.disclaimer-header {
  font-size: 0.85rem;
  font-weight: 700;
  color: #fbbf24;
  margin-bottom: 0.35rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.disclaimer-text {
  font-size: 0.825rem;
  color: var(--text-secondary);
  line-height: 1.5;
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
</style>
