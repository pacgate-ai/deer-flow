"use client";

import Link from "next/link";
import {
  WorkspaceBody,
  WorkspaceContainer,
  WorkspaceHeader,
} from "@/components/workspace/workspace-container";
import { Badge } from "@/components/ui/badge";
import { useI18n } from "@/core/i18n/hooks";
import { useMatters } from "@/core/matters/hooks";
import type { MatterSummary } from "@/core/matters/types";

function ConflictsBadge({ cleared }: { cleared: boolean }) {
  if (cleared) {
    return <Badge className="bg-green-100 text-green-800">利冲已清</Badge>;
  }
  return <Badge className="bg-red-100 text-red-800">利冲未清</Badge>;
}

function MatterRow({ matter }: { matter: MatterSummary }) {
  return (
    <tr className="border-b hover:bg-muted/50">
      <td className="p-3">
        <Link
          href={`/workspace/chats/${matter.thread_id}`}
          className="text-blue-600 hover:underline"
        >
          {matter.title || matter.thread_id.slice(0, 12)}
        </Link>
      </td>
      <td className="p-3 text-sm text-muted-foreground">{matter.agent_name || "—"}</td>
      <td className="p-3">
        <ConflictsBadge cleared={matter.conflicts_cleared} />
      </td>
      <td className="p-3 text-sm">
        {matter.has_dd_report ? (
          <Badge className="bg-blue-100 text-blue-800">DD 报告</Badge>
        ) : (
          <span className="text-muted-foreground">—</span>
        )}
      </td>
      <td className="p-3 text-sm text-muted-foreground">
        {matter.active_skills.length > 0
          ? matter.active_skills.join(", ")
          : "—"}
      </td>
      <td className="p-3 text-sm text-muted-foreground">{matter.message_count}</td>
      <td className="p-3 text-sm text-muted-foreground">
        {matter.last_activity
          ? new Date(matter.last_activity).toLocaleDateString()
          : "—"}
      </td>
    </tr>
  );
}

export default function MattersPage() {
  const { t } = useI18n();
  const mattersQuery = useMatters();

  const matters = mattersQuery.data?.matters ?? [];
  const loading = mattersQuery.isLoading;
  const error = mattersQuery.error;

  return (
    <WorkspaceContainer>
      <WorkspaceHeader>
        <h1 className="text-xl font-semibold">
          {t.sidebar.matters || "Matters"}
        </h1>
        <p className="text-sm text-muted-foreground">
          {matters.length} {t.sidebar.matters || "matters"}
        </p>
      </WorkspaceHeader>
      <WorkspaceBody>
        {loading && <p className="text-muted-foreground p-4">Loading...</p>}
        {error && (
          <p className="text-red-600 p-4">
            Failed to load matters: {error.message}
          </p>
        )}
        {!loading && !error && matters.length === 0 && (
          <p className="text-muted-foreground p-4">No matters found.</p>
        )}
        {!loading && !error && matters.length > 0 && (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left">
                  <th className="p-3 font-medium">Title</th>
                  <th className="p-3 font-medium">Agent</th>
                  <th className="p-3 font-medium">Conflicts</th>
                  <th className="p-3 font-medium">DD Report</th>
                  <th className="p-3 font-medium">Active Skills</th>
                  <th className="p-3 font-medium">Messages</th>
                  <th className="p-3 font-medium">Last Activity</th>
                </tr>
              </thead>
              <tbody>
                {matters.map((matter) => (
                  <MatterRow key={matter.thread_id} matter={matter} />
                ))}
              </tbody>
            </table>
          </div>
        )}
      </WorkspaceBody>
    </WorkspaceContainer>
  );
}