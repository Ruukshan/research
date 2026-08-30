<template>
  <header class="navbar">
    <div class="container navbar-inner">
      <router-link to="/" class="brand">
        <div class="brand-logo">
          <span class="logo-icon">🎓</span>
        </div>
        <div class="brand-text">
          <span class="brand-title">SCPRS <span class="brand-tag">AI</span></span>
          <span class="brand-subtitle">Sri Lankan GCE A/L Career Recommender</span>
        </div>
      </router-link>

      <nav class="nav-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/assessment" class="nav-link">Student Assessment</router-link>
        <router-link to="/dashboard" class="nav-link">Research Dashboard</router-link>
      </nav>

      <div class="navbar-actions">
        <span class="badge badge-real">
          <span class="pulse-dot"></span> Real Survey Trained
        </span>
        <router-link to="/assessment" class="btn btn-primary btn-sm">Take Assessment ➔</router-link>
      </div>
    </div>
  </header>
</template>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(5, 8, 17, 0.82);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border-subtle);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
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
  gap: 0.85rem;
}

.brand-logo {
  width: 2.6rem;
  height: 2.6rem;
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.25) 0%, rgba(6, 182, 212, 0.2) 100%);
  border: 1px solid rgba(59, 130, 246, 0.4);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  box-shadow: 0 0 15px rgba(37, 99, 235, 0.3);
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-family: var(--font-heading);
  font-weight: 800;
  font-size: 1.15rem;
  color: var(--text-primary);
  line-height: 1.2;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.brand-tag {
  background: var(--primary-gradient);
  color: #fff;
  font-size: 0.65rem;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  font-weight: 800;
}

.brand-subtitle {
  font-size: 0.72rem;
  color: var(--text-muted);
  font-weight: 500;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.8rem;
}

.nav-link {
  font-family: var(--font-heading);
  font-weight: 600;
  font-size: 0.92rem;
  color: var(--text-secondary);
  transition: var(--transition-smooth);
  padding: 0.5rem 0.2rem;
  position: relative;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--primary-gradient);
  transition: width 0.25s ease;
  border-radius: 2px;
}

.nav-link:hover, .nav-link.router-link-active {
  color: #ffffff;
}

.nav-link:hover::after, .nav-link.router-link-active::after {
  width: 100%;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 1.1rem;
}

.btn-sm {
  padding: 0.55rem 1.15rem;
  font-size: 0.85rem;
}

.pulse-dot {
  display: inline-block;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background-color: #34d399;
  box-shadow: 0 0 8px #34d399;
  margin-right: 4px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(0.95); opacity: 0.8; }
  50% { transform: scale(1.3); opacity: 1; }
  100% { transform: scale(0.95); opacity: 0.8; }
}

@media (max-width: 768px) {
  .nav-links {
    display: none;
  }
}
</style>
