## Player Rating and Evaluation Systems for Ultimate Frisbee

This Repository contains all code needed to replicate my work in creating player rating and evaluation systems for profesional Ultimate Frisbee.

In order to successfully recreate the model, follow these steps.

1. Ensure you have the needed libraries to all code
     - Install the AUDL API by running `pip install audl` in a notebook or in a terminal
     - It require a veriosn of pandas older than 2.0 to work
2.  Get Data
     - Open the file `getting_data.ipynb`
     - In the second cell, change filenames to your desired CSV filenames
     - run the notebook
     - It will only get play-by-play stats for one year (2024 by default), you can rerun the whole notebook or just the play-by-play section, changing the value for `year_for_play_by_play` in cell 2
3. Get positional classifications
    - open file `classifying_by_position.ipynb`
     - In Cell 2, set filenames for your career stats file and the file to save with career stats with positional predictions
     - Either run the whole file to replicate the experiment or results or if you just want prediction run cells 1-3 and then run cell with comment #RUN HERE on top of the cell
4. Run Mixed Model
     - Open file called `mixed_model.ipynb`
     - In cell 2 change filenames as appropriate
     - It will by default get rating over the course of the entire league history. If you want to replicate the results from the paper (2021-2024) then uncomment the last line in the third cell before running the notebook.
5. Run On-Off Model
      - For every year that you are running this model make sure that you have a separate file named yearplaydata.csv for example for 2024 it would be 2024playdata.csv
      - Open file called `on off model .ipynb`
      - Set correct filenames in cell 2
      - Run the entire Notebook
6. Make Visualization that are presnt in paper
      - open the file called `visualizing results.ipynb`
      - Change the filenames to your file names in cell 2
      - run the notebook
7. Make a web app with updated results
     - In the file called `web_app_temp.py` replace the filenames in lines
     - To run the app, in a terminal you need to navigate to the correct folder and run `streamlit run web_app_temp.py`
     - If t doesn't redirect you to the page immediately then, click the link or enter the ip address in a browser


Notes: 
- step 2 may take about 1 hour to run. Step 5 may take 10-20 minutes depending on your computer. The other steps can all be run in about 5 minutes or less.
- the current file names that are in the notebooks can work with the exception of the play by play data
- all data files are also located in this github repo with names that will work in the files, which can allow you to start at any step in the process
