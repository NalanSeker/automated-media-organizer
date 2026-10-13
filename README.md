# Automated Media Organizer

## 1. Project Overview

Automated Media Organizer is a zero-dependency Python command-line application that organizes files from a source directory into categorized destination folders based on their file extensions.

The application aims to reduce digital clutter, save time, prevent accidental file overwrites, and provide an activity history.

## 2. Features

- **Extension-based classification:** Routes files to folders according to their extensions.
- **Automatic directory creation:** Creates destination folders when required.
- **Collision-safe filenames:** Adds numerical suffixes to prevent overwriting existing files.
- **Date-prefix renaming:** Optionally adds the file's last-modified date to its name.
- **Dry-run mode:** Previews planned operations without moving files.
- **Activity logging:** Prints operation details and records successful-mode operations in a log file.
- **Error handling:** Reports filesystem errors and continues processing other files when possible.
- **CLI:** Supports command-line arguments through Python's `argparse` module.

## 3. File Categories

| Category | Extensions | Destination |
|---|---|---|
| Images | `.jpg`, `.png`, `.gif`, `.svg` | `Sorted/Images/` |
| Video | `.mp4`, `.avi`, `.mkv` | `Sorted/Video/` |
| Word | `.doc`, `.docx` | `Sorted/Documents/Word/` |
| PowerPoint | `.ppt`, `.pptx` | `Sorted/Documents/PowerPoint/` |
| Excel | `.xls`, `.xlsx`, `.csv` | `Sorted/Documents/Excel/` |
| PDF | `.pdf` | `Sorted/Documents/PDF/` |
| Text | `.txt` | `Sorted/Documents/Text/` |
| Other documents | `.rtf`, `.odt`, `.md` | `Sorted/Documents/Other/` |
| Archives and code | `.zip`, `.py`, `.js`, `.json` | `Sorted/Archives_Code/` |
| Miscellaneous | Unknown or missing extensions | `Sorted/Misc/` |

Extension matching is case-insensitive.

## 4. Requirements

- Python 3.10 or newer
- No third-party Python packages are required to run the application

The application uses standard-library modules including `argparse`, `os`, `shutil`, `sys`, and `datetime`.

## 5. Project Structure

```text
automated-media-organizer/
├── code.py
├── README.md
├── .gitignore
└── contributions/
    ├── NALAN_SEKER_2309011153_NalanSeker.md
    ├── ELIFSU_BASIBUYUK_2509011065_elifsubasibuyuk.md
    ├── ABDULLAH_AZIZ_2609011046_catnoirabdullah1.md
    └── HATEM_MOHAMED_2309015061_hatemmohamed21.md
```

- `code.py`: Contains the file organization functions and CLI entry point.
- `README.md`: Documents the project's purpose, features, structure, and usage.
- `.gitignore`: Excludes temporary files and generated output from version control.
- `contributions/`: Contains individual team member contribution statements.

The `test_input/`, `test_output/`, `Sorted/`, and `activity.log` paths are runtime or test artifacts and should not be committed.

## 6. Usage

Run commands from the project root directory.

### Preview operations without moving files

```bash
python code.py --source test_input --dest test_output --dry-run
```

### Organize files

```bash
python code.py --source test_input --dest test_output
```

### Add modification dates to filenames

```bash
python code.py --source test_input --dest test_output --date-prefix
```

### Display available arguments

```bash
python code.py --help
```

### Command-line arguments

| Argument | Required | Description |
|---|---|---|
| `--source` | Yes | Source directory containing files to organize |
| `--dest` | No | Destination root directory; defaults to the current directory |
| `--dry-run` | No | Previews operations without moving files |
| `--date-prefix` | No | Prefixes filenames with their last-modified date |

## 7. Main Functions

- `get_clean_extension(file_name)`: Extracts and normalizes the file extension.
- `find_destination_folder(destination_root, extension)`: Resolves the destination directory for an extension.
- `make_unique_file_name(destination_folder, wanted_file_name)`: Generates a unique filename when a destination name already exists.
- `add_date_to_file_name(file_path, file_name)`: Adds the file's last-modified date to its name.
- `write_log_entry(log_file_path, old_path, new_path, dry_run)`: Prints an activity record and appends it to the log outside dry-run mode.
- `organize_files(source_folder, destination_folder, dry_run, date_prefix)`: Validates paths, scans entries, classifies files, performs operations, handles errors, and returns summary counts.
- `create_argument_parser()`: Defines the command-line arguments.
- `main(argv=None)`: Connects parsed arguments to the organizing pipeline and returns an exit status.

## 8. Safety and Error Handling

- The source path must point to an existing directory.
- Subdirectories and symbolic links are skipped.
- Destination filenames are checked before moving files.
- Dry-run mode is intended to preview planned operations without moving files.
- Filesystem errors are reported to the terminal and included in the error count.

Always test the application on a temporary directory before using important folders such as Downloads or Desktop.

## 9. Testing

Manual checks have been performed for dry-run behavior and file organization using sample files.

Further verification should cover:
- Uppercase and lowercase extensions
- Files without extensions
- Unknown extensions
- Existing destination filenames
- Invalid source paths
- Subdirectories and symbolic links
- Date-prefix behavior
- Log persistence across multiple runs

A `pytest` test suite should be added and run before the final submission. Do not consider the test suite complete until its results have been verified.

## 10. Team Contributions

Individual responsibilities are documented in the `contributions/` directory. Each contribution statement should accurately reflect the work completed by that team member.

