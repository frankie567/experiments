# Movie Duration by Year Analysis

This experiment analyzes the evolution of movie durations since 1930 using data from the IMDB API.

## Overview

The script fetches movie data from the [IMDB API](https://imdbapi.dev/) and analyzes how movie durations have changed over time. It produces two types of visualizations:

1. **Average duration by year** - Shows the year-over-year trend in movie durations
2. **Average duration by decade** - Shows the broader decadal trends

## Data Source

- **API**: IMDB API (https://api.imdbapi.dev)
- **API Spec**: https://imdbapi.dev/imdbapi.swagger.yaml
- **Data Range**: Movies from 1930 to present
- **Filter**: Only movies (type=MOVIE) with valid runtime data

## Usage

Run the analysis script:

```bash
uv run analyze.py
```

This will:
1. Fetch movie data from the IMDB API for each year since 1930
2. Calculate average durations by year and decade
3. Generate and save visualization plots as PNG files

## Output

The script generates:
- `duration_by_year.png` - Line plot showing average movie duration by year
- `duration_by_decade.png` - Bar chart showing average movie duration by decade
- Console output with statistics and progress information

## Dependencies

- `httpx` - For making API requests
- `matplotlib` - For creating visualizations
- `pandas` - For data analysis and aggregation

Dependencies are declared inline in the script using PEP 723 and automatically installed by `uv`.
