from IPython.display import HTML
import random

"""
Provides a function that can be called within a
Jupyter Notebook cell to hide its input but still
display its outbook. Intended use is solution
cells in D-Lab workshops.

Made from code taken and tweaked from both
[here](https://stackoverflow.com/questions/31517194/how-to-hide-one-specific-cell-input-or-output-in-ipython-notebook)
and [here](https://stackoverflow.com/questions/27934885/how-to-hide-code-from-cells-in-ipython-notebook-visualized-with-nbviewer).
"""


def hide_solution():
    """
    When called in a cell, hides that cell's input
    (as intended, this would be solution code in
    D-Lab workshop exercises) and provides
    a toggle button for revealing and hiding the input.
    """
    html = '''<script>
            code_show=true; 
            function code_toggle() {
             if (code_show){
             $('div.cell.code_cell.rendered.selected div.input').hide();
             } else {
             $('div.cell.code_cell.rendered.selected div.input').show();
             }
             code_show = !code_show
            } 
            $( document ).ready(code_toggle);
            </script>
            <form action="javascript:code_toggle()"><input type="submit" value="CLICK TO TOGGLE SOLUTION"></form>'''
    return HTML(html)


def hide_solution_broken(for_next=False):
    this_cell = """$('div.cell.code_cell.rendered.selected')"""
    next_cell = this_cell + '.next()'

    toggle_text = 'CLICK TO TOGGLE SOLUTION'  # text shown on toggle link
    target_cell = this_cell  # target cell to control with toggle
    js_hide_current = ''  # bit of JS to permanently hide code in current cell (only when toggling next cell)

    if for_next:
        target_cell = next_cell
        toggle_text += ' next cell'
        js_hide_current = this_cell + '.find("div.input").show();'

    js_f_name = 'code_toggle_{}'.format(str(random.randint(1,2**64)))

    html = """
        <script>
            function {f_name}() {{
                {cell_selector}.find('div.input').toggle();
            }}

            {js_hide_current}
        </script>

        <a href="javascript:{f_name}()">{toggle_text}</a>
    """.format(
        f_name=js_f_name,
        cell_selector=target_cell,
        js_hide_current=js_hide_current, 
        toggle_text=toggle_text
    )
    
    return HTML(html)