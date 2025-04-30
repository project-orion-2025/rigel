### Setting Up the `PYTHONPATH` for Local Development

To make sure the `configs` module is always available, you can set the `PYTHONPATH` permanently by adding it to your shell configuration file.

#### Instructions for macOS/Linux:

1. **Open your terminal**.

2. **Edit your shell configuration file**:
    - For **bash** (default on many systems):
      ```bash
      nano ~/.bashrc
      ```
    - For **zsh** (default on newer macOS versions):
      ```bash
      nano ~/.zshrc
      ```

3. **Add the following line at the end of the file**:
   ```bash
   export PYTHONPATH=$PYTHONPATH:/Users/kushidhar/Projects/project_orion/automation_pytest

---

```pip freeze > requirements.txt```


---

```text
VIRTUAL ENV SETUP
python3 -m venv venv  
     
source venv/bin/activate 

pip3 install -r requirements.txt 

pytest tests_question_api

deactivate
```

#### Instructions for Windows

1. **Open cmd or PowerShell**

2. **Set PYTHONPATH locally or in environment variables.**
    - For cmd
    ```bash
    set PYTHONPATH=%PYTHONPATH%;C:\Users\kushidhar\Projects\project_orion\automation_pytest
    ```
    - For PowerShell
   ```bash
   $env:PYTHONPATH="$env:PYTHONPATH;C:\Users\kushidhar\Projects\project_orion\automation_pytest"
   ```

3. **Virtual environment setup**
    ```text
    VIRTUAL ENV SETUP
    python -m venv venv  
         
    venv/Scripts/activate.ps1 (For PowerShell)
    venv/Scripts/activate.bat (For cmd)
    
    pip install -r requirements.txt 
    
    pytest tests_question_api
    
    deactivate
    ```
