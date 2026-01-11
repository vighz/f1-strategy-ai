"use client";

import { DegradationCurve } from "@/lib/types";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface DegradationChartProps {
  curves: DegradationCurve[];
}

const COMPOUND_COLORS: { [key: string]: string } = {
  SOFT: "#FF0000",
  MEDIUM: "#FFFF00",
  HARD: "#FFFFFF",
  INTERMEDIATE: "#00FF00",
  WET: "#00BFFF",
};

export default function DegradationChart({ curves }: DegradationChartProps) {
  if (!curves || curves.length === 0) {
    return (
      <div className="bg-card p-6 rounded-lg">
        <h2 className="text-xl font-bold mb-4">Tyre Degradation</h2>
        <p className="text-gray-400">No degradation data available</p>
      </div>
    );
  }

  // Generate chart data for tyre life 1-40 laps
  const maxTyreLife = 40;
  const chartData = [];

  for (let life = 1; life <= maxTyreLife; life++) {
    const point: any = { tyre_life: life };

    curves.forEach((curve) => {
      const [a, b, c] = curve.coefficients;
      const lapTime = a * life * life + b * life + c;
      point[curve.compound] = lapTime;
    });

    chartData.push(point);
  }

  return (
    <div className="bg-card p-6 rounded-lg">
      <h2 className="text-xl font-bold mb-4">Tyre Degradation</h2>

      <div className="mb-4 space-y-2">
        {curves.map((curve) => (
          <div key={curve.compound} className="text-sm">
            <span
              className="inline-block w-3 h-3 mr-2 rounded-full"
              style={{ backgroundColor: COMPOUND_COLORS[curve.compound] }}
            />
            <span className="font-bold">{curve.compound}:</span>{" "}
            <span className="text-gray-400">
              {curve.deg_per_lap.toFixed(3)}s/lap (R² = {curve.r_squared.toFixed(3)})
            </span>
          </div>
        ))}
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis
            dataKey="tyre_life"
            label={{ value: "Tyre Life (laps)", position: "insideBottom", offset: -5 }}
            stroke="#999"
          />
          <YAxis
            label={{ value: "Lap Time (s)", angle: -90, position: "insideLeft" }}
            stroke="#999"
          />
          <Tooltip
            contentStyle={{ backgroundColor: "#1A1A1A", border: "1px solid #333" }}
          />
          <Legend />
          {curves.map((curve) => (
            <Line
              key={curve.compound}
              type="monotone"
              dataKey={curve.compound}
              stroke={COMPOUND_COLORS[curve.compound]}
              strokeWidth={2}
              dot={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
