# TU Delft thesis - MMX thesis plotting - minimum working example

This repository offers a minimum working example for a Python plotting tool which may be used with the [TU Delft thesis template](https://www.tudelft.nl/en/tu-delft-corporate-design/downloads/). This code enables plots with the [Utopia](https://www.fonts.com/font/adobe/utopia/story) font used in the TU Delft thesis template or any other font that is selected in the beginning of the plotting file.

<p align="center">
<img src="https://github.com/HaralDev/TUDelft_thesis_plotting/blob/main/EM1_motor_lifetest.png" width="600">
  <br>Figure 1: Motor test example (compressed PNG file)
</p>

# Example plot
Figure 1 shows an example from my thesis. The code is found the bottom `minimum_working.py` and the raw data is in `data_file_example.csv`. The plot contains two axes subplots, with the top one divided into two, resulting in three subplots. The x-axes is shared and the y-axes are different for every subplot. Each subplot has its own legend. 

# Sizing of plots and fonts
See [this article](https://jwalton.info/Embed-Publication-Matplotlib-Latex/) for explanation of the `set_size` function and about font sizing. It comes down to defining the number you would use in Latex in `\includegraphics[width=0.5\textwidth]{my-uploaded-figure.png}`([at Overleaf](https://www.overleaf.com/learn/latex/Inserting_Images)), the **0.5** in this case, as the width of the figure. Matplotlib then ensures that the text size in the figure is the same as the text size.


I altered `set_size` function slightly to ensure I could change the height of the plots (sometimes I needed thinner, longer plots). 

# Installs
- `pip install pandas matplotlib seaborn scipy`
- Download [Utopia font](https://www.fonts.com/font/adobe/utopia/story)
- Recommended: [Visual Studio Code](https://code.visualstudio.com/) 
# Tips
- Structure: I used a `.py` file to write the code for all my plots and a `.ipynb` notebook to execute the plotting functions and organise myself. This resulted in a very structured and easy to understand notebook with all my plots (Figure 2). 
- Plot in `pdf` format, from the beginning, **always**. 
- Use wise filenames, I suggest including the `get_timestamp` so that you know when you plotted it. 

<p align="center">
<img src="https://github.com/HaralDev/TUDelft_thesis_plotting/blob/main/visual_studio_plot_notebook.png" width="800">
  <br>Figure 2: Example of structured notebook
</p>

