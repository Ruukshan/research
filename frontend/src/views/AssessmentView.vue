<template>
  <div class="assessment-view container">
    <div class="stepper-header">
      <h1 class="page-title">Student Assessment Intake</h1>
      <p class="page-desc">Complete the 6-step questionnaire to receive personalized AI recommendations.</p>

      <!-- Stepper Navigation -->
      <div class="stepper-bar mt-4">
        <div 
          v-for="step in steps" 
          :key="step.number"
          class="step-item"
          :class="{ active: store.currentStep === step.number, completed: store.currentStep > step.number }"
          @click="goToStep(step.number)"
        >
          <div class="step-circle">
            <span v-if="store.currentStep > step.number">✓</span>
            <span v-else>{{ step.number }}</span>
          </div>
          <span class="step-title">{{ step.title }}</span>
        </div>
      </div>
    </div>

    <!-- Quick Preset Buttons -->
    <div class="preset-strip glass-card mt-4">
      <div class="preset-label">
        <span>⚡</span>
        <strong>Test Real Survey Archetypes:</strong>
      </div>
      <div class="preset-buttons">
        <button type="button" @click="loadPreset('tech')" class="preset-btn btn-tech">💻 Technology</button>
        <button type="button" @click="loadPreset('bio')" class="preset-btn btn-bio">🔬 Bio Science</button>
        <button type="button" @click="loadPreset('math')" class="preset-btn btn-math">📐 Physical Science</button>
        <button type="button" @click="loadPreset('comm')" class="preset-btn btn-comm">📊 Commerce</button>
        <button type="button" @click="loadPreset('arts')" class="preset-btn btn-arts">🎨 Arts</button>
      </div>
    </div>

    <!-- Multi-Step Card -->
    <div class="glass-card mt-4 assessment-card">
      <!-- Step 1: Academic Profile -->
      <div v-if="store.currentStep === 1" class="step-content">
        <h2 class="step-heading">Step 1: GCE O/L Academic Performance</h2>
        <p class="step-instruction">Enter your achieved or expected grades for core subjects and basket electives.</p>

        <div class="grid-3 mt-4">
          <div class="form-group">
            <label class="form-label">Mathematics Grade</label>
            <select v-model="store.formData.academic.math_grade" class="form-select">
              <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Science Grade</label>
            <select v-model="store.formData.academic.science_grade" class="form-select">
              <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">English Language</label>
            <select v-model="store.formData.academic.english_grade" class="form-select">
              <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">First Language (Sinhala / Tamil)</label>
            <select v-model="store.formData.academic.first_lang_grade" class="form-select">
              <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">History Grade</label>
            <select v-model="store.formData.academic.history_grade" class="form-select">
              <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Religion Grade</label>
            <select v-model="store.formData.academic.religion_grade" class="form-select">
              <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
            </select>
          </div>
        </div>

        <h3 class="subsection-title mt-4">Basket Electives</h3>
        <div class="grid-3 mt-2">
          <div class="form-group">
            <label class="form-label">Basket 1 Subject</label>
            <select v-model="store.formData.academic.basket_1_subject" class="form-select">
              <option value="ICT">Information & Comm. Tech (ICT)</option>
              <option value="Commerce">Commerce & Accounting</option>
              <option value="Geography">Geography</option>
              <option value="Civics">Civics Education</option>
              <option value="Entrepreneurship Studies">Entrepreneurship Studies</option>
            </select>
            <label class="form-label mt-2">Grade</label>
            <select v-model="store.formData.academic.basket_1_grade" class="form-select">
              <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Basket 2 Subject</label>
            <select v-model="store.formData.academic.basket_2_subject" class="form-select">
              <option value="Art">Art</option>
              <option value="Music">Music (Eastern / Western)</option>
              <option value="Drama">Drama & Theatre</option>
              <option value="Dancing">Dancing</option>
              <option value="English Literature">English Literature</option>
            </select>
            <label class="form-label mt-2">Grade</label>
            <select v-model="store.formData.academic.basket_2_grade" class="form-select">
              <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Basket 3 Subject</label>
            <select v-model="store.formData.academic.basket_3_subject" class="form-select">
              <option value="Design_Tech">Design & Technology</option>
              <option value="Agriculture">Agriculture & Food Tech</option>
              <option value="Home_Economics">Home Economics</option>
              <option value="Health_Science">Health & Physical Science</option>
            </select>
            <label class="form-label mt-2">Grade</label>
            <select v-model="store.formData.academic.basket_3_grade" class="form-select">
              <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Step 2: Extracurricular Activities -->
      <div v-else-if="store.currentStep === 2" class="step-content">
        <h2 class="step-heading">Step 2: Extracurricular Activities & Leadership</h2>
        <p class="step-instruction">Select all school clubs, sports, and co-curricular activities you have participated in.</p>

        <div class="checkbox-grid mt-4">
          <label class="checkbox-card">
            <input type="checkbox" v-model="store.formData.extracurricular.has_sports" />
            <div class="checkbox-info">
              <strong>🏃 Sports & Athletics</strong>
              <span>Track, Cricket, Badminton, Swimming, Volleyball</span>
            </div>
          </label>

          <label class="checkbox-card">
            <input type="checkbox" v-model="store.formData.extracurricular.has_coding_robotics" />
            <div class="checkbox-info">
              <strong>🤖 Coding & Robotics Club</strong>
              <span>IT society, programming competitions, electronics</span>
            </div>
          </label>

          <label class="checkbox-card">
            <input type="checkbox" v-model="store.formData.extracurricular.has_clubs_societies" />
            <div class="checkbox-info">
              <strong>🔬 Science / Commerce Societies</strong>
              <span>Academic societies, exhibition stalls, quiz teams</span>
            </div>
          </label>

          <label class="checkbox-card">
            <input type="checkbox" v-model="store.formData.extracurricular.has_debating_media" />
            <div class="checkbox-info">
              <strong>🎙️ Debating & Media Unit</strong>
              <span>School announcements, debating tournaments, journalism</span>
            </div>
          </label>

          <label class="checkbox-card">
            <input type="checkbox" v-model="store.formData.extracurricular.has_music_performing_arts" />
            <div class="checkbox-info">
              <strong>🎭 Music & Performing Arts</strong>
              <span>School choir, orchestra, stage drama, band</span>
            </div>
          </label>

          <label class="checkbox-card">
            <input type="checkbox" v-model="store.formData.extracurricular.has_visual_arts" />
            <div class="checkbox-info">
              <strong>🎨 Visual Arts & Photography</strong>
              <span>Art circles, graphic design, photography society</span>
            </div>
          </label>

          <label class="checkbox-card">
            <input type="checkbox" v-model="store.formData.extracurricular.has_volunteering_scouts" />
            <div class="checkbox-info">
              <strong>🤝 Scouts & Red Cross</strong>
              <span>Girl Guides, St. John Ambulance, community service</span>
            </div>
          </label>

          <label class="checkbox-card">
            <input type="checkbox" v-model="store.formData.extracurricular.has_leadership_prefect" />
            <div class="checkbox-info">
              <strong>⭐ Prefect Guild & Leadership</strong>
              <span>School prefect, house captain, society president</span>
            </div>
          </label>

          <label class="checkbox-card">
            <input type="checkbox" v-model="store.formData.extracurricular.has_reading_writing" />
            <div class="checkbox-info">
              <strong>📚 Literary Association</strong>
              <span>Reading circles, poetry, essay writing, library club</span>
            </div>
          </label>

          <label class="checkbox-card">
            <input type="checkbox" v-model="store.formData.extracurricular.has_entrepreneurship" />
            <div class="checkbox-info">
              <strong>💼 Young Entrepreneurs Club</strong>
              <span>Mini-business ventures, commerce fairs, innovation</span>
            </div>
          </label>
        </div>
      </div>

      <!-- Step 3: RIASEC Personality -->
      <div v-else-if="store.currentStep === 3" class="step-content">
        <h2 class="step-heading">Step 3: Holland RIASEC Personality Dimensions</h2>
        <p class="step-instruction">Rate your affinity for each career orientation style (1 = Low, 5 = High).</p>

        <div class="riasec-grid mt-4">
          <div class="riasec-slider-card">
            <div class="riasec-header">
              <strong>Realistic (R) - Practical & Hands-on</strong>
              <span class="score-badge">{{ store.formData.personality.score_realistic }} / 5.0</span>
            </div>
            <p>Working with machines, building physical systems, outdoor work, tools and equipment.</p>
            <input type="range" min="1.0" max="5.0" step="0.1" v-model.number="store.formData.personality.score_realistic" class="range-slider" />
          </div>

          <div class="riasec-slider-card">
            <div class="riasec-header">
              <strong>Investigative (I) - Scientific & Analytical</strong>
              <span class="score-badge">{{ store.formData.personality.score_investigative }} / 5.0</span>
            </div>
            <p>Solving complex mathematics, scientific research, diagnosing problems, discovery.</p>
            <input type="range" min="1.0" max="5.0" step="0.1" v-model.number="store.formData.personality.score_investigative" class="range-slider" />
          </div>

          <div class="riasec-slider-card">
            <div class="riasec-header">
              <strong>Artistic (A) - Creative & Expressive</strong>
              <span class="score-badge">{{ store.formData.personality.score_artistic }} / 5.0</span>
            </div>
            <p>Visual art, literature, drama, creative writing, digital media, music, original expression.</p>
            <input type="range" min="1.0" max="5.0" step="0.1" v-model.number="store.formData.personality.score_artistic" class="range-slider" />
          </div>

          <div class="riasec-slider-card">
            <div class="riasec-header">
              <strong>Social (S) - Teaching & Helping</strong>
              <span class="score-badge">{{ store.formData.personality.score_social }} / 5.0</span>
            </div>
            <p>Guiding people, healthcare, teamwork, social welfare, counseling, community service.</p>
            <input type="range" min="1.0" max="5.0" step="0.1" v-model.number="store.formData.personality.score_social" class="range-slider" />
          </div>

          <div class="riasec-slider-card">
            <div class="riasec-header">
              <strong>Enterprising (E) - Leadership & Business</strong>
              <span class="score-badge">{{ store.formData.personality.score_enterprising }} / 5.0</span>
            </div>
            <p>Managing projects, public speaking, entrepreneurship, marketing, strategic decisions.</p>
            <input type="range" min="1.0" max="5.0" step="0.1" v-model.number="store.formData.personality.score_enterprising" class="range-slider" />
          </div>

          <div class="riasec-slider-card">
            <div class="riasec-header">
              <strong>Conventional (C) - Organized & Data-focused</strong>
              <span class="score-badge">{{ store.formData.personality.score_conventional }} / 5.0</span>
            </div>
            <p>Financial records, data tables, structured rules, accuracy, systematic organization.</p>
            <input type="range" min="1.0" max="5.0" step="0.1" v-model.number="store.formData.personality.score_conventional" class="range-slider" />
          </div>
        </div>
      </div>

      <!-- Step 4: Career Aspirations & Influences -->
      <div v-else-if="store.currentStep === 4" class="step-content">
        <h2 class="step-heading">Step 4: Career Aspirations & Influences</h2>
        <p class="step-instruction">Tell us about your long-term occupational goals and educational path preferences.</p>

        <div class="grid-2 mt-4">
          <div class="form-group">
            <label class="form-label">Preferred Career Domain</label>
            <select v-model="store.formData.career.preferred_career_domain" class="form-select">
              <option value="Software Architecture & AI">Software Engineering, AI & Computing</option>
              <option value="Civil & Structural Engineering">Civil / Mechanical / Electrical Engineering</option>
              <option value="Medicine & Clinical Surgery">Medicine, Surgery & Healthcare</option>
              <option value="Biomedical & Molecular Genetics">Biomedical Science & Genetics</option>
              <option value="Accounting, Audit & Taxation">Accounting, Finance & Banking</option>
              <option value="Digital Marketing & Brand Strategy">Marketing & Business Administration</option>
              <option value="Law, Judiciary & Advocacy">Law & Legal Practice</option>
              <option value="Journalism & Digital Mass Media">Media, Journalism & PR</option>
              <option value="Robotics, Mechatronics & Automation">Robotics & Engineering Technology</option>
              <option value="Biosystems & Industrial Food Tech">Biosystems & Food Science Tech</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Preferred Work Style</label>
            <select v-model="store.formData.career.preferred_work_style" class="form-select">
              <option value="Team-based & Project-driven">Team-based & Project-driven</option>
              <option value="Independent Analytical & Research">Independent Analytical & Research</option>
              <option value="Hands-on Practical & Fieldwork">Hands-on Practical & Fieldwork</option>
              <option value="Client-facing & Communicative">Client-facing & Communicative</option>
              <option value="Structured, Routine & Detail-focused">Structured, Routine & Detail-focused</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Higher Education Interest</label>
            <select v-model="store.formData.career.higher_education_interest" class="form-select">
              <option value="State University Degree">State University Degree (UGC Merit/District)</option>
              <option value="State University Technology Degree">State University Technology / Applied Degree</option>
              <option value="Private/Foreign University Degree">Private / Foreign Affiliated University Degree</option>
              <option value="Professional Qualification">Professional Chartered Pathway (CA/CIMA/SLIIT/Law)</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Parental Influence Level (1 = Low, 5 = High)</label>
            <select v-model.number="store.formData.career.parental_influence_level" class="form-select">
              <option :value="1">1 - Minimal Influence (Independent Choice)</option>
              <option :value="2">2 - Low Influence</option>
              <option :value="3">3 - Moderate Advisory Influence</option>
              <option :value="4">4 - High Influence</option>
              <option :value="5">5 - Decisive Parental Direction</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Step 5: Demographic & School Context -->
      <div v-else-if="store.currentStep === 5" class="step-content">
        <h2 class="step-heading">Step 5: Demographic & School Context</h2>
        <p class="step-instruction">Educational background and administrative district (used for UGC merit/district context).</p>

        <div class="grid-2 mt-4">
          <div class="form-group">
            <label class="form-label">Administrative District</label>
            <select v-model="store.formData.district" class="form-select">
              <option v-for="d in districts" :key="d" :value="d">{{ d }}</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">School Classification</label>
            <select v-model="store.formData.school_type" class="form-select">
              <option value="1AB National School">1AB National School (All Streams Available)</option>
              <option value="1AB Provincial School">1AB Provincial School</option>
              <option value="1C School">1C School (Arts & Commerce)</option>
              <option value="Type 2 School">Type 2 School (Up to O/L)</option>
              <option value="Private/Semi-Government">Private / Semi-Government School</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Medium of Instruction</label>
            <select v-model="store.formData.medium" class="form-select">
              <option value="Sinhala">Sinhala Medium</option>
              <option value="Tamil">Tamil Medium</option>
              <option value="English">English Medium</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Gender Demographic</label>
            <select v-model="store.formData.gender" class="form-select">
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Prefer not to say">Prefer not to say</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Step 6: Review and Submit -->
      <div v-else-if="store.currentStep === 6" class="step-content">
        <h2 class="step-heading">Step 6: Review Assessment Profile</h2>
        <p class="step-instruction">Review your profile before executing the ML stream prediction and hybrid recommendation model.</p>

        <div class="review-grid mt-4">
          <div class="review-section">
            <h4>Academic Snapshot</h4>
            <div class="review-badges">
              <span class="review-badge">Math: <strong>{{ store.formData.academic.math_grade }}</strong></span>
              <span class="review-badge">Science: <strong>{{ store.formData.academic.science_grade }}</strong></span>
              <span class="review-badge">English: <strong>{{ store.formData.academic.english_grade }}</strong></span>
              <span class="review-badge">First Lang: <strong>{{ store.formData.academic.first_lang_grade }}</strong></span>
              <span class="review-badge">{{ store.formData.academic.basket_1_subject }}: <strong>{{ store.formData.academic.basket_1_grade }}</strong></span>
            </div>
          </div>

          <div class="review-section">
            <h4>Dominant RIASEC Profile</h4>
            <p class="riasec-summary">
              R: {{ store.formData.personality.score_realistic }} | 
              I: {{ store.formData.personality.score_investigative }} | 
              A: {{ store.formData.personality.score_artistic }} | 
              S: {{ store.formData.personality.score_social }} | 
              E: {{ store.formData.personality.score_enterprising }} | 
              C: {{ store.formData.personality.score_conventional }}
            </p>
          </div>

          <div class="review-section">
            <h4>Target Aspirations</h4>
            <p>{{ store.formData.career.preferred_career_domain }} ({{ store.formData.career.higher_education_interest }})</p>
          </div>
        </div>

        <div class="disclaimer-banner mt-4">
          <span>⚖️</span>
          <p>
            By submitting, your profile will be evaluated by the recommendation model. Results are for educational decision support only.
          </p>
        </div>
      </div>

      <!-- Navigation Actions -->
      <div class="step-actions mt-6">
        <button 
          v-if="store.currentStep > 1" 
          @click="store.prevStep()" 
          class="btn btn-secondary"
          :disabled="store.isLoading"
        >
          ← Back
        </button>
        <div class="action-spacer"></div>
        <button 
          v-if="store.currentStep < 6" 
          @click="store.nextStep()" 
          class="btn btn-primary"
        >
          Continue ➔
        </button>
        <button 
          v-else 
          @click="handleSubmit" 
          class="btn btn-primary"
          :disabled="store.isLoading"
        >
          <span v-if="store.isLoading">Computing Recommendations...</span>
          <span v-else>Generate Ranked Pathways 🚀</span>
        </button>
      </div>

      <div v-if="store.error" class="error-msg mt-4">
        ⚠️ {{ store.error }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAssessmentStore } from '../stores/assessmentStore'

