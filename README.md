# COH3-CDN
CDN sources for coh3stats

They are deployed to cdn.coh3stats.com

All images are stored under two versions:
- .png (original)
- .webp (80% quality - still indistiguishble) 

Anything which is under public folder can be found under the root. 
For example webp:
- https://cdn.coh3stats.com/export/icons/races/american/infantry/captain_us_portrait.webp
- https://cdn.coh3stats.com/export_flatten/captain_us_portrait.webp

For example png:
- https://cdn.coh3stats.com/export/icons/races/american/infantry/captain_us_portrait.png
- https://cdn.coh3stats.com/export_flatten/captain_us_portrait.png

### Maps

You can find all maps under `https://cdn.coh3stats.com/maps`:

Where the format is `maps/{map_code}/{map_code}.webp` for example:
- https://cdn.coh3stats.com/maps/benghazi_6p/benghazi_6p.webp

Maps are also marked things on them, there are 3 versions:
```
benghazi_6p.marked.color.webp
benghazi_6p.marked.tm.webp
benghazi_6p.marked.webp
```
*Some maps might not have the marked versions generated yet 

For example:
- https://cdn.coh3stats.com/maps/benghazi_6p/benghazi_6p.marked.webp

## Development
The marked images are taken from [coh-replay-analyzer-discord-bot](https://github.com/Janne252/coh-replay-analyzer-discord-bot/tree/master/data/scenario-preview-images/coh3) project.

### Extract Game Images Workflow (Manual)
A comprehensive GitHub Actions workflow is available to automatically extract and convert game images from Company of Heroes 3. This workflow can be triggered manually and will:

1. Download the COH3 game files using SteamCMD
2. Extract UI.sga archive using AOEMods.Essence tool
3. Convert RRTEX files to WebP format using [coh3-image-extractor](https://github.com/cohstats/coh3-image-extractor)
4. Organize images in both structured (`public/export/`) and flattened (`public/export_flatten/`) directories
5. Automatically create a Pull Request with all extracted images

**To run the workflow:**
1. Go to the "Actions" tab in this repository
2. Select "Extract and Convert Game Images" workflow
3. Click "Run workflow" button
4. Wait for the workflow to complete (may take 1-3 hours depending on download speed)
5. Review and merge the automatically created Pull Request

**Requirements:**
- Repository secrets must be configured:
  - `STEAM_USERNAME_COH3`: Your Steam account username
  - `STEAM_PASSWORD_COH3`: Your Steam account password
- The workflow runs on Windows runners to handle Windows executables
- Requires approximately 60-80 GB of disk space for game files and extraction

**Note:** This workflow is designed for periodic updates when new game versions are released. The extracted images will be automatically converted to WebP format and organized in the appropriate directories.

### Automated .webp conversion and flatten folder
All you have to do is to commit new files in /public/export folder and this will trigger the GH Action which will create a new automated PR.

### Script to sync map images
You can use the provided Python script to automatically sync map images from the coh-replay-analyzer-discord-bot repository and convert them to WebP format.

Requirements:
- Python 3.6 or higher
- pip (Python package installer)

Steps to sync map images:
1. Navigate to the scripts directory:
   ```bash
   cd scripts
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the sync script:
   ```bash
   python sync_map_images.py
   ```

   To overwrite existing files, use the --overwrite flag:
   ```bash
   python sync_map_images.py --overwrite
   ```

The script will:
- Fetch map images from the coh-replay-analyzer-discord-bot repository
- Convert images to WebP format with 85% quality
- Create map-specific folders under public/maps/
- Handle all three image variants (base, colored, and tm)
- Skip existing files unless --overwrite is used
- Print progress and summary information

### Scripts PNG to WebP Conversion
You can use the provided Python script to automatically convert PNG files to WebP format. The script will only convert PNG files that don't already have a WebP version.

Requirements:
- Python 3.6 or higher
- pip (Python package installer)

Steps to use the automated converter:
1. Navigate to the scripts directory:
   ```bash
   cd scripts
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the conversion script:
   ```bash
   python convert_to_webp.py
   ```

The script will:
- Automatically find all PNG files in the public directory and its subdirectories
- Convert only PNG files that don't have a corresponding WebP version
- Use 85% quality for the WebP conversion
- Handle images with transparency
- Print progress information during conversion

Note: This is an alternative to using XnViewMP and provides an automated way to convert only missing WebP files.


### Manual flatten folder copy

To copy the files to the flatten folder you can run these unix commands:
```
cd public
cp export/**/*.webp export_flatten
```

Windows:
```
for /r export %f in (*.webp) do copy /Y "%f" export_flatten\
```

### Converting to .webp using tools
For example you can use this tool https://www.xnview.com/en/xnviewmp/#downloads

Steps:
1. Open the app XnViewMP
2. Tools --> Batch Converter
3. Add Folder (select folder) (select only .png files remove any webp)
4. Click Output tab, format webp, quality 80%
5. Click on Convert

<img width="867" alt="image" src="https://github.com/cohstats/coh3-cdn/assets/8086995/47d18ef4-124c-44c8-85cf-85bb9a402bb6">
<img width="863" alt="image" src="https://github.com/cohstats/coh3-cdn/assets/8086995/4d12ccd8-056a-4dd8-aa58-55c22c5d7304">
<img width="869" alt="image" src="https://github.com/cohstats/coh3-cdn/assets/8086995/48434a05-0659-436c-a6ea-0aef46f9c29e">