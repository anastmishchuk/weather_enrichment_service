export interface WeatherSnapshot {
  temperature: number | null;
  humidity: number | null;
  description: string | null;
  fetched_at: string;
}

export interface City {
  id: number;
  name: string;
  created_at: string;
  weather: WeatherSnapshot | null;
}
