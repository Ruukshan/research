<template>
  <div class="results-view container">
    <!-- Header -->
    <div class="results-header">
      <div class="header-badge">
        <span class="badge badge-real">{{ result?.model_name || 'Empirical Best Model' }}</span>
        <span class="badge badge-synthetic">Data Mode: Real Survey + Augmented</span>
        <span class="badge badge-real">Hybrid Fusion Engine</span>
      </div>
      <h1 class="page-title">Personalized Career Pathway Results</h1>
      <p class="page-desc">AI-assisted recommendations based on your academic profile, RIASEC dimensions, and career aspirations.</p>
    </div>

    <!-- Disclaimer Banner -->
    <div class="disclaimer-banner mt-4">
      <span>⚖️</span>
      <p>{{ result?.disclaimer || 'Educational decision support only. Recommendations do not replace qualified counselling.' }}</p>
    </div>

    <!-- Section 1: Stream Probabilities -->
    <section class="probabilities-section mt-6">
      <h2 class="section-heading">1. Predicted A/L Stream Probabilities</h2>
      <p class="section-subtext">Estimated alignment across the five Sri Lankan GCE A/L subject streams.</p>

      <div class="probabilities-grid mt-4">
        <div 
          v-for="(prob, streamName) in result?.stream_probabilities" 
          :key="streamName"
          class="prob-card"
          :class="{ 'prob-winner': streamName === result?.predicted_stream }"
        >
          <div class="prob-header">
            <span class="stream-name">{{ streamName }}</span>
            <span class="prob-pct">{{ (prob * 100).toFixed(1) }}%</span>
          </div>
          <div class="prob-bar-track">
            <div 
              class="prob-bar-fill" 
              :class="getStreamClass(streamName)" 
              :style="{ width: `${prob * 100}%` }"
            ></div>
          </div>
          <span v-if="streamName === result?.predicted_stream" class="winner-tag">★ Highest Alignment</span>
        </div>
      </div>
    </section>

    <!-- Section 2: Top-5 Career Pathways -->
    <section class="pathways-section mt-6">
      <h2 class="section-heading">2. Ranked Top-5 Career Pathways</h2>
      <p class="section-subtext">Fused recommendations combining ML Stream Confidence + Pathway Alignment + Historical Similarities.</p>

      <div class="pathways-list mt-4">
        <div 
          v-for="rec in result?.recommendations" 
          :key="rec.rank"
          class="pathway-card glass-card"
        >
          <div class="pathway-rank-badge">
            #{{ rec.rank }}
          </div>

          <div class="pathway-main-info">
            <div class="pathway-meta">
              <span class="stream-tag" :class="getStreamClass(rec.stream)">{{ rec.stream }}</span>
              <span class="compatibility-tag">{{ rec.compatibility_level }}</span>
            </div>

            <h3 class="degree-title">{{ rec.degree_program }}</h3>
            <div class="career-domain-text">Career Domain: <strong>{{ rec.career_domain }}</strong></div>

            <p class="pathway-explanation mt-2">
              💡 <em>{{ rec.explanation }}</em>
            </p>

            <div v-if="rec.sample_job_titles && rec.sample_job_titles.length" class="jobs-row mt-2">
              <span class="jobs-label">Sample Roles:</span>
              <span v-for="job in rec.sample_job_titles" :key="job" class="job-chip">{{ job }}</span>
            </div>
          </div>

          <div class="pathway-score-box">
            <div class="score-num">{{ (rec.score * 100).toFixed(1) }}%</div>
            <div class="score-label">Match Score</div>
            <div class="score-breakdown">
              <span>ML: {{ (rec.ml_stream_score * 100).toFixed(0) }}%</span>
              <span>Content: {{ (rec.content_similarity_score * 100).toFixed(0) }}%</span>
              <span>Collab: {{ (rec.collaborative_score * 100).toFixed(0) }}%</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 3: SHAP Explainability -->
    <section class="shap-section mt-6">
      <div class="section-header">
        <div class="flex-between">
          <div>
            <h2 class="section-heading">3. Explainable AI (SHAP Insights)</h2>
            <p class="section-subtext">Understanding which factors positively or negatively influenced your prediction.</p>
          </div>
          <button @click="showTechnicalShap = !showTechnicalShap" class="btn btn-outline btn-sm">
            {{ showTechnicalShap ? '▲ Hide Technical Details' : '▼ Technical Details & Waterfall' }}
          </button>
        </div>
      </div>

      <div class="glass-card mt-4 shap-card">
        <h3 class="shap-title">Why {{ result?.predicted_stream }} was predicted</h3>

        <div class="shap-factors-grid mt-4">
          <div class="factors-column">
            <h4 class="factor-heading positive-heading">▲ Key Supporting Factors (+ SHAP Contribution)</h4>
            <ul class="factors-list">
              <li v-for="(factor, idx) in result?.shap_explanation?.top_positive" :key="idx" class="factor-item positive-item">
                <span class="factor-icon">+</span>
                <span>{{ factor }}</span>
              </li>
              <li v-if="!result?.shap_explanation?.top_positive?.length" class="factor-item positive-item">
                <span class="factor-icon">+</span>
                <span>Strong aptitude in core analytical & domain subjects</span>
              </li>
            </ul>
          </div>

          <div class="factors-column">
            <h4 class="factor-heading negative-heading">▼ Dampening Factors (- SHAP Contribution)</h4>
            <ul class="factors-list">
              <li v-for="(factor, idx) in result?.shap_explanation?.top_negative" :key="idx" class="factor-item negative-item">
                <span class="factor-icon">-</span>
                <span>{{ factor }}</span>
              </li>
              <li v-if="!result?.shap_explanation?.top_negative?.length" class="factor-item negative-item">
                <span class="factor-icon">-</span>
                <span>Lower orientation toward non-selected subject domains</span>
              </li>
            </ul>
          </div>
        </div>

        <!-- Technical Waterfall Plot Section -->
        <div v-if="showTechnicalShap" class="technical-shap-box mt-4">
          <h4 class="technical-title">Technical SHAP Attribution Waterfall</h4>
          <p class="technical-desc">
            Visualizing cumulative positive (red) and negative (blue) log-odds contributions from the baseline model expected value.
          </p>
          <div class="waterfall-img-wrapper mt-2">
            <img :src="'/static/results/shap_waterfall.png'" alt="SHAP Waterfall" class="waterfall-img" />
          </div>
        </div>
      </div>
    </section>

    <!-- Actions -->
    <div class="results-actions mt-6 text-center">
      <router-link to="/assessment" class="btn btn-secondary">
        🔄 Re-Take Assessment
      </router-link>
      <router-link to="/dashboard" class="btn btn-primary">
        📊 View Researcher Dashboard
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAssessmentStore } from '../stores/assessmentStore'

