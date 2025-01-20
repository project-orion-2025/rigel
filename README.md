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