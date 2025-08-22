# A utility for downloading files from a page

"Page Files Downloader" is a Python command-line utility designed to easily download files from a selected page with the ability to select the desired file types.
---

## Usage

There are two ways to run this application: using Docker or locally using Python.

### Option 1: Using Docker (recommended)

This method is the simplest because it automatically handles all dependencies.

**Preliminary requirements:**
* [Docker] must be installed and running on your system (https://www.docker.com/get-started ).

**Step 1: Create a Docker Image**

Clone this repository, navigate to the project directory, and run the following command to create a Docker image. This only needs to be done once.

``bash
docker build -t page-downloader .
``

**Step 2: Launch the app**

Run the following command to launch the interactive loader. The files you uploaded will appear in a new folder named "my_downloads" in your current directory.

``bash
docker run -it --rm -v "$(pwd)/my_downloads:/application/uploaded files" loader page
``

---

### Option 2: Local use (without Docker)

**Preliminary requirements:**
* Python 3.8+
* Git

**Step 1: Clone the repository**
``
clone bash git https://github.com/F4ilji/page-files-downloader.git
cd loader for swap files
``

**Step 2: Create a virtual environment (recommended)**
It is recommended to create a virtual environment to isolate dependencies.
# For macOS/Linux
``bash
python3 -m venv venv
source venv/bin/activate
``

# For Windows
``
python -m venv venv
.\venv\Scripts\activate
``

**Step 3: Install Dependencies**
Install all necessary Python packages from the file `requirements.txt `.
``bash
pip install -r requirements.txt
``

**Step 4: Launch the app**
Run the script by running the command:
``bash
python main.py
``
Your files will be saved in a new folder `downloaded_files' inside the project directory.
