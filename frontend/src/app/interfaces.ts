interface Episode {
  primary_title: string;
  season_number: number;
  episode_number: number;
  average_rating: string;
}

export interface Title {
  primary_title: string;
  episodes: Episode[];
}
