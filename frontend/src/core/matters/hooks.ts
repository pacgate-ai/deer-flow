import { useQuery } from "@tanstack/react-query";
import { fetchMatters } from "./api";

export function useMatters() {
  return useQuery({
    queryKey: ["matters"],
    queryFn: fetchMatters,
    refetchInterval: 30000,
    refetchIntervalInBackground: false,
  });
}