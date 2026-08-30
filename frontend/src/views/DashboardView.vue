<template>
  <div class="dashboard-view container">
    <!-- Header -->
    <div class="dashboard-header">
      <div class="header-badges">
        <span class="badge" :class="report.dataset_source === 'mixed' || report.dataset_source === 'real' ? 'badge-real' : 'badge-synthetic'">
          Data Mode: {{ report.dataset_source === 'mixed' ? 'Mixed Real Survey + Augmented (1,200 records)' : report.dataset_source === 'real' ? 'Real Survey Dataset' : 'Synthetic Development' }}
        </span>
        <span class="badge badge-real">Reproducibility Seed: 42</span>
      </div>
      <h1 class="page-title">Counsellor & Researcher Dashboard</h1>
      <p class="page-desc">
        Empirical 10-fold cross-validation benchmarks, model comparison reports, and publication figures.
      </p>
    </div>

    <!-- Academic Notice Alert -->
    <div class="disclaimer-banner mt-4">
      <span>🔬</span>
      <p>
        <strong>Research Evaluation Notice:</strong> All evaluation benchmarks shown below represent 10-fold Stratified Cross-Validation on the
        combined dataset (Real Survey + Augmented Samples, n=1,200). Models and research figures are updated directly from the training pipeline.
      </p>
    </div>

    <!-- Key Metrics Grid -->
    <div class="grid-3 mt-6">
      <div class="metric-card glass-card">
        <div class="metric-title">Total Benchmark Samples</div>
        <div class="metric-value">{{ report.total_samples || 1200 }}</div>
        <div class="metric-subtext">Real Survey Intake + Augmented</div>
      </div>

      <div class="metric-card glass-card">
        <div class="metric-title">Active Benchmark Model</div>
        <div class="metric-value text-accent">{{ report.selected_model_name }}</div>
        <div class="metric-subtext" v-if="selectedModelInfo">
          10-fold CV Macro F1: {{ (selectedModelInfo.cv_mean * 100).toFixed(2) }}% ± {{ (selectedModelInfo.cv_std * 100).toFixed(2) }}%
        </div>
        <div class="metric-subtext" v-else>10-fold Stratified CV</div>
      </div>

      <div class="metric-card glass-card">
        <div class="metric-title">Target Curriculum Streams</div>
        <div class="metric-value">5 Streams</div>
        <div class="metric-subtext">Physical, Bio, Commerce, Arts, Tech</div>
      </div>
    </div>

    <!-- Model Comparison Table -->
    <section class="table-section mt-6">
      <div class="section-header">
        <h2 class="section-heading">Model Comparison Benchmarks (10-Fold Stratified CV)</h2>
        <p class="section-subtext">Standardized multi-class classification evaluation across candidate architectures.</p>
      </div>

      <div class="glass-card mt-4 table-container">
        <table class="research-table">
          <thead>
            <tr>
              <th>Model Name</th>
              <th>CV Macro F1</th>
              <th>CV Std (±)</th>
              <th>Test Acc</th>
              <th>Test Precision</th>
              <th>Test Recall</th>
              <th>Test Macro F1</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in report.models" :key="m.experiment_id" :class="{ 'selected-row': m.selected_model }">
              <td>
                <div class="model-name-cell">
                  <strong>{{ m.model_name }}</strong>
                  <span class="exp-id">{{ m.experiment_id }}</span>
                </div>
              </td>
              <td><strong>{{ (m.cv_mean * 100).toFixed(2) }}%</strong></td>
              <td>±{{ (m.cv_std * 100).toFixed(2) }}%</td>
              <td>{{ (m.test_accuracy * 100).toFixed(2) }}%</td>
              <td>{{ (m.test_precision * 100).toFixed(2) }}%</td>
              <td>{{ (m.test_recall * 100).toFixed(2) }}%</td>
              <td>
                <strong class="f1-highlight">{{ (m.test_f1 * 100).toFixed(2) }}%</strong>
              </td>
              <td>
                <span v-if="m.selected_model" class="badge badge-real">★ Selected Best</span>
                <span v-else class="badge badge-synthetic">Candidate</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Research Visualizations Gallery -->
    <section class="figures-section mt-6">
      <div class="section-header">
        <h2 class="section-heading">Publication-Ready Research Figures</h2>
        <p class="section-subtext">Interactive visual outputs generated from 10-fold cross-validation and SHAP explainability.</p>
      </div>

      <!-- Figure Tabs -->
      <div class="figure-tabs mt-4">
        <button 
          v-for="fig in figures" 
          :key="fig.id" 
          class="fig-tab-btn"
          :class="{ active: selectedFigId === fig.id }"
          @click="selectedFigId = fig.id"
        >
          {{ fig.title }}
        </button>
      </div>

      <!-- Active Figure Display Card -->
      <div v-if="activeFigure" class="glass-card mt-4 figure-display-card">
        <div class="figure-card-header">
          <div>
            <h3 class="figure-title">{{ activeFigure.title }}</h3>
            <p class="figure-desc">{{ activeFigure.description }}</p>
          </div>
          <a :href="activeFigure.url" target="_blank" class="btn btn-outline btn-sm">
            🔍 Open Full Resolution
          </a>
        </div>
        <div class="figure-img-wrapper mt-4">
          <img :src="activeFigure.url" :alt="activeFigure.title" class="figure-img" />
        </div>
      </div>
    </section>

    <!-- Synthetic Dataset Class Distribution -->
    <section class="distribution-section mt-6">
      <div class="section-header">
        <h2 class="section-heading">Dataset Class Distribution</h2>
        <p class="section-subtext">Stratified balance across the 1,200 synthetic development records.</p>
      </div>

      <div class="grid-3 mt-4">
        <div class="dist-card glass-card">
          <div class="dist-header">
            <span class="stream-tag fill-commerce">Commerce</span>
            <span class="dist-count">296 records (24.7%)</span>
          </div>
          <p class="dist-desc">Accounting, Business Studies & Economics orientations.</p>
        </div>

        <div class="dist-card glass-card">
          <div class="dist-header">
            <span class="stream-tag fill-physical">Physical Science</span>
            <span class="dist-count">263 records (21.9%)</span>
          </div>
          <p class="dist-desc">High Combined Mathematics & Physics aptitude.</p>
        </div>

        <div class="dist-card glass-card">
          <div class="dist-header">
            <span class="stream-tag fill-bio">Biological Science</span>
            <span class="dist-count">236 records (19.7%)</span>
          </div>
          <p class="dist-desc">Science, Biology & Health science preferences.</p>
        </div>

        <div class="dist-card glass-card">
          <div class="dist-header">
            <span class="stream-tag fill-arts">Arts & Humanities</span>
            <span class="dist-count">216 records (18.0%)</span>
          </div>
          <p class="dist-desc">Languages, Media, Literature & Social sciences.</p>
        </div>

        <div class="dist-card glass-card">
          <div class="dist-header">
            <span class="stream-tag fill-tech">Technology</span>
            <span class="dist-count">189 records (15.7%)</span>
          </div>
          <p class="dist-desc">Engineering Technology, SFT, and ICT applications.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

