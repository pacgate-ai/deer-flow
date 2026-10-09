export type MatterSummary = {
  thread_id: string;
  title: string | null;
  agent_name: string | null;
  conflicts_cleared: boolean;
  last_activity: string | null;
  message_count: number;
  has_dd_report: boolean;
  active_skills: string[];
};

export type MatterListResponse = {
  matters: MatterSummary[];
  total: number;
};