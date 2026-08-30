export type GradeType = "A" | "B" | "C" | "S" | "W";

export interface AcademicProfile {
  math_grade: GradeType;
  science_grade: GradeType;
  english_grade: GradeType;
  first_lang_grade: GradeType;
  history_grade: GradeType;
  religion_grade: GradeType;
  basket_1_subject: string;
  basket_1_grade: GradeType;
  basket_2_subject: string;
  basket_2_grade: GradeType;
  basket_3_subject: string;
  basket_3_grade: GradeType;
}

export interface ExtracurricularProfile {
  has_sports: boolean;
  has_clubs_societies: boolean;
  has_coding_robotics: boolean;
  has_debating_media: boolean;
  has_music_performing_arts: boolean;
  has_visual_arts: boolean;
  has_volunteering_scouts: boolean;
  has_leadership_prefect: boolean;
  has_reading_writing: boolean;
  has_entrepreneurship: boolean;
}

export interface PersonalityProfile {
  score_realistic: number;
  score_investigative: number;
  score_artistic: number;
  score_social: number;
  score_enterprising: number;
  score_conventional: number;
}

export interface CareerPreference {
  preferred_career_domain: string;
  preferred_work_style: string;
  higher_education_interest: string;
  parental_influence_level: number;
  teacher_guidance_level: number;
}

export interface StudentAssessmentInput {
  gender: string;
  district: string;
  school_type: string;
  medium: string;
  academic: AcademicProfile;
  extracurricular: ExtracurricularProfile;
  personality: PersonalityProfile;
  career: CareerPreference;
}

export interface PathwayRecommendationItem {
  rank: number;
  pathway_id: string;
  stream: string;
  degree_area: string;
  degree_program: string;
  career_domain: string;
  score: number;
  ml_stream_score: number;
  content_similarity_score: number;
  collaborative_score: number;
  compatibility_level: string;
  explanation: string;
  sample_job_titles?: string[];
  required_subjects?: string[];
}

export interface AssessmentSubmissionResult {
  student_id: string;
  record_id: string;
  data_source: string;
  model_name?: string;
  stream_probabilities: Record<string, number>;
  predicted_stream: string;
  recommendations: PathwayRecommendationItem[];
  shap_explanation?: {
    top_positive: string[];
    top_negative: string[];
  };
  disclaimer: string;
}

export interface CareerPathway {
  pathway_id: string;
  stream: string;
  degree_area: string;
  degree_program: string;
  career_domain: string;
  required_subjects: string[];
  preferred_subjects: string[];
  interest_tags: string[];
  riasec_profile: Record<string, number>;
  skill_tags: string[];
  description: string;
  sample_job_titles?: string[];
}

export interface ModelExperimentRecord {
  experiment_id: string;
  date: string;
  dataset_source: string;
  dataset_size: number;
  feature_version: string;
  preprocessing_version: string;
  model_name: string;
  hyperparameters: Record<string, any>;
  cv_mean: number;
  cv_std: number;
  test_accuracy: number;
  test_precision: number;
  test_recall: number;
  test_f1: number;
  random_seed: number;
  selected_model: boolean;
  notes?: string;
}

export interface ModelComparisonReport {
  dataset_source: string;
  total_samples: number;
  models: ModelExperimentRecord[];
  selected_model_name: string;
  evaluation_summary: string;
  created_at: string;
}
