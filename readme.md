<h2>Introduction</h2>
This project has a script how execute the clone of projects from git and search a specific expression defined by user in the content  newly downloaded.
 
<h2>Environment Configuration 🚧</h2> 
1) **First**  you must prepare the environment. How the script is written in **python**, you will need install them in your local station. 
    - The installation and configuration of the python is simple and uncomplicated, do this as instructs in this [link](www.python.org);
2) If you has correctly installed the python, install the library GitPython, do this as this [link] instruct.

<h2>Execution  🚀</h2>
This project have three principal file: **clone.py**, **search.py** and **main.py**.
1) **clone.py**  (``python clone.py``):
    - Clone all projects inserted in a file ".csv" named as "*repositories.csv*". So, to defined who repositories you want to clone, just update this file.
        The file *repositories.csv* have two columns, the first with the **repository** and the secoend with the **branch** to be cloned.
    - This script have a specific logic to select the *branch*, if you no have informed them in the file *repositories.csv*, or if the *branch* informed is not exists to the respective repository.
      > **Warning:** In tihis case, the *script* will try clone from *branch* ***development***, if it is not founded the *script* will try the *branch* ***master***, if it is not founded the *script* will do the clone from default branch of the repository.
    - You can run this script in isolation (``python clone.py``), so you just do the clone of the projects from git.
2) **search.py** (``python search.py``):
    - This *script* execute the search of specific word (defined by user) in a specific folder of files (defined by user too);
    - After the end, a file named '***results.csv***' will generated with the results of the search.
      - The first column from this file have the name of the project;
          - It is just the root folder of the file scanned;
      - The second column have the absolute path from the file;
      - The third column have the line where was founded de result;
      - The fourth column have the format from dependency founded;
          - This value is suppressed case if is not possible defined them.
      - In the fifth column will have the content of the line fonded;
         - The contents with mor 800 characters is will suppressed.
3) **main.py** (``python main.py``):
   - It's a facilitator. It's run the two previous scripts (**clone.py** and **search.py**) in the sequence.
    


Enjoy 😎 God bless you 🙌.