const store = useAssessmentStore()
const showTechnicalShap = ref(false)

const result = computed(() => {
  if (store.assessmentResult) {
    return store.assessmentResult
  }
  return {
    record_id: 'STU-SYN-DEMO',
    student_id: 'demo-id',
    data_source: 'synthetic',
    predicted_stream: 'Physical Science',
    stream_probabilities: {
      'Physical Science': 0.62,
      'Technology': 0.21,
      'Commerce': 0.08,
      'Biological Science': 0.06,
      'Arts': 0.03,
    },
    recommendations: [
      {
        rank: 1,
        pathway_id: 'PATH_PS_002',
        stream: 'Physical Science',
        degree_area: 'Computing & Informatics',
        degree_program: 'B.Sc. (Hons) in Computer Science / Software Engineering',
        career_domain: 'Software Architecture & AI Engineering',
        score: 0.88,
        ml_stream_score: 0.62,
        content_similarity_score: 0.92,
        collaborative_score: 0.65,
        compatibility_level: 'High Match',
        explanation: 'Top ranked due to high aptitude in Mathematics & Science combined with strong RIASEC Investigative score.',
        sample_job_titles: ['Software Engineer', 'Machine Learning Engineer', 'Cloud Architect'],
      },
      {
        rank: 2,
        pathway_id: 'PATH_PS_001',
        stream: 'Physical Science',
        degree_area: 'Engineering & Technology',
        degree_program: 'B.Sc. (Eng.) in Civil / Mechanical / Electrical Engineering',
        career_domain: 'Engineering Infrastructure & Operations',
        score: 0.84,
        ml_stream_score: 0.62,
        content_similarity_score: 0.88,
        collaborative_score: 0.60,
        compatibility_level: 'High Match',
        explanation: 'High mathematical foundation aligns directly with state university engineering faculties.',
        sample_job_titles: ['Civil Engineer', 'Mechanical Engineer', 'Project Consultant'],
      },
      {
        rank: 3,
        pathway_id: 'PATH_TECH_002',
        stream: 'Technology',
        degree_area: 'Information & Communication Technology (BICT)',
        degree_program: 'Bachelor of Information & Communication Technology (BICT Hons)',
        career_domain: 'Applied Software, Network Engineering & Cloud Tech',
        score: 0.72,
        ml_stream_score: 0.21,
        content_similarity_score: 0.89,
        collaborative_score: 0.55,
        compatibility_level: 'Moderate Match',
        explanation: 'Cross-stream high-tech pathway leveraging your practical coding and IT interests.',
        sample_job_titles: ['Network Engineer', 'DevOps Associate', 'Database Admin'],
      },
      {
        rank: 4,
        pathway_id: 'PATH_PS_003',
        stream: 'Physical Science',
        degree_area: 'Data Science & Mathematics',
        degree_program: 'B.Sc. (Hons) in Data Science & Artificial Intelligence / Statistics',
        career_domain: 'Data Analytics & Quantitative Research',
        score: 0.70,
        ml_stream_score: 0.62,
        content_similarity_score: 0.75,
        collaborative_score: 0.58,
        compatibility_level: 'Moderate Match',
        explanation: 'Quantitative analytics track with strong demand in tech and banking sectors.',
        sample_job_titles: ['Data Scientist', 'Quantitative Analyst'],
      },
      {
        rank: 5,
        pathway_id: 'PATH_TECH_001',
        stream: 'Technology',
        degree_area: 'Engineering Technology & Robotics',
        degree_program: 'Bachelor of Technology (B.Tech) in Mechatronics',
        career_domain: 'Applied Engineering & Industrial Automation',
        score: 0.65,
        ml_stream_score: 0.21,
        content_similarity_score: 0.82,
        collaborative_score: 0.50,
        compatibility_level: 'Exploratory Match',
        explanation: 'Applied robotics track combining hands-on mechanics and microcontroller programming.',
        sample_job_titles: ['Automation Specialist', 'Mechatronics Technologist'],
      },
    ],
    shap_explanation: {
      top_positive: [
        'O/L Mathematics Grade strongly supported this stream (+0.28)',
        'Investigative Personality (RIASEC) increased suitability (+0.19)',
        'Coding & Robotics Club Experience boosted score (+0.14)',
      ],
      top_negative: [
        'Lower score for Biological Science electives (-0.22)',
        'Lower score for Conventional accounting focus (-0.15)',
      ],
    },
    disclaimer: 'This system provides AI-assisted career pathway recommendations for educational decision support. It should not replace advice from qualified teachers, counsellors, parents or career guidance professionals.',
  }
})

