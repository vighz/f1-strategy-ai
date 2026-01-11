"use client";

import { useEffect, useState } from "react";
import { getRaces } from "@/lib/api";
import { RaceInfo } from "@/lib/types";

interface RaceSelectorProps {
  onRaceSelect: (race: RaceInfo) => void;
  selectedYear: number;
}

export default function RaceSelector({
  onRaceSelect,
  selectedYear,
}: RaceSelectorProps) {
  const [races, setRaces] = useState<RaceInfo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchRaces() {
      setLoading(true);
      setError(null);
      try {
        const data = await getRaces(selectedYear);
        setRaces(data.races);
      } catch (err) {
        setError("Failed to load races");
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchRaces();
  }, [selectedYear]);

  if (loading) {
    return (
      <div className="bg-card p-4 rounded-lg">
        <p className="text-gray-400">Loading races...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-card p-4 rounded-lg">
        <p className="text-red-400">{error}</p>
      </div>
    );
  }

  return (
    <div className="bg-card p-6 rounded-lg">
      <h2 className="text-xl font-bold mb-4">Select Race</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        {races.map((race) => (
          <button
            key={race.round_number}
            onClick={() => onRaceSelect(race)}
            className="bg-background hover:bg-f1red hover:text-white transition-colors p-3 rounded text-left"
          >
            <div className="font-bold text-sm">{race.race_name}</div>
            <div className="text-xs text-gray-400">{race.circuit_name}</div>
          </button>
        ))}
      </div>
    </div>
  );
}