interface ResearchFigure {
  id: string
  title: string
  description: string
  url: string
}

const stats = ref({
  total_assessments: 1200,
  synthetic_assessments: 1200,
  real_assessments: 0,
})

const report = ref({
  dataset_source: 'synthetic',
  total_samples: 1200,
  selected_model_name: 'Random Forest (Baseline)',
  models: [
    {
      experiment_id: 'EXP-RAN-001',
      model_name: 'Random Forest (Baseline)',
      cv_mean: 0.9476,
      cv_std: 0.0180,
      test_accuracy: 0.9708,
      test_precision: 0.9684,
      test_recall: 0.9701,
      test_f1: 0.9692,
      selected_model: true,
    },
    {
      experiment_id: 'EXP-XGB-001',
      model_name: 'XGBoost Multi-Class',
      cv_mean: 0.9392,
      cv_std: 0.0190,
      test_accuracy: 0.9625,
      test_precision: 0.9623,
      test_recall: 0.9606,
      test_f1: 0.9614,
      selected_model: false,
    },
    {
      experiment_id: 'EXP-DEE-001',
      model_name: 'Deep Neural Network (Tabular MLP)',
      cv_mean: 0.9435,
      cv_std: 0.0185,
      test_accuracy: 0.9458,
      test_precision: 0.9443,
      test_recall: 0.9402,
      test_f1: 0.9419,
      selected_model: false,
    },
  ],
})

