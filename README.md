# Shazam API v5 song list fetch
Easy batch retrieval of your [myshazam library](https://www.shazam.com/myshazam)

## Direct run
### Prerequisites
1. Install python 3.8 and the required prerequisites from requirements.txt file
2. Place your own urls.txt file (formatted as one url per line) under ./mnt directory
3. Set 'SEMAPHORE' env variable for asyncio module (if not set, default of 25 is used)
## Docker (from inside project directory)
### Build (not necessary, can directly run)
docker build -t shazamapiv5fetchsongs .
### Run from windows cmd
docker run -v %cd%\mnt:/app/mnt --env SEMAPHORE=50 --network="host" --name shazamapiv5fetchsongs shazamapiv5fetchsongs:latest
### Run from linux bash
docker run -v $(pwd)/mnt:/app/mnt --env SEMAPHORE=50 --network="host" --name shazamapiv5fetchsongs shazamapiv5fetchsongs:latest
# Donating

If you found this project useful, consider buying me a coffee

<a href="https://www.buymeacoffee.com/diman82" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/black_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>