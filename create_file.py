import csv
import json
import os
from pathlib import Path

def create_notebook(day, date, phases, lessons, study_time, resources, daily_task, assignment, cumulative_project, project_task, milestone):
    """Create a Jupyter notebook with a markdown cell containing the day's information."""
    
    # Create notebook structure
    notebook = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    # Create markdown content
    markdown_content = f"""# Day {day}: {date}

## Phase(s)
{phases}

## Lessons Covered
{lessons}

## Est. Study Time (hrs)
{study_time}

## Resources (links)
{resources}

## Daily Task
{daily_task}

## Assignment
{assignment}

## Cumulative Project
{cumulative_project}

## Project Application Task
{project_task}
"""
    
    if milestone:
        markdown_content += f"""
## Milestone
{milestone}
"""
    
    # Add markdown cell
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": markdown_content.split('\n')
    })
    
    return notebook

def parse_phases(phases_str):
    """Parse the phases string and return a list of phase identifiers."""
    phases = []
    if '|' in phases_str:
        phase_parts = phases_str.split('|')
        for part in phase_parts:
            # Extract phase number (e.g., "P0: Setup & Tooling" -> "P0")
            phase_num = part.strip().split(':')[0]
            phases.append(phase_num)
    else:
        # Single phase
        phase_num = phases_str.strip().split(':')[0]
        phases.append(phase_num)
    return phases

def phase_to_dir(phase_num):
    """Convert phase number to directory name."""
    # P0 -> phase_00, P1 -> phase_01, etc.
    num = int(phase_num[1:])  # Extract number after 'P'
    return f"phase_{num:02d}"

def main():
    csv_file = "/Users/absyd/mystfs/cs/ai/coursingggs_/AI_ENG_FROM_SCRATCH/aies_final - Schedule.csv"
    base_dir = "/Users/absyd/mystfs/cs/ai/coursingggs_/AI_ENG_FROM_SCRATCH"
    
    # Read CSV file
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            day = row['Day']
            date = row['Date']
            phases_str = row['Phase(s)']
            lessons = row['Lessons Covered']
            study_time = row['Est. Study Time (hrs)']
            resources = row['Resources (links)']
            daily_task = row['Daily Task']
            assignment = row['Assignment']
            cumulative_project = row['Cumulative Project']
            project_task = row['Project Application Task']
            milestone = row['Milestone']
            
            # Parse phases
            phases = parse_phases(phases_str)
            
            # Create notebook for each phase this day belongs to
            for phase in phases:
                phase_dir = phase_to_dir(phase)
                phase_path = os.path.join(base_dir, phase_dir)
                
                # Create phase directory if it doesn't exist
                os.makedirs(phase_path, exist_ok=True)
                
                # Create notebook
                notebook = create_notebook(
                    day, date, phases_str, lessons, study_time, resources,
                    daily_task, assignment, cumulative_project, project_task, milestone
                )
                
                # Save notebook
                notebook_filename = f"day_{day.zfill(2)}.ipynb"
                notebook_path = os.path.join(phase_path, notebook_filename)
                
                with open(notebook_path, 'w', encoding='utf-8') as nb_file:
                    json.dump(notebook, nb_file, indent=1)
                
                print(f"Created notebook: {notebook_path}")

if __name__ == "__main__":
    main()