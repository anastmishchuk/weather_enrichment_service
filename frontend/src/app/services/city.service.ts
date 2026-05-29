import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { City } from '../models/city.model';

@Injectable({ providedIn: 'root' })
export class CityService {
  private base = '/api/cities';

  constructor(private http: HttpClient) {}

  getCities(): Observable<City[]> {
    return this.http.get<City[]>(this.base);
  }

  addCity(name: string): Observable<City> {
    return this.http.post<City>(this.base, { name });
  }

  refreshWeather(id: number): Observable<void> {
    return this.http.post<void>(`${this.base}/${id}/refresh`, {});
  }
}
