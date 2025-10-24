import { Component, signal, OnInit } from '@angular/core';
import { ApiService, PCSetup, Game, Prediction } from './api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  standalone: false,
  styleUrl: './app.css'
})
export class App implements OnInit {
  protected readonly title = signal('Neural Gaming');
  pcSetups = signal<PCSetup[]>([]);
  games = signal<Game[]>([]);
  selectedSetup = signal<PCSetup | null>(null);
  selectedGame = signal<Game | null>(null);
  prediction = signal<Prediction | null>(null);
  loading = signal(false);

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.apiService.getPCSetups().subscribe(setups => {
      this.pcSetups.set(setups);
    });

    this.apiService.getGames().subscribe(games => {
      this.games.set(games);
    });
  }

  selectSetup(setup: PCSetup) {
    this.selectedSetup.set(setup);
    this.predictIfReady();
  }

  selectGame(game: Game) {
    this.selectedGame.set(game);
    this.predictIfReady();
  }

  predictIfReady() {
    if (this.selectedSetup() && this.selectedGame()) {
      this.loading.set(true);
      this.apiService.predictPerformance(this.selectedSetup()!.id, this.selectedGame()!.id)
        .subscribe(prediction => {
          this.prediction.set(prediction);
          this.loading.set(false);
        });
    }
  }
}
