/**
 * Standard envelope every agent returns. Designed to drive approval gates,
 * compliance logs, and downstream workflow decisions.
 */
export interface AgentEnvelope<T> {
  output: T;
  confidence: 'low' | 'medium' | 'high';
  assumptions: string[];
  compliance_concerns: string[];
  human_review_required: boolean;
  suggested_next_action: string;
}
