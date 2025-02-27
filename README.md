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



To copy the files to the flatten folder you can run these unix commands:
```
cd public
cp export/**/*.webp export_flatten
```

Windows:
```
for /r export %f in (*.webp) do copy /Y "%f" export_flatten\
```


### Converting to .webp 
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

### Automated PNG to WebP Conversion
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