const router = useRouter()
const store = useAssessmentStore()

const grades = ["A", "B", "C", "S", "W"]

const steps = [
  { number: 1, title: 'Academic' },
  { number: 2, title: 'Activities' },
  { number: 3, title: 'RIASEC' },
  { number: 4, title: 'Aspirations' },
  { number: 5, title: 'Context' },
  { number: 6, title: 'Review' },
]

const districts = [
  "Colombo", "Gampaha", "Kalutara", "Kandy", "Matale", "Nuwara Eliya",
  "Galle", "Matara", "Hambantota", "Jaffna", "Kilinochchi", "Mannar",
  "Vavuniya", "Mullaitivu", "Batticaloa", "Ampara", "Trincomalee",
  "Kurunegala", "Puttalam", "Anuradhapura", "Polonnaruwa", "Badulla",
  "Monaragala", "Ratnapura", "Kegalle"
]

const goToStep = (stepNum: number) => {
  if (stepNum <= store.currentStep || store.currentStep === 6) {
    store.setStep(stepNum)
  }
}

const loadPreset = (type: 'tech' | 'bio' | 'math' | 'comm' | 'arts') => {
  if (type === 'tech') {
    store.formData.academic = {
      math_grade: 'A', science_grade: 'A', english_grade: 'A', first_lang_grade: 'B', history_grade: 'B', religion_grade: 'A',
      basket_1_subject: 'ICT', basket_1_grade: 'A', basket_2_subject: 'Drama', basket_2_grade: 'B', basket_3_subject: 'Design_Tech', basket_3_grade: 'A'
    }
    store.formData.extracurricular = {
      has_sports: true, has_clubs_societies: true, has_coding_robotics: true, has_debating_media: false, has_music_performing_arts: false,
      has_visual_arts: false, has_volunteering_scouts: false, has_leadership_prefect: true, has_reading_writing: true, has_entrepreneurship: false
    }
    store.formData.personality = { score_realistic: 4.8, score_investigative: 4.6, score_artistic: 2.3, score_social: 2.8, score_enterprising: 3.5, score_conventional: 3.9 }
    store.formData.career.preferred_career_domain = 'Software Architecture & AI'
    store.formData.career.higher_education_interest = 'State University Technology Degree'
  } else if (type === 'bio') {
    store.formData.academic = {
      math_grade: 'B', science_grade: 'A', english_grade: 'A', first_lang_grade: 'A', history_grade: 'A', religion_grade: 'A',
      basket_1_subject: 'Geography', basket_1_grade: 'A', basket_2_subject: 'Drama', basket_2_grade: 'B', basket_3_subject: 'Health_Science', basket_3_grade: 'A'
    }
    store.formData.extracurricular = {
      has_sports: true, has_clubs_societies: true, has_coding_robotics: false, has_debating_media: false, has_music_performing_arts: false,
      has_visual_arts: false, has_volunteering_scouts: true, has_leadership_prefect: true, has_reading_writing: false, has_entrepreneurship: false
    }
    store.formData.personality = { score_realistic: 2.5, score_investigative: 4.8, score_artistic: 2.0, score_social: 4.7, score_enterprising: 3.0, score_conventional: 3.4 }
    store.formData.career.preferred_career_domain = 'Medicine & Clinical Surgery'
    store.formData.career.higher_education_interest = 'State University Degree'
  } else if (type === 'math') {
    store.formData.academic = {
      math_grade: 'A', science_grade: 'A', english_grade: 'A', first_lang_grade: 'A', history_grade: 'A', religion_grade: 'A',
      basket_1_subject: 'ICT', basket_1_grade: 'A', basket_2_subject: 'Art', basket_2_grade: 'B', basket_3_subject: 'Design_Tech', basket_3_grade: 'A'
    }
    store.formData.extracurricular = {
      has_sports: true, has_clubs_societies: true, has_coding_robotics: true, has_debating_media: false, has_music_performing_arts: false,
      has_visual_arts: false, has_volunteering_scouts: false, has_leadership_prefect: true, has_reading_writing: false, has_entrepreneurship: false
    }
    store.formData.personality = { score_realistic: 4.6, score_investigative: 4.9, score_artistic: 2.0, score_social: 2.4, score_enterprising: 3.2, score_conventional: 4.3 }
    store.formData.career.preferred_career_domain = 'Civil & Structural Engineering'
    store.formData.career.higher_education_interest = 'State University Degree'
  } else if (type === 'comm') {
    store.formData.academic = {
      math_grade: 'B', science_grade: 'C', english_grade: 'A', first_lang_grade: 'A', history_grade: 'A', religion_grade: 'A',
      basket_1_subject: 'Commerce', basket_1_grade: 'A', basket_2_subject: 'Art', basket_2_grade: 'B', basket_3_subject: 'Health_Science', basket_3_grade: 'B'
    }
    store.formData.extracurricular = {
      has_sports: false, has_clubs_societies: true, has_coding_robotics: false, has_debating_media: true, has_music_performing_arts: false,
      has_visual_arts: false, has_volunteering_scouts: false, has_leadership_prefect: true, has_reading_writing: true, has_entrepreneurship: true
    }
    store.formData.personality = { score_realistic: 2.1, score_investigative: 3.0, score_artistic: 2.8, score_social: 3.8, score_enterprising: 4.8, score_conventional: 4.6 }
    store.formData.career.preferred_career_domain = 'Accounting, Audit & Taxation'
    store.formData.career.higher_education_interest = 'Professional Qualification'
  } else if (type === 'arts') {
    store.formData.academic = {
      math_grade: 'C', science_grade: 'S', english_grade: 'A', first_lang_grade: 'A', history_grade: 'A', religion_grade: 'A',
      basket_1_subject: 'Civics', basket_1_grade: 'A', basket_2_subject: 'Drama', basket_2_grade: 'A', basket_3_subject: 'Home_Economics', basket_3_grade: 'B'
    }
    store.formData.extracurricular = {
      has_sports: false, has_clubs_societies: true, has_coding_robotics: false, has_debating_media: true, has_music_performing_arts: true,
      has_visual_arts: true, has_volunteering_scouts: true, has_leadership_prefect: true, has_reading_writing: true, has_entrepreneurship: false
    }
    store.formData.personality = { score_realistic: 1.8, score_investigative: 2.4, score_artistic: 4.9, score_social: 4.5, score_enterprising: 3.9, score_conventional: 2.3 }
    store.formData.career.preferred_career_domain = 'Law, Judiciary & Advocacy'
    store.formData.career.higher_education_interest = 'State University Degree'
  }
}

