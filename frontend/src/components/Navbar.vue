<template>
  <header class="navbar">
    <div class="container navbar-inner">
      <router-link to="/" class="brand">
        <div class="brand-logo">
          <span class="logo-icon">🎓</span>
        </div>
        <div class="brand-text">
          <span class="brand-title">Smart Pathway AI</span>
          <span class="brand-subtitle">Sri Lankan GCE A/L Recommender</span>
        </div>
      </router-link>

      <nav class="nav-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/assessment" class="nav-link">Student Assessment</router-link>
        <router-link to="/dashboard" class="nav-link">Researcher Dashboard</router-link>
      </nav>

      <div class="navbar-actions">
        <span class="badge badge-synthetic">
          <span class="pulse-dot"></span> Mode: Synthetic Dev
        </span>
        <router-link to="/assessment" class="btn btn-primary btn-sm">Start Assessment</router-link>
      </div>
    </div>
  </header>
</template>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(11, 15, 25, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-subtle);
}

.navbar-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 4.5rem;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.brand-logo {
  width: 2.5rem;
  height: 2.5rem;
  background: var(--primary-light);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--text-primary);
  line-height: 1.2;
}

.brand-subtitle {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-link {
  font-weight: 500;
  font-size: 0.9rem;
  color: var(--text-secondary);
  transition: var(--transition-smooth);
  padding: 0.5rem 0.25rem;
  border-bottom: 2px solid transparent;
}

.nav-link:hover, .nav-link.router-link-active {
  color: #ffffff;
  border-bottom-color: var(--primary);
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
}

.pulse-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #fbbf24;
  margin-right: 4px;
}

@media (max-width: 768px) {
  .nav-links {
    display: none;
  }
}
</style>
