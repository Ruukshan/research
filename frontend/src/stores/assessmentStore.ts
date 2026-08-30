import { defineStore } from 'pinia'
import axios from 'axios'
import type { StudentAssessmentInput, AssessmentSubmissionResult } from '../types'

const API_BASE = '/api'

export const useAssessmentStore = defineStore('assessment', {
  state: () => ({
    currentStep: 1,
    formData: {
      gender: 'Male',
      district: 'Colombo',
      school_type: '1AB National School',
      medium: 'Sinhala',
      academic: {
        math_grade: 'A',
        science_grade: 'A',
        english_grade: 'A',
        first_lang_grade: 'A',
        history_grade: 'B',
        religion_grade: 'A',
        basket_1_subject: 'ICT',
        basket_1_grade: 'A',
        basket_2_subject: 'Art',
        basket_2_grade: 'B',
        basket_3_subject: 'Design_Tech',
        basket_3_grade: 'A',
      },
      extracurricular: {
        has_sports: true,
        has_clubs_societies: true,
        has_coding_robotics: true,
        has_debating_media: false,
        has_music_performing_arts: false,
        has_visual_arts: false,
        has_volunteering_scouts: false,
        has_leadership_prefect: true,
        has_reading_writing: true,
        has_entrepreneurship: false,
      },
      personality: {
        score_realistic: 4.2,
        score_investigative: 4.6,
        score_artistic: 2.4,
        score_social: 2.8,
        score_enterprising: 3.4,
        score_conventional: 3.8,
      },
      career: {
        preferred_career_domain: 'Software Architecture & AI',
        preferred_work_style: 'Team-based & Project-driven',
        higher_education_interest: 'State University Degree',
        parental_influence_level: 3,
        teacher_guidance_level: 4,
      },
    } as StudentAssessmentInput,
    isLoading: false,
    error: null as string | null,
    assessmentResult: null as AssessmentSubmissionResult | null,
  }),

  actions: {
    setStep(step: number) {
      this.currentStep = step
    },

    nextStep() {
      if (this.currentStep < 6) {
        this.currentStep++
      }
    },

    prevStep() {
      if (this.currentStep > 1) {
        this.currentStep--
      }
    },

    resetForm() {
      this.currentStep = 1
      this.assessmentResult = null
      this.error = null
    },

    async submitAssessment() {
      this.isLoading = true
      this.error = null
      try {
        const response = await axios.post<AssessmentSubmissionResult>(
          `${API_BASE}/assessment`,
          this.formData
        )
        this.assessmentResult = response.data
        return response.data
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Failed to process assessment.'
        throw err
      } finally {
        this.isLoading = false
      }
    },
  },
})
