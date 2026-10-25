// Display formatting only (no scoring logic): 8 -> "8", 7.5 -> "7.5".

export function formatScore(score: number): string {
  return Number.isInteger(score) ? String(score) : score.toFixed(1);
}
