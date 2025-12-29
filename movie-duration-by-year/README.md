# Movie Duration by Year Analysis

This experiment analyzes the evolution of movie durations since 1930 using data from the IMDB API.

## Overview

The script fetches movie data from the [IMDB API](https://imdbapi.dev/) and analyzes how movie durations have changed over time. It produces two types of visualizations:

1. **Average duration by year** - Shows the year-over-year trend in movie durations
2. **Average duration by decade** - Shows the broader decadal trends

## Methodology

To ensure statistical accuracy across different eras, this analysis uses **stratified random sampling**:

1. **Initial filtering**: Fetches movies with at least 10 votes to exclude extremely obscure entries
2. **Stratified sampling**: Randomly samples up to 50 movies per year to ensure equal representation
3. **Bias mitigation**: This approach avoids the internet-era bias where post-2000 movies naturally have more votes

This methodology addresses the concern that simply filtering by vote count (e.g., minVoteCount=500) creates a sampling bias, since movies from the internet era (2000+) are much more likely to have high vote counts than older films, even if they're of comparable quality or popularity for their time.

## Data Source

- **API**: IMDB API (https://api.imdbapi.dev)
- **API Spec**: https://imdbapi.dev/imdbapi.swagger.yaml
- **Data Range**: Movies from 1930 to present
- **Filter**: Only movies (type=MOVIE) with at least 10 votes and valid runtime data
- **Sampling**: Random sample of up to 50 movies per year

## Usage

Run the analysis script:

```bash
uv run analyze.py
```

This will:
1. Fetch movie data from the IMDB API for each year since 1930
2. Apply stratified random sampling to ensure equal representation
3. Calculate average durations by year and decade
4. Generate and save visualization plots as PNG files

## Output

The script generates:
- `duration_by_year.png` - Line plot showing average movie duration by year with stratified sampling
- `duration_by_decade.png` - Bar chart showing average movie duration by decade with stratified sampling
- Console output with statistics and progress information

## Dependencies

- `httpx` - For making API requests
- `matplotlib` - For creating visualizations
- `pandas` - For data analysis and aggregation
- `numpy` - For random sampling operations

Dependencies are declared inline in the script using PEP 723 and automatically installed by `uv`.