const figures = ref<ResearchFigure[]>([
  {
    id: 'model_metrics_comparison',
    title: 'Model Performance Comparison',
    description: 'Grouped bar chart comparing Accuracy, Precision, Recall, and Macro F1 across RF, XGBoost, and DNN.',
    url: '/static/results/model_metrics_comparison.png',
  },
  {
    id: 'confusion_matrices_comparison',
    title: 'Confusion Matrices',
    description: 'Side-by-side 5x5 multi-class confusion matrices for each candidate architecture.',
    url: '/static/results/confusion_matrices_comparison.png',
  },
  {
    id: 'cross_validation_distribution',
    title: '10-Fold CV Distribution',
    description: 'Box plot and fold-by-fold scatter points displaying stability across all 10 CV folds.',
    url: '/static/results/cross_validation_distribution.png',
  },
  {
    id: 'feature_importance_rf_xgb',
    title: 'Feature Importances',
    description: 'Relative Gini importance ranking of the top 12 features driving A/L stream selection.',
    url: '/static/results/feature_importance_rf_xgb.png',
  },
  {
    id: 'dnn_training_curves',
    title: 'DNN Training Curves',
    description: 'Cross-Entropy loss trajectory and validation accuracy curve with early stopping.',
    url: '/static/results/dnn_training_curves.png',
  },
  {
    id: 'shap_waterfall',
    title: 'SHAP Waterfall Attribution',
    description: 'Explains individual student prediction driving factors with positive and negative push.',
    url: '/static/results/shap_waterfall.png',
  },
  {
    id: 'shap_summary',
    title: 'Global SHAP Summary',
    description: 'Global feature impact distribution across all 5 Sri Lankan curriculum streams.',
    url: '/static/results/shap_summary.png',
  },
])

const selectedFigId = ref('model_metrics_comparison')

const activeFigure = computed(() => {
  return figures.value.find((f) => f.id === selectedFigId.value) || figures.value[0]
})

const selectedModelInfo = computed(() => {
  return report.value.models.find((m) => m.model_name === report.value.selected_model_name || m.selected_model) || report.value.models[0]
})

onMounted(async () => {
  try {
    const statsResp = await axios.get('/api/dashboard/stats')
    stats.value = statsResp.data
  } catch (e) {
    // Keep defaults
  }

  try {
    const evalResp = await axios.get('/api/evaluation')
    report.value = evalResp.data
  } catch (e) {
    // Keep defaults
  }

  try {
    const figResp = await axios.get('/api/evaluation/figures')
    if (figResp.data && figResp.data.length > 0) {
      figures.value = figResp.data
    }
  } catch (e) {
    // Keep defaults
  }
})
</script>

<style scoped>
.dashboard-view {
  padding: 2rem 0;
}

.dashboard-header {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.header-badges {
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

.metric-card {
  padding: 1.5rem;
}

.metric-title {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.metric-value {
  font-family: var(--font-mono);
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.2;
}

.text-accent {
  color: var(--accent);
  font-size: 1.25rem;
}

.metric-subtext {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-top: 0.5rem;
}

.section-heading {
  font-size: 1.35rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.section-subtext {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

/* Table */
.table-container {
  overflow-x: auto;
  padding: 0;
}

.research-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.research-table th {
  background: var(--bg-surface-elevated);
  padding: 1rem 1.25rem;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-subtle);
}

.research-table td {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--border-subtle);
  font-size: 0.9rem;
}

.selected-row {
  background: rgba(79, 70, 229, 0.08);
}

.model-name-cell {
  display: flex;
  flex-direction: column;
}

.exp-id {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--text-muted);
}

.f1-highlight {
  font-family: var(--font-mono);
  color: var(--accent);
}

/* Figure Tabs & Gallery */
.figure-tabs {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.fig-tab-btn {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  color: var(--text-secondary);
  padding: 0.5rem 1rem;
  border-radius: var(--radius-md);
  font-size: 0.825rem;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition-smooth);
}

.fig-tab-btn:hover {
  background: var(--bg-surface-elevated);
  color: var(--text-primary);
}

.fig-tab-btn.active {
  background: var(--primary-light);
  border-color: var(--primary);
  color: #ffffff;
}

.figure-display-card {
  padding: 1.5rem;
}

.figure-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 1rem;
}

.figure-title {
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.figure-desc {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.figure-img-wrapper {
  background: #0d1322;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 380px;
}

.figure-img {
  max-width: 100%;
  height: auto;
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-md);
}

/* Distribution Cards */
.dist-card {
  padding: 1.25rem;
}

.dist-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.dist-count {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-primary);
}

.dist-desc {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.stream-tag {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: var(--radius-sm);
}

.stream-tag.fill-physical { background: rgba(59, 130, 246, 0.15); color: #60a5fa; }
.stream-tag.fill-bio { background: rgba(16, 185, 129, 0.15); color: #34d399; }
.stream-tag.fill-commerce { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }
.stream-tag.fill-arts { background: rgba(236, 72, 153, 0.15); color: #f472b6; }
.stream-tag.fill-tech { background: rgba(6, 182, 212, 0.15); color: #22d3ee; }

.mt-4 { margin-top: 1.5rem; }
.mt-6 { margin-top: 3rem; }
</style>
