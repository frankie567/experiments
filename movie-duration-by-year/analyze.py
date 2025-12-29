#!/usr/bin/env python3
# /// script
# dependencies = [
#   "httpx>=0.27.0",
#   "matplotlib>=3.9.0",
#   "pandas>=2.2.0",
# ]
# ///
"""
Movie Duration Analysis Script

This script fetches movie data from the IMDB API and analyzes how movie durations
have evolved since 1930. It generates visualizations showing average durations
by year and by decade.

Uses stratified random sampling to ensure statistical accuracy across different eras,
avoiding bias from the internet era having more votes.
"""

import httpx
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from typing import List, Dict, Any


BASE_URL = "https://api.imdbapi.dev"
CURRENT_YEAR = datetime.now().year


def fetch_movies_for_year(year: int, min_votes: int = 0) -> List[Dict[str, Any]]:
    """
    Fetch all movies for a specific year from the IMDB API.
    
    Args:
        year: The year to fetch movies for
        min_votes: Minimum vote count to filter movies (default: 0 for no filtering)
    
    Returns:
        List of movie dictionaries with their data including vote counts
    """
    all_movies = []
    page_token = None
    
    print(f"Fetching movies for {year}...", end=" ", flush=True)
    
    while True:
        params = {
            "types": "MOVIE",
            "startYear": year,
            "endYear": year,
        }
        
        if min_votes > 0:
            params["minVoteCount"] = min_votes
        
        if page_token:
            params["pageToken"] = page_token
        
        try:
            response = httpx.get(f"{BASE_URL}/titles", params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            
            titles = data.get("titles", [])
            all_movies.extend(titles)
            
            page_token = data.get("nextPageToken")
            if not page_token:
                break
                
        except (httpx.HTTPError, httpx.TimeoutException, httpx.RequestError) as e:
            print(f"Error fetching year {year}: {e}")
            break
    
    print(f"✓ {len(all_movies)} movies")
    return all_movies


def extract_duration_data(movies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extract year, duration, and vote count data from movies.
    
    Args:
        movies: List of movie dictionaries
    
    Returns:
        List of dictionaries with year, duration in minutes, and vote count
    """
    data = []
    for movie in movies:
        runtime_seconds = movie.get("runtimeSeconds")
        start_year = movie.get("startYear")
        rating = movie.get("rating", {})
        vote_count = rating.get("voteCount", 0) if rating else 0
        
        # Only include movies with valid runtime and year
        if runtime_seconds and start_year and runtime_seconds > 0:
            duration_minutes = runtime_seconds / 60
            data.append({
                "year": start_year,
                "duration_minutes": duration_minutes,
                "vote_count": vote_count,
            })
    
    return data


def apply_stratified_sampling(df: pd.DataFrame, sample_size: int = 50) -> pd.DataFrame:
    """
    Apply stratified random sampling to ensure equal representation across years.
    
    For years with fewer movies than sample_size, includes all movies.
    For years with more movies, randomly samples sample_size movies.
    
    Args:
        df: DataFrame with movie data
        sample_size: Number of movies to sample per year (default: 50)
    
    Returns:
        DataFrame with sampled movies
    """
    sampled_data = []
    
    for year in df['year'].unique():
        year_df = df[df['year'] == year]
        
        if len(year_df) <= sample_size:
            # Include all movies if fewer than sample_size
            sampled_data.append(year_df)
        else:
            # Random sample without replacement
            sampled = year_df.sample(n=sample_size, random_state=42)
            sampled_data.append(sampled)
    
    return pd.concat(sampled_data, ignore_index=True)


def add_decade_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a decade column to the dataframe.
    
    Args:
        df: DataFrame with year column
    
    Returns:
        DataFrame with decade column added
    """
    df["decade"] = (df["year"] // 10) * 10
    return df


def fetch_all_movies(start_year: int = 1930, end_year: int = None, min_votes: int = 0) -> pd.DataFrame:
    """
    Fetch movies for all years in the specified range.
    
    Args:
        start_year: First year to fetch (default: 1930)
        end_year: Last year to fetch (default: current year)
        min_votes: Minimum vote count to filter movies (default: 0 for no filtering)
    
    Returns:
        DataFrame with movie duration data
    """
    if end_year is None:
        end_year = CURRENT_YEAR
    
    all_data = []
    
    print(f"\nFetching movie data from {start_year} to {end_year}...")
    if min_votes > 0:
        print(f"Using minVoteCount={min_votes} as initial filter")
    else:
        print("Fetching all movies (no vote threshold)")
    print("=" * 60)
    
    for year in range(start_year, end_year + 1):
        movies = fetch_movies_for_year(year, min_votes=min_votes)
        year_data = extract_duration_data(movies)
        all_data.extend(year_data)
    
    print("=" * 60)
    print(f"Total movies collected: {len(all_data)}")
    
    return pd.DataFrame(all_data)


def calculate_statistics(df: pd.DataFrame, title: str = "STATISTICS") -> None:
    """
    Calculate and print statistics about the data.
    
    Args:
        df: DataFrame with movie data
        title: Title for the statistics section
    """
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    
    yearly_avg = df.groupby("year")["duration_minutes"].mean()
    yearly_count = df.groupby("year").size()
    
    print(f"Total movies analyzed: {len(df)}")
    print(f"Year range: {df['year'].min()} - {df['year'].max()}")
    print(f"Overall average duration: {df['duration_minutes'].mean():.1f} minutes")
    print(f"Shortest average year: {yearly_avg.idxmin()} ({yearly_avg.min():.1f} min)")
    print(f"Longest average year: {yearly_avg.idxmax()} ({yearly_avg.max():.1f} min)")
    print(f"Min movies per year: {yearly_count.min()}")
    print(f"Max movies per year: {yearly_count.max()}")
    print(f"Average movies per year: {yearly_count.mean():.0f}")
    
    # Decade statistics
    df_with_decade = add_decade_column(df.copy())
    decade_avg = df_with_decade.groupby("decade")["duration_minutes"].mean()
    
    print(f"\nShortest average decade: {int(decade_avg.idxmin())}s ({decade_avg.min():.1f} min)")
    print(f"Longest average decade: {int(decade_avg.idxmax())}s ({decade_avg.max():.1f} min)")
    print("=" * 60)


def plot_by_year(df: pd.DataFrame, output_file: str = "duration_by_year.png", title_suffix: str = "") -> None:
    """
    Create a plot showing average movie duration by year.
    
    Args:
        df: DataFrame with movie data
        output_file: Output filename for the plot
        title_suffix: Optional suffix to add to the plot title
    """
    yearly_avg = df.groupby("year")["duration_minutes"].mean()
    yearly_count = df.groupby("year").size()
    
    fig, ax1 = plt.subplots(figsize=(14, 6))
    
    color = 'tab:blue'
    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Average Duration (minutes)', color=color, fontsize=12)
    ax1.plot(yearly_avg.index, yearly_avg.values, color=color, linewidth=2, label='Average Duration')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)
    
    # Add second y-axis for movie count
    ax2 = ax1.twinx()
    color = 'tab:orange'
    ax2.set_ylabel('Number of Movies', color=color, fontsize=12)
    ax2.bar(yearly_count.index, yearly_count.values, color=color, alpha=0.3, label='Movie Count')
    ax2.tick_params(axis='y', labelcolor=color)
    
    title = f'Average Movie Duration by Year (1930-Present){title_suffix}'
    plt.title(title, fontsize=14, fontweight='bold')
    fig.tight_layout()
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved plot: {output_file}")
    plt.close()


def plot_by_decade(df: pd.DataFrame, output_file: str = "duration_by_decade.png", title_suffix: str = "") -> None:
    """
    Create a plot showing average movie duration by decade.
    
    Args:
        df: DataFrame with movie data
        output_file: Output filename for the plot
        title_suffix: Optional suffix to add to the plot title
    """
    df_with_decade = add_decade_column(df.copy())
    decade_avg = df_with_decade.groupby("decade")["duration_minutes"].mean()
    decade_count = df_with_decade.groupby("decade").size()
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    x = [f"{int(d)}s" for d in decade_avg.index]
    x_pos = range(len(x))
    
    color = 'tab:blue'
    ax1.set_xlabel('Decade', fontsize=12)
    ax1.set_ylabel('Average Duration (minutes)', color=color, fontsize=12)
    bars1 = ax1.bar(x_pos, decade_avg.values, color=color, alpha=0.7, label='Average Duration')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(x, rotation=45)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for i, v in enumerate(decade_avg.values):
        ax1.text(i, v + 1, f'{v:.1f}', ha='center', va='bottom', fontsize=9)
    
    # Add second y-axis for movie count
    ax2 = ax1.twinx()
    color = 'tab:orange'
    ax2.set_ylabel('Number of Movies', color=color, fontsize=12)
    ax2.plot(x_pos, decade_count.values, color=color, marker='o', linewidth=2, 
             markersize=8, label='Movie Count')
    ax2.tick_params(axis='y', labelcolor=color)
    
    title = f'Average Movie Duration by Decade (1930s-Present){title_suffix}'
    plt.title(title, fontsize=14, fontweight='bold')
    fig.tight_layout()
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved plot: {output_file}")
    plt.close()


def main():
    """Main execution function."""
    print("\n" + "=" * 60)
    print("MOVIE DURATION ANALYSIS")
    print("Analyzing the evolution of movie durations since 1930")
    print("Using stratified sampling to avoid internet-era bias")
    print("=" * 60)
    
    # Fetch all movie data with low vote threshold to get a broader sample
    # Using minVoteCount=10 to filter out extremely obscure entries while
    # still capturing a wide range of movies across all eras
    df_all = fetch_all_movies(start_year=1930, min_votes=10)
    
    if df_all.empty:
        print("\n❌ No data collected. Exiting.")
        return
    
    # Show statistics for all data
    calculate_statistics(df_all, "STATISTICS (All Movies with 10+ Votes)")
    
    # Apply stratified sampling to get equal representation per year
    print("\n" + "=" * 60)
    print("Applying stratified random sampling (50 movies per year)...")
    print("This ensures equal representation across all eras")
    print("=" * 60)
    
    df_sampled = apply_stratified_sampling(df_all, sample_size=50)
    
    # Show statistics for sampled data
    calculate_statistics(df_sampled, "STATISTICS (Stratified Sample)")
    
    # Create visualizations for sampled data
    print("\nGenerating visualizations from stratified sample...")
    plot_by_year(df_sampled, "duration_by_year.png", " - Stratified Sample")
    plot_by_decade(df_sampled, "duration_by_decade.png", " - Stratified Sample")
    
    print("\n" + "=" * 60)
    print("✓ Analysis complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
