import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CityService } from '../../services/city.service';

@Component({
  selector: 'app-add-city',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <form (ngSubmit)="submit()" class="add-form">
      <input
        [(ngModel)]="cityName"
        name="cityName"
        placeholder="Enter city name"
        required
        [disabled]="loading"
      />
      <button type="submit" [disabled]="loading || !cityName.trim()">
        {{ loading ? 'Adding…' : 'Add City' }}
      </button>
      <span class="error" *ngIf="error">{{ error }}</span>
    </form>
  `,
  styles: [`
    .add-form { display: flex; gap: 8px; align-items: center; margin-bottom: 24px; }
    input { padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px; flex: 1; max-width: 300px; }
    button { padding: 8px 16px; background: #1976d2; color: white; border: none; border-radius: 4px; cursor: pointer; }
    button:disabled { opacity: 0.6; cursor: not-allowed; }
    .error { color: #c62828; font-size: 13px; }
  `],
})
export class AddCityComponent {
  @Output() cityAdded = new EventEmitter<void>();

  cityName = '';
  loading = false;
  error = '';

  constructor(private cityService: CityService) {}

  submit(): void {
    if (!this.cityName.trim()) return;
    this.loading = true;
    this.error = '';
    this.cityService.addCity(this.cityName.trim()).subscribe({
      next: () => {
        this.cityName = '';
        this.loading = false;
        this.cityAdded.emit();
      },
      error: (err) => {
        this.error = err?.error?.detail ?? 'Failed to add city';
        this.loading = false;
      },
    });
  }
}
