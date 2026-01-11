/**
 * API client for F1 Strategy Room backend
 */

import {
  DegradationResponse,
  OvertakeResponse,
  RacesResponse,
  StrategyResponse,
} from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchAPI<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return response.json();
}

export async function healthCheck(): Promise<{ status: string }> {
  return fetchAPI("/health");
}

export async function getRaces(year: number): Promise<RacesResponse> {
  return fetchAPI(`/api/races/${year}`);
}

export async function getDegradation(
  year: number,
  race: string,
  session: string = "R"
): Promise<DegradationResponse> {
  return fetchAPI("/api/degradation", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ year, race, session }),
  });
}

export async function getStrategy(
  year: number,
  race: string,
  session: string = "R"
): Promise<StrategyResponse> {
  return fetchAPI("/api/strategy", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ year, race, session }),
  });
}

export async function getOvertakes(
  year: number,
  race: string,
  session: string = "R"
): Promise<OvertakeResponse> {
  return fetchAPI("/api/overtakes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ year, race, session }),
  });
}
