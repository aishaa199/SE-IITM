### 1. Set Up Environment for Pytest
It is recommended to use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
## 2. Install Dependencies
```bash
pip install -r test_requirements.txt
##3. Foder to execute
Stay inside backend to execute the pytest scripts
Testscripts are present inside tests folder in backend
##4. Command to execute the scripts
pytest tests/<test_file.py> -s
(e.g. pytest tests/test_service.py -s)
Try to eliminate the errors. DO NOT make any changes to files other than those in the tests folder.
Keep test branch different than the development branch.