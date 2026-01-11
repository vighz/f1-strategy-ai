"use client";

import { useState } from "react";
import DegradationChart from "@/components/DegradationChart";
import RaceSelector from "@/components/RaceSelector";
import StrategyRanking from "@/components/StrategyRanking";
import { getDegradation, getStrategy } from "@/lib/api";
import { DegradationResponse, RaceInfo, StrategyResponse } from "@/lib/types";

export default function Home() {
  const [selectedYear] = useState(2023);
  const [selectedRace, setSelectedRace] = useState<RaceInfo | null>(null);
  const [degradationData, setDegradationData] =
    useState<DegradationResponse | null>(null);
  const [strategyData, setStrategyData] = useState<StrategyResponse | null>(
    null
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleRaceSelect(race: RaceInfo) {
    setSelectedRace(race);
    setLoading(true);
    setError(null);

    try {
      // Fetch degradation and strategy data in parallel
      const [degData, stratData] = await Promise.all([
        getDegradation(race.year, race.circuit_name),
        getStrategy(race.year, race.circuit_name),
      ]);

      setDegradationData(degData);
      setStrategyData(stratData);
    } catch (err) {
      setError("Failed to load race data. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 text-f1red">
            F1 Strategy Room
          </h1>
          <p className="text-gray-400">
            Turn F1 telemetry into race-winning strategy insights
          </p>
        </div>

        {/* Race Selector */}
        <div className="mb-6">
          <RaceSelector
            selectedYear={selectedYear}
            onRaceSelect={handleRaceSelect}
          />
        </div>

        {/* Selected Race Info */}
        {selectedRace && (
          <div className="bg-card p-4 rounded-lg mb-6">
            <h2 className="text-2xl font-bold">{selectedRace.race_name}</h2>
            <p className="text-gray-400">
              {selectedRace.circuit_name}, {selectedRace.country} |{" "}
              {selectedRace.date}
            </p>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="bg-card p-8 rounded-lg text-center">
            <p className="text-gray-400">
              Analyzing race data... This may take 30-60 seconds on first load.
            </p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-card p-8 rounded-lg text-center">
            <p className="text-red-400">{error}</p>
          </div>
        )}

        {/* Data Display */}
        {!loading && !error && degradationData && strategyData && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Degradation Chart */}
            <div className="lg:col-span-2">
              <DegradationChart curves={degradationData.curves} />
            </div>

            {/* Strategy Ranking */}
            <div className="lg:col-span-2">
              <StrategyRanking
                strategies={strategyData.strategies}
                fastestStrategy={strategyData.fastest_strategy}
              />
            </div>

            {/* Model Caveats */}
            <div className="lg:col-span-2 bg-card p-6 rounded-lg border border-yellow-600/30">
              <h3 className="text-lg font-bold mb-3 text-yellow-500">
                ⚠️ Model Assumptions
              </h3>
              <ul className="text-sm text-gray-400 space-y-1">
                <li>
                  • Fuel effect estimated at {degradationData.fuel_effect_per_lap}
                  s/lap (may vary by circuit)
                </li>
                <li>• Track evolution not modeled</li>
                <li>• Traffic effects filtered but not perfectly</li>
                <li>• Aggregates all drivers (individual deg varies)</li>
                <li>• Weather assumed constant within session</li>
                <li>
                  • Model suggests trends, not exact predictions for future races
                </li>
              </ul>
            </div>
          </div>
        )}

        {/* Initial State */}
        {!selectedRace && !loading && (
          <div className="bg-card p-8 rounded-lg text-center">
            <p className="text-gray-400">Select a race to begin analysis</p>
          </div>
        )}
      </div>
    </main>
  );
}
