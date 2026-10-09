import { throwGatewayApiError } from "@/core/api/errors";
import { fetch as apiFetch } from "@/core/api/fetcher";
import { getBackendBaseURL } from "@/core/config";
import type { MatterListResponse } from "./types";

function mattersUrl(path: string): string {
  return `${getBackendBaseURL()}/api/matters${path}`;
}

export async function fetchMatters(): Promise<MatterListResponse> {
  const response = await apiFetch(mattersUrl(""));
  if (!response.ok) {
    await throwGatewayApiError(response, `Failed to load matters: ${response.statusText}`);
  }
  return response.json();
}