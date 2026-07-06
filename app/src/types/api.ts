export type UUID = string;
export type ISODateTime = string;

export interface User {
  id: UUID;
  name: string;
  email: string;
  is_active: boolean;
}

export interface UserPatch {
  name?: string;
  is_active?: boolean;
}

export interface RegisterRequest {
  name: string;
  email: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: "bearer";
}

export interface LearnerProfileCreate {
  user_id: UUID;
  academic_level?: string;
  institution?: string;
  major?: string;
  learning_style?: string;
  preferred_explanation_style?: string;
  preferred_difficulty?: string;
  domain?: string[];
  language?: string;
}

export interface LearnerProfilePatch {
  academic_level?: string;
  institution?: string;
  major?: string;
  learning_style?: string;
  preferred_explanation_style?: string;
  preferred_difficulty?: string;
  domain?: string[];
  language?: string;
}

export interface LearnerProfile {
  id: UUID;
  user_id: UUID;
  academic_level: string | null;
  institution: string | null;
  major: string | null;
  learning_style: string | null;
  preferred_explanation_style: string | null;
  preferred_difficulty: string | null;
  domain: string[];
  language: string;
  created_at: ISODateTime;
  updated_at: ISODateTime | null;
}

export interface LearnerPreferences {
  learning_style: string | null;
  preferred_explanation_style: string | null;
  preferred_difficulty: string | null;
  domain: string[];
  language: string;
}

export interface ConceptCreate {
  name: string;
  description?: string;
  difficulty?: string;
  domain?: string;
}

export interface ConceptPatch {
  name?: string;
  description?: string;
  difficulty?: string;
  domain?: string;
}

export interface Concept {
  id: UUID;
  name: string;
  description: string | null;
  difficulty: string | null;
  domain: string | null;
  isactive: boolean;
  created_at: ISODateTime;
}

export interface ConceptSummary {
  id: UUID;
  name: string;
  difficulty: string | null;
}

export type ConceptType =
  | "concept"
  | "misconception"
  | "question"
  | "resource"
  | "prerequisite"
  | "related"
  | "prerequisite_of"
  | "related_to"
  | "misconception_of"
  | "misconception_related_to";

export interface ConceptNodeCreate {
  id: UUID;
  name: string;
  concepttype?: ConceptType;
  description?: string;
  difficulty?: number;
  domain?: string;
}

export interface ConceptRelationshipCreate {
  target_concept_id: UUID;
}

export interface ConceptRelationshipRemove {
  target_concept_id: UUID;
  relationship: string;
}

export interface RelatedConcept {
  id: UUID;
  name: string;
  description: string | null;
  difficulty: number | null;
  domain: string | null;
}

export interface GraphNode {
  id: UUID;
  label: string;
  node_type: string;
  metadata?: Record<string, unknown> | null;
}

export interface GraphEdge {
  source: UUID;
  target: UUID;
  relationship: string;
  weight?: number | null;
  confidence?: number | null;
}

export interface ConceptGraph {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface EntityReference {
  id: UUID;
  name?: string | null;
  title?: string | null;
}

export interface ConceptDetail {
  id: UUID;
  name: string;
  description?: string | null;
  difficulty?: number | null;
  domain?: string | null;
}

export interface ConceptNeighborhood {
  concept: ConceptDetail;
  prerequisites: EntityReference[];
  related: EntityReference[];
  misconceptions: EntityReference[];
}

export interface LearningPath {
  path: ConceptDetail[];
  difficulty_score: number;
  estimated_time: number;
}

export interface ConceptMasteryCreate {
  user_id: UUID;
  concept_id: UUID;
  mastery_score: number;
  confidence: number;
}

export interface ConceptMastery {
  id: UUID;
  user_id: UUID;
  concept_id: UUID;
  mastery_score: number;
  confidence: number;
  last_interaction: ISODateTime;
}

export interface MisconceptionCreate {
  name: string;
  user_id: UUID;
  title: string;
  explanation: string;
  concept_ids: UUID[];
  frequency?: number;
}

export interface MisconceptionPatch {
  name?: string;
  title?: string;
  explanation?: string;
  frequency?: number;
  concept_ids?: UUID[];
}

export interface Misconception {
  id: UUID;
  user_id: UUID;
  title: string;
  explanation: string;
  concept_ids: UUID[];
  frequency: number | null;
  created_at: string;
}

export interface RetrievalMetadata {
  source_count: number;
  retrieved_chunks: number;
  average_similarity?: number | null;
}

export interface ExplanationCreate {
  prompt?: string;
  generated_explanation?: string;
  difficulty_score?: number;
  explanation_style?: string;
  token_count?: number;
  llm_provider: string;
  llm_model?: string;
  generation_time_ms?: number;
  retrieval?: RetrievalMetadata;
}

export interface Explanation {
  id: UUID;
  exp_session_id: UUID;
  prompt: string | null;
  generated_explanation: string | null;
  difficulty_score: number | null;
  explanation_style: string | null;
  token_count: number | null;
  llm_provider: string;
  llm_model: string | null;
  generation_time_ms: number | null;
  retrieval: RetrievalMetadata | null;
  created_at: ISODateTime;
}

export interface ExplanationSessionCreate {
  user_id: UUID;
  topic: string;
  explanations: ExplanationCreate[];
}

export interface ExplanationSession {
  id: UUID;
  user_id: UUID;
  topic: string;
  created_at: ISODateTime;
  explanations: Explanation[];
}

export interface ExplanationSessionHistoryItem {
  id: UUID;
  topic: string;
  created_at: ISODateTime;
}

export interface ExplanationSessionHistory {
  sessions: ExplanationSessionHistoryItem[];
}

export interface FeedbackCreate {
  explanation_id: UUID;
  rating?: number;
  clarity_score?: number;
  usefulness_score?: number;
  correctness_score?: number;
  comments?: string;
}

export interface FeedbackPatch {
  rating?: number;
  clarity_score?: number;
  usefulness_score?: number;
  correctness_score?: number;
  comments?: string;
}

export interface Feedback {
  id: UUID;
  explanation_id: UUID;
  rating: number | null;
  clarity_score: number | null;
  usefulness_score: number | null;
  correctness_score: number | null;
  comments: string | null;
  created_at: ISODateTime;
}
