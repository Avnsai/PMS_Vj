// Centralized type definitions for the application

export interface User {
  id: string
  email: string
  username: string
  first_name?: string
  last_name?: string
  role: string
  organization_id: string
  is_active: boolean
  email_verified: boolean
  avatar_url?: string
  created_at: string
  phone?: string
  bio?: string
  timezone?: string
  language?: string
  theme?: string
  notifications_enabled?: boolean
  activity_tracking_level?: string
}

export interface Task {
  id: string
  title: string
  description?: string
  status: 'todo' | 'in_progress' | 'review' | 'completed' | 'blocked' | 'done' | 'cancelled' | 'in_review'
  priority: 'low' | 'medium' | 'high' | 'critical'
  type?: 'task' | 'bug' | 'feature' | 'epic' | 'story' | 'milestone'
  project_id: string
  assignee_id?: string
  assignee_ids?: string[]
  assigned_to?: string[]
  reporter_id?: string
  parent_task_id?: string
  created_at: string
  updated_at?: string
  due_date?: string | null
  start_date?: string | null
  completed_at?: string | null
  estimated_hours?: number
  actual_hours?: number
  percent_complete?: number
  dependencies?: string[] | Array<{ task_id: string; dependency_type: string }>
  tags?: string[]
  attachments?: string[]
  time_tracking?: {
    logged_time?: number
    remaining_estimate?: number
    estimated_hours?: number
    actual_hours?: number
  }
}

export interface TimelineTask extends Task {
  start_date: string
  end_date: string
  dependencies: string[]
  assignee_ids: string[]
}

export interface Comment {
  id: string
  content: string
  type: 'comment' | 'note' | 'review' | 'suggestion' | 'approval'
  entity_type: 'task' | 'project'
  entity_id: string
  author_id: string
  author_name?: string
  parent_id?: string | null
  thread_id?: string | null
  nested_replies?: Comment[]
  mentions?: Array<{
    user_id: string
    username: string
    position: number
  }>
  attachments?: string[]
  is_edited: boolean
  created_at: string
  updated_at?: string
  reactions?: Array<{
    user_id: string
    type: string
  }>
}

export interface SecurityMetrics {
  security_events: {
    total_last_30_days: number
    by_type: Record<string, number>
    high_risk_events: number
  }
  mfa_status: {
    adoption_rate: number
    enabled_users: number
    total_users: number
  }
  threat_detection: {
    active_threats: number
    status: string
  }
  threat_intelligence?: {
    active_threats: number
    critical_alerts: number
    blocked_ips: number
    malware_detected: number
    indicators?: Array<{
      type: string
      value: string
      severity: string
      confidence: number
      last_seen: string
    }>
  }
  vulnerability_status?: {
    critical: number
    high: number
    medium: number
    low: number
    patched_last_30_days?: number
    remediation_rate?: number
  }
  security_trends?: {
    events_trend: string
    threat_trend: string
    compliance_trend: string
  }
  compliance: {
    active_certifications: number
    status: string
  }
  system_health: {
    overall_status: string
    last_updated: string
    zero_trust_enabled: boolean
  }
}

export interface TaskConflict {
  id: string
  type: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  description: string
  task_id: string
  related_task_id?: string
  affected_tasks?: string[]
  detected_at: string
  resolved: boolean
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
  user_id?: string
}

export interface Project {
  id: string
  name: string
  description?: string
  status: 'planning' | 'active' | 'on_hold' | 'completed' | 'archived'
  start_date?: string
  end_date?: string
  organization_id: string
  owner_id: string
  created_at: string
  updated_at?: string
  budget?: number
  progress?: number
  team_members?: string[]
}
