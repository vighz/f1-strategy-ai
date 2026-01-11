/**
 * TypeScript interfaces for F1 Strategy Room
 */

export type Compound = "SOFT" | "MEDIUM" | "HARD" | "INTERMEDIATE" | "WET";

// ============================================================================
// Races API
// ============================================================================

export interface RaceInfo {
  year: number;
  round_number: number;
  race_name: string;
  circuit_name: string;
  country: string;
  date: string;
}

export interface RacesResponse {
  season: number;
  races: RaceInfo[];
}

// ============================================================================
// Degradation API
// ============================================================================

export interface DegradationCurve {
  compound: string;
  coefficients: number[];
  deg_per_lap: number;
  r_squared: number;
  sample_size: number;
}

export interface DegradationResponse {
  race_name: string;
  year: number;
  curves: DegradationCurve[];
  fuel_effect_per_lap: number;
}

// ============================================================================
// Strategy API
// ============================================================================

export interface PitStop {
  lap: number;
  compound_before: string;
  compound_after: string;
}

export interface StrategyStint {
  compound: string;
  start_lap: number;
  end_lap: number;
  laps: number;
}

export interface Strategy {
  strategy_name: string;
  stops: number;
  pit_stops: PitStop[];
  stints: StrategyStint[];
  predicted_time: number;
  time_delta: number;
}

export interface StrategyResponse {
  race_name: string;
  year: number;
  total_laps: number;
  pit_loss_seconds: number;
  strategies: Strategy[];
  fastest_strategy: string;
}

// ============================================================================
// Overtakes API
// ============================================================================

export interface OvertakeZone {
  zone_id: number;
  distance_start: number;
  distance_end: number;
  avg_speed_delta: number;
  overtake_count: number;
  difficulty: string;
  has_drs: boolean;
}

export interface OvertakeResponse {
  race_name: string;
  year: number;
  zones: OvertakeZone[];
  total_overtakes: number;
}
