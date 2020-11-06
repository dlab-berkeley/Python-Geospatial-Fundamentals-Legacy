from IPython.display import display, HTML

"""
Provides a function that can be called within a
Jupyter Notebook cell to hide its input but still
display its outbook. Intended use is solution
cells in D-Lab workshops.

Made from code taken and tweaked from both
[here](https://stackoverflow.com/questions/31517194/how-to-hide-one-specific-cell-input-or-output-in-ipython-notebook)
and [here](https://stackoverflow.com/questions/27934885/how-to-hide-code-from-cells-in-ipython-notebook-visualized-with-nbviewer) and [here](https://www.xspdf.com/help/50518335.html).
"""


def hide_solution():
    """
    When called in a cell, hides that cell's input
    (as intended, this would be solution code in
    D-Lab workshop exercises) and provides
    a toggle button for revealing and hiding the input.
    """
    toggle_code_str = '''
    <form action="javascript:code_toggle()"><input type="submit" id="toggleButton" value="CLICK TO TOGGLE SOLUTION"></form>
    '''

    toggle_code_prepare_str = '''
        <script>
        function code_toggle() {
            if ($('div.cell.code_cell.rendered.selected div.input').css('display')!='none'){
                $('div.cell.code_cell.rendered.selected div.input').hide();
            } else {
                $('div.cell.code_cell.rendered.selected div.input').show();
            }
        }
        </script>

    '''

    return display(HTML(toggle_code_prepare_str + toggle_code_str))


