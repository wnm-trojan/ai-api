import { useEffect, useState } from "react";
import { fetchHealth } from "@/services/apiClient";
import type { HealthResponse } from "@/types/api";

export function useHealth() {
  const [health, setHealth] = useState<HealthResponse | null>(null);

  useEffect(() => {
    fetchHealth<HealthResponse>()
      .then(setHealth)
      .catch(() => setHealth({ status: "unreachable" }));
  }, []);

  return health;
}
