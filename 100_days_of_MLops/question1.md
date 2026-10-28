```

The xFusionCorp Industries data science team requires a standardized Python environment for their new machine learning project. Set up a virtual environment on the controlplane host that includes all necessary ML libraries.


The work is done on the controlplane host under /root/code/.

The end state must satisfy the following:

a Python virtual environment named ml-env exists under /root/code/;
the environment has numpy, pandas, scikit-learn, and matplotlib installed;
a requirements.txt capturing the installed packages is saved at /root/code/requirements.txt.


Run the following commands on the controlplane host to create the Python virtual environment, install the required machine learning libraries, and generate requirements.txt.
Step 1: Navigate to the working directory
mkdir -p /root/code
cd /root/code


Step 2: Create the virtual environment
python3 -m venv ml-env


This creates:
/root/code/ml-env/


If venv is unavailable, install the appropriate python3-venv package for your operating system.
Step 3: Activate the virtual environment
source /root/code/ml-env/bin/activate


Your terminal prompt should now show (ml-env).
Step 4: Install the required ML libraries
python -m pip install --upgrade pip
python -m pip install numpy pandas scikit-learn matplotlib


This installs all four libraries and their required dependencies inside ml-env.
Step 5: Generate requirements.txt
python -m pip freeze > /root/code/requirements.txt


This saves the installed packages and their exact versions.
Step 6: Verify the installation
python -m pip list


Test all four libraries:
python -c "import numpy, pandas, sklearn, matplotlib; print('All ML libraries installed successfully!')"


Expected output:
All ML libraries installed successfully!


Step 7: Verify the required files
ls -ld /root/code/ml-env
ls -l /root/code/requirements.txt


Confirm that the requirements file includes the libraries:
grep -E '^(numpy|pandas|scikit-learn|matplotlib)==' /root/code/requirements.txt


One-command solution
If you want to complete the entire task quickly, run:
mkdir -p /root/code && \
cd /root/code && \
python3 -m venv ml-env && \
source ml-env/bin/activate && \
python -m pip install --upgrade pip && \
python -m pip install numpy pandas scikit-learn matplotlib && \
python -m pip freeze > /root/code/requirements.txt


Final checklist
Requirement	Expected result
Virtual environment	/root/code/ml-env
NumPy	Installed
Pandas	Installed
Scikit-learn	Installed
Matplotlib	Installed
Requirements file	/root/code/requirements.txt

Important: Make sure the installation commands finish successfully before clicking FINISH. The libraries must be installed inside the virtual environment, not globally.