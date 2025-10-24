import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface PCSetup {
  id: number;
  user?: number;
  cpu: string;
  gpu: string;
  ram: number;
  storage_type: string;
  cooling?: string;
  psu?: string;
  created_at?: string;
}

export interface Game {
  id: number;
  name: string;
  genre?: string;
  developer?: string;
  release_year?: number;
  min_cpu?: string;
  min_gpu?: string;
  min_ram?: number;
}

export interface Prediction {
  predicted_fps: number;
  cpu_usage: number;
  gpu_usage: number;
  temperature: number;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) { }

  getPCSetups(): Observable<PCSetup[]> {
    return this.http.get<PCSetup[]>(`${this.apiUrl}/pcsetups/`);
  }

  getGames(): Observable<Game[]> {
    return this.http.get<Game[]>(`${this.apiUrl}/games/`);
  }

  predictPerformance(setupId: number, gameId: number): Observable<Prediction> {
    return this.http.get<Prediction>(`${this.apiUrl}/predict/?setup_id=${setupId}&game_id=${gameId}`);
  }
}
