# Timetable Images Folder

## Purpose
This folder contains timetable images that are displayed on the timetable page when users select their semester and section.

## File Naming Convention
Timetable images **must** follow this exact naming format:

```
Semester [NUMBER] - Section [LETTER].jpeg
```

### Examples:
- `Semester 1 - Section A.jpeg`
- `Semester 1 - Section B.jpeg`
- `Semester 2 - Section A.jpeg`
- `Semester 2 - Section E.jpeg`
- `Semester 3 - Section C.jpeg`

## Important Notes:
1. **File Extension**: Use `.jpeg` (not `.jpg` or `.png`)
2. **Spacing**: Include spaces around the dash (` - `)
3. **Case Sensitive**: Use capital letters for "Semester" and "Section"
4. **Section Format**: Use "Section A", "Section B", etc. (not just "A" or "B")

## How It Works:
When a user selects a semester and section from the dropdown menus and clicks "Load Timetable", the system will look for an image file matching the pattern above.

For example:
- If user selects "Semester 2" and "Section E"
- The system will look for: `Semester 2 - Section E.jpeg`

## Adding New Timetables:
1. Create or obtain your timetable image
2. Name it according to the convention above
3. Save it in this folder
4. The timetable will automatically be available for selection

## Sample File:
A sample timetable image has been included: `Semester 2 - Section E.jpeg`
