"use client";

import { Strategy } from "@/lib/types";

interface StrategyRankingProps {
  strategies: Strategy[];
  fastestStrategy: string;
}

const COMPOUND_COLORS: { [key: string]: string } = {
  SOFT: "#FF0000",
  MEDIUM: "#FFFF00",
  HARD: "#FFFFFF",
};

export default function StrategyRanking({
  strategies,
  fastestStrategy,
}: StrategyRankingProps) {
  if (!strategies || strategies.length === 0) {
    return (
      <div className="bg-card p-6 rounded-lg">
        <h2 className="text-xl font-bold mb-4">Strategy Ranking</h2>
        <p className="text-gray-400">No strategy data available</p>
      </div>
    );
  }

  return (
    <div className="bg-card p-6 rounded-lg">
      <h2 className="text-xl font-bold mb-4">Strategy Ranking</h2>
      <p className="text-sm text-gray-400 mb-4">
        Fastest: <span className="text-f1red font-bold">{fastestStrategy}</span>
      </p>

      <div className="space-y-3">
        {strategies.slice(0, 5).map((strategy, index) => (
          <div
            key={index}
            className={`p-4 rounded-lg border ${
              index === 0
                ? "border-f1red bg-f1red/10"
                : "border-gray-700 bg-background"
            }`}
          >
            <div className="flex justify-between items-start mb-2">
              <div>
                <span className="font-bold text-lg">#{index + 1}</span>
                <span className="ml-3">{strategy.strategy_name}</span>
              </div>
              <div className="text-right">
                <div className="font-mono">
                  {(strategy.predicted_time / 60).toFixed(2)} min
                </div>
                {index > 0 && (
                  <div className="text-sm text-gray-400">
                    +{strategy.time_delta.toFixed(2)}s
                  </div>
                )}
              </div>
            </div>

            <div className="flex gap-2 mt-2">
              {strategy.stints.map((stint, stintIdx) => (
                <div
                  key={stintIdx}
                  className="flex-1 px-2 py-1 rounded text-xs text-center font-bold"
                  style={{
                    backgroundColor: COMPOUND_COLORS[stint.compound] || "#666",
                    color: stint.compound === "MEDIUM" ? "#000" : "#FFF",
                  }}
                >
                  {stint.compound.slice(0, 1)} ({stint.laps}L)
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
