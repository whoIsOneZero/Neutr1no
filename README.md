# Neutr1no
Neutr1no is a python-based network vulnerability assessment tool in script form.

## How to set up
1. **Download and install Nmap**:  
  [Nmap website](https://nmap.org/download)

2. **Register for an API key with Vulners**  
  - Website - https://vulners.com/
  - Insert the API key in the `.env` file

3. **Clone repo and install dependencies**:
    ```sh
    # clone the repository
    git clone https://github.com/Ar1t/Neutr1no.git

    # or download the zipped project folder and extract the files

    # Navigate to the project directory
    cd Desktop/security_projects/Neutr1no/

    # create a virtual environment to isolate the project dependencies
    python3 -m venv my_venv

    # activate the virtual environment.
    my_venv\Scripts\activate # Windows:
  
    source my_venv/bin/activate # macOS/Linux:

    # install the required dependencies
    pip install -r requirements.txt
    ```

3. **Run the program**:
    ```sh
    python main.py
    ```
  
## How to use
- After running the code, follow prompts,
- After port scanning, it will take about 2 mins (max) to return a list of vulnerabilities.
  
## Contributing
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
  
