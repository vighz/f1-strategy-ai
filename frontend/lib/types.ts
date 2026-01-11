/**
 * TypeScript interfaces for F1 Strategy Room
 */

export type Compound = "SOFT" | "MEDIUM" | "HARD" | "INTERMEDIATE" | "WET";

export interface LapData {
  driver: string;
  lap_number: number;
  lap_time: number | null;
  compound: Compound;
  tyre_life: number | null;
  is_personal_best: boolean;
}

export interface StintLap {
  lap_time: number | null;
  tyre_life: number | null;
}

export interface Stint {
  stint_number: number;
  compound: Compound;
  start_lap: number;
  end_lap: number;
  laps: StintLap[];
}

export interface DegradationCurve {
  compound: Compound;
  coefficients: [number, number, number];
  deg_per_lap: number;
  r_squared: number;
}