const handleSubmit = async () => {
  try {
    await store.submitAssessment()
    router.push('/results')
  } catch (e) {
    // Error is handled in store
  }
}
</script>

<style scoped>
.preset-strip {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.25rem;
  gap: 0.75rem;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.preset-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.preset-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.preset-btn {
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  font-size: 0.82rem;
  font-weight: 600;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.preset-btn:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.12);
}

.btn-tech:hover { border-color: #06b6d4; color: #06b6d4; }
.btn-bio:hover { border-color: #10b981; color: #10b981; }
.btn-math:hover { border-color: #3b82f6; color: #3b82f6; }
.btn-comm:hover { border-color: #f59e0b; color: #f59e0b; }
.btn-arts:hover { border-color: #ec4899; color: #ec4899; }

.assessment-view {
  padding: 2rem 0;
  max-width: 900px;
}

.stepper-header {
  text-align: center;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.page-desc {
  color: var(--text-secondary);
}

.stepper-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  margin: 2rem 0;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  z-index: 1;
}

.step-circle {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: var(--bg-surface);
  border: 2px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
  color: var(--text-muted);
  transition: var(--transition-smooth);
}

.step-item.active .step-circle {
  background: var(--primary);
  border-color: var(--primary);
  color: #ffffff;
  box-shadow: 0 0 15px rgba(79, 70, 229, 0.5);
}

.step-item.completed .step-circle {
  background: var(--success);
  border-color: var(--success);
  color: #ffffff;
}

.step-title {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.step-item.active .step-title {
  color: var(--text-primary);
}

.assessment-card {
  min-height: 480px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.step-heading {
  font-size: 1.35rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.step-instruction {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
}

.subsection-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--accent);
}

/* Checkbox Grid */
.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}

.checkbox-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 1rem;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  cursor: pointer;
  transition: var(--transition-smooth);
}

.checkbox-card:hover {
  border-color: rgba(255, 255, 255, 0.2);
}

.checkbox-info {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.checkbox-info strong {
  font-size: 0.9rem;
}

.checkbox-info span {
  font-size: 0.775rem;
  color: var(--text-muted);
}

/* RIASEC Sliders */
.riasec-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 1.25rem;
}

.riasec-slider-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 1.25rem;
}

.riasec-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.25rem;
}

.score-badge {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--accent);
}

.riasec-slider-card p {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}

.range-slider {
  width: 100%;
  accent-color: var(--primary);
}

/* Review Section */
.review-grid {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.review-section {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 1.25rem;
}

.review-section h4 {
  font-size: 0.95rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.review-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.review-badge {
  background: var(--bg-surface-elevated);
  padding: 0.35rem 0.75rem;
  border-radius: var(--radius-sm);
  font-size: 0.825rem;
}

.step-actions {
  display: flex;
  align-items: center;
  border-top: 1px solid var(--border-subtle);
  padding-top: 1.5rem;
}

.action-spacer {
  flex: 1;
}

.error-msg {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: var(--radius-md);
  padding: 0.75rem 1rem;
  color: #fca5a5;
  font-size: 0.9rem;
}

.mt-2 { margin-top: 0.5rem; }
.mt-4 { margin-top: 1.5rem; }
.mt-6 { margin-top: 2rem; }

@media (max-width: 640px) {
  .step-title {
    display: none;
  }
}
</style>
