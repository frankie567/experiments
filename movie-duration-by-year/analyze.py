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
"""

import httpx
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from typing import List, Dict, Any


BASE_URL = "https://api.imdbapi.dev"
CURRENT_YEAR = datetime.now().year


def fetch_movies_for_year(year: int, min_votes: int = 500) -> List[Dict[str, Any]]:
    """
    Fetch all movies for a specific year from the IMDB API.
    
    Args:
        year: The year to fetch movies for
        min_votes: Minimum vote count to filter quality movies (default: 500)
    
    Returns:
        List of movie dictionaries with their data
    """
    all_movies = []
    page_token = None
    
    print(f"Fetching movies for {year}...", end=" ", flush=True)
    
    while True:
        params = {
            "types": "MOVIE",
            "startYear": year,
            "endYear": year,
            "minVoteCount": min_votes,
        }
        
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
    Extract year and duration data from movies.
    
    Args:
        movies: List of movie dictionaries
    
    Returns:
        List of dictionaries with year and duration in minutes
    """
    data = []
    for movie in movies:
        runtime_seconds = movie.get("runtimeSeconds")
        start_year = movie.get("startYear")
        
        # Only include movies with valid runtime and year
        if runtime_seconds and start_year and runtime_seconds > 0:
            duration_minutes = runtime_seconds / 60
            data.append({
                "year": start_year,
                "duration_minutes": duration_minutes,
            })
    
    return data


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


def fetch_all_movies(start_year: int = 1930, end_year: int = None, min_votes: int = 500) -> pd.DataFrame:
    """
    Fetch movies for all years in the specified range.
    
    Args:
        start_year: First year to fetch (default: 1930)
        end_year: Last year to fetch (default: current year)
        min_votes: Minimum vote count to filter quality movies (default: 500)
    
    Returns:
        DataFrame with movie duration data
    """
    if end_year is None:
        end_year = CURRENT_YEAR
    
    all_data = []
    
    print(f"\nFetching movie data from {start_year} to {end_year}...")
    print(f"Using minVoteCount={min_votes} to focus on well-known movies")
    print("=" * 60)
    
    for year in range(start_year, end_year + 1):
        movies = fetch_movies_for_year(year, min_votes=min_votes)
        year_data = extract_duration_data(movies)
        all_data.extend(year_data)
    
    print("=" * 60)
    print(f"Total movies collected: {len(all_data)}")
    
    return pd.DataFrame(all_data)


def calculate_statistics(df: pd.DataFrame) -> None:
    """
    Calculate and print statistics about the data.
    
    Args:
        df: DataFrame with movie data
    """
    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)
    
    yearly_avg = df.groupby("year")["duration_minutes"].mean()
    
    print(f"Total movies analyzed: {len(df)}")
    print(f"Year range: {df['year'].min()} - {df['year'].max()}")
    print(f"Overall average duration: {df['duration_minutes'].mean():.1f} minutes")
    print(f"Shortest average year: {yearly_avg.idxmin()} ({yearly_avg.min():.1f} min)")
    print(f"Longest average year: {yearly_avg.idxmax()} ({yearly_avg.max():.1f} min)")
    
    # Decade statistics
    df_with_decade = add_decade_column(df.copy())
    decade_avg = df_with_decade.groupby("decade")["duration_minutes"].mean()
    
    print(f"\nShortest average decade: {int(decade_avg.idxmin())}s ({decade_avg.min():.1f} min)")
    print(f"Longest average decade: {int(decade_avg.idxmax())}s ({decade_avg.max():.1f} min)")
    print("=" * 60)


def plot_by_year(df: pd.DataFrame, output_file: str = "duration_by_year.png") -> None:
    """
    Create a plot showing average movie duration by year.
    
    Args:
        df: DataFrame with movie data
        output_file: Output filename for the plot
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
    
    plt.title('Average Movie Duration by Year (1930-Present)', fontsize=14, fontweight='bold')
    fig.tight_layout()
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved plot: {output_file}")
    plt.close()


def plot_by_decade(df: pd.DataFrame, output_file: str = "duration_by_decade.png") -> None:
    """
    Create a plot showing average movie duration by decade.
    
    Args:
        df: DataFrame with movie data
        output_file: Output filename for the plot
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
    
    plt.title('Average Movie Duration by Decade (1930s-Present)', fontsize=14, fontweight='bold')
    fig.tight_layout()
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved plot: {output_file}")
    plt.close()


def main():
    """Main execution function."""
    print("\n" + "=" * 60)
    print("MOVIE DURATION ANALYSIS")
    print("Analyzing the evolution of movie durations since 1930")
    print("=" * 60)
    
    # Fetch all movie data with higher vote threshold for faster processing
    # Using minVoteCount=500 to focus on popular movies and reduce API calls
    df = fetch_all_movies(start_year=1930, min_votes=500)
    
    if df.empty:
        print("\n❌ No data collected. Exiting.")
        return
    
    # Calculate and display statistics
    calculate_statistics(df)
    
    # Create visualizations
    print("\nGenerating visualizations...")
    plot_by_year(df)
    plot_by_decade(df)
    
    print("\n" + "=" * 60)
    print("✓ Analysis complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