const getStreamClass = (streamName: string) => {
  switch (streamName) {
    case 'Physical Science': return 'fill-physical'
    case 'Biological Science': return 'fill-bio'
    case 'Commerce': return 'fill-commerce'
    case 'Arts': return 'fill-arts'
    case 'Technology': return 'fill-tech'
    default: return ''
  }
}
</script>

<style scoped>
.results-view {
  padding: 2rem 0;
}

.results-header {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.header-badge {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.page-title {
  font-size: 2.25rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.page-desc {
  color: var(--text-secondary);
}

.section-heading {
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.section-subtext {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

/* Probabilities Grid */
.probabilities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.prob-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 1.4rem;
  position: relative;
  transition: var(--transition-smooth);
}

.prob-winner {
  border-color: var(--primary);
  box-shadow: var(--shadow-glow-blue);
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.12) 0%, rgba(11, 17, 32, 0.9) 100%);
}

.prob-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.6rem;
}

.stream-name {
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: 0.95rem;
}

.prob-pct {
  font-family: var(--font-mono);
  font-weight: 800;
  font-size: 1.2rem;
  color: var(--text-primary);
}

.prob-bar-track {
  width: 100%;
  height: 9px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.prob-bar-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

.fill-physical { background: var(--gradient-physical); }
.fill-bio { background: var(--gradient-biological); }
.fill-commerce { background: var(--gradient-commerce); }
.fill-arts { background: var(--gradient-arts); }
.fill-tech { background: var(--gradient-technology); }

.winner-tag {
  display: inline-block;
  margin-top: 0.6rem;
  font-family: var(--font-heading);
  font-size: 0.78rem;
  color: #60a5fa;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

/* Pathways Cards */
.pathways-list {
  display: flex;
  flex-direction: column;
  gap: 1.35rem;
}

.pathway-card {
  display: flex;
  align-items: center;
  gap: 1.75rem;
  padding: 1.75rem;
  border-left: 4px solid rgba(59, 130, 246, 0.4);
}

.pathway-rank-badge {
  font-family: var(--font-heading);
  font-size: 1.6rem;
  font-weight: 900;
  color: #ffffff;
  width: 3.8rem;
  height: 3.8rem;
  background: var(--primary-gradient);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
}

.pathway-main-info {
  flex: 1;
}

.pathway-meta {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.4rem;
}

.stream-tag {
  font-family: var(--font-heading);
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.2rem 0.65rem;
  border-radius: var(--radius-sm);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.stream-tag.fill-physical { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
.stream-tag.fill-bio { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.stream-tag.fill-commerce { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }
.stream-tag.fill-arts { background: rgba(244, 63, 94, 0.15); color: #fb7185; }
.stream-tag.fill-tech { background: rgba(6, 182, 212, 0.15); color: #22d3ee; }

.compatibility-tag {
  font-family: var(--font-heading);
  font-size: 0.75rem;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.06);
  padding: 0.2rem 0.6rem;
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  border: 1px solid var(--border-subtle);
}

.degree-title {
  font-size: 1.25rem;
  font-weight: 800;
  margin-bottom: 0.25rem;
  color: var(--text-primary);
}

.career-domain-text {
  font-size: 0.88rem;
  color: var(--text-secondary);
}

.pathway-explanation {
  font-size: 0.86rem;
  color: var(--text-secondary);
  line-height: 1.5;
}

.jobs-row {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  flex-wrap: wrap;
}

.jobs-label {
  font-family: var(--font-heading);
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--text-muted);
}

.job-chip {
  font-size: 0.76rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-subtle);
  padding: 0.15rem 0.55rem;
  border-radius: 4px;
  color: var(--text-secondary);
}

.pathway-score-box {
  text-align: right;
  min-width: 120px;
  background: rgba(0, 0, 0, 0.25);
  padding: 0.85rem 1rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-subtle);
}

.score-num {
  font-family: var(--font-mono);
  font-size: 1.85rem;
  font-weight: 900;
  color: #38bdf8;
  text-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
}

.score-label {
  font-family: var(--font-heading);
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.score-breakdown {
  display: flex;
  flex-direction: column;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--text-muted);
  margin-top: 0.35rem;
  gap: 0.1rem;
}

/* SHAP Card */
.shap-card {
  padding: 1.85rem;
}

.shap-title {
  font-size: 1.15rem;
  font-weight: 800;
}

.shap-factors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
}

.factors-column {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 1.4rem;
}

.factor-heading {
  font-family: var(--font-heading);
  font-size: 0.92rem;
  font-weight: 800;
  margin-bottom: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.positive-heading { color: #34d399; }
.negative-heading { color: #f87171; }

.factors-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.factor-item {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  font-size: 0.86rem;
  line-height: 1.45;
}

.positive-item .factor-icon { color: #34d399; font-weight: 800; }
.negative-item .factor-icon { color: #f87171; font-weight: 800; }

.technical-shap-box {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 1.4rem;
}

.technical-title {
  font-size: 1rem;
  font-weight: 800;
  margin-bottom: 0.25rem;
}

.technical-desc {
  font-size: 0.84rem;
  color: var(--text-secondary);
}

.waterfall-img-wrapper {
  display: flex;
  justify-content: center;
  background: #090e1c;
  border-radius: var(--radius-sm);
  padding: 1rem;
  border: 1px solid var(--border-subtle);
}

.waterfall-img {
  max-width: 100%;
  height: auto;
  border-radius: var(--radius-sm);
}

.results-actions {
  display: flex;
  justify-content: center;
  gap: 1.25rem;
  flex-wrap: wrap;
}

.mt-2 { margin-top: 0.5rem; }
.mt-4 { margin-top: 1.5rem; }
.mt-6 { margin-top: 3rem; }
.text-center { text-align: center; }

@media (max-width: 768px) {
  .pathway-card {
    flex-direction: column;
    align-items: flex-start;
  }
  .pathway-score-box {
    text-align: left;
    width: 100%;
  }
}
</style>
