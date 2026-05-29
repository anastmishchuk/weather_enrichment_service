import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CityService } from '../../services/city.service';
import { City } from '../../models/city.model';
import { AddCityComponent } from '../add-city/add-city.component';

@Component({
  selector: 'app-city-list',
  standalone: true,
  imports: [CommonModule, AddCityComponent],
  template: `
    <div class="container">
      <h1>Weather Enrichment Service</h1>

      <app-add-city (cityAdded)="loadCities()"></app-add-city>

      <div *ngIf="loading" class="status">Loading…</div>
      <div *ngIf="error" class="status error">{{ error }}</div>

      <table *ngIf="!loading && cities.length > 0">
        <thead>
          <tr>
            <th>City</th>
            <th>Temperature</th>
            <th>Humidity</th>
            <th>Description</th>
            <th>Last Updated</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let city of cities">
            <td>{{ city.name }}</td>
            <td>{{ city.weather ? (city.weather.temperature | number:'1.1-1') + ' °C' : '—' }}</td>
            <td>{{ city.weather ? city.weather.humidity + '%' : '—' }}</td>
            <td>{{ city.weather?.description ?? '—' }}</td>
            <td>{{ city.weather ? (city.weather.fetched_at | date:'d.M.yyyy. HH:mm') : '—' }}</td>
            <td>
              <button (click)="refresh(city)" [disabled]="refreshing[city.id]">
                {{ refreshing[city.id] ? 'Updating…' : 'Refresh' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div *ngIf="!loading && cities.length === 0 && !error" class="status">
        No cities yet. Add one above.
      </div>
    </div>
  `,
  styles: [`
    .container { max-width: 900px; margin: 40px auto; padding: 0 16px; font-family: sans-serif; }
    h1 { margin-bottom: 24px; }
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #e0e0e0; }
    th { background: #f5f5f5; font-weight: 600; }
    button { padding: 6px 12px; background: #388e3c; color: white; border: none; border-radius: 4px; cursor: pointer; }
    button:disabled { opacity: 0.6; cursor: not-allowed; }
    .status { padding: 16px 0; color: #555; }
    .error { color: #c62828; }
  `],
})
export class CityListComponent implements OnInit {
  cities: City[] = [];
  loading = false;
  error = '';
  refreshing: Record<number, boolean> = {};

  constructor(private cityService: CityService) {}

  ngOnInit(): void {
    this.loadCities();
  }

  loadCities(): void {
    this.loading = true;
    this.error = '';
    this.cityService.getCities().subscribe({
      next: (data) => {
        this.cities = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Failed to load cities';
        this.loading = false;
      },
    });
  }

  refresh(city: City): void {
    this.refreshing[city.id] = true;
    this.cityService.refreshWeather(city.id).subscribe({
      next: () => {
        setTimeout(() => {
          this.loadCities();
          delete this.refreshing[city.id];
        }, 3000);
      },
      error: () => {
        delete this.refreshing[city.id];
      },
    });
  }
}
