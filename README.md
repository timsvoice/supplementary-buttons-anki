
This add-on adds the following supplementary formatting buttons to Anki:

* a **code** button that will wrap selected text in a `<code>` (shortcut: <kbd>Ctrl</kbd> + <kbd>,</kbd>). You can specify the CSS class you want to use in combination with `<code>`. For example, we have a CSS class named `c` defined in the *Styling* section of *Cards*:


        .c {
            font-family: droid sans mono;
            background-color: #f2f2f2;
            padding-left: 5px;
            padding-right: 5px;
        }

    In the options *Tools &gt; Supplementary buttons add-on (options) &gt; Alter &lt;code&gt; CSS...* we can specify the class name, so that our `<code>` elements will be automatically transformed to `<code class="c">`.

* an **unordered list** button (shortcut <kbd>Ctrl</kbd> + <kbd>[</kbd>):

    * One
    * Two
    * Three

* an **ordered list** button (shortcut <kbd>Ctrl</kbd> + <kbd>]</kbd>):

    1. One
    2. Two
    3. Three

* an **indent** button (shortcut <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>]</kbd>) to indent text or lists:

    1. One
        * Two
            1. Three

* an **outdent** button (shortcut <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>[</kbd>) to outdent text or lists

* a **strikethrough** button (shortcut <kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>5</kbd>):

    ~~strikethrough text example~~

* a **code block** button (shortcut <kbd>Ctrl</kbd> + <kbd>.</kbd>) that creates a `<pre>` block element around the selected element. This works the same way the code button works. You can specify the CSS class you want to use in combination with <code>&lt;pre&gt;</code> by going to <i>Tools &gt; Supplementary buttons add-on (options) &gt; Alter &lt;code&gt; CSS...</i>

* a **horizontal rule** button (shortcut <kbd>Ctrl</kbd> + <kbd>H</kbd>) that inserts a horizontal rule after the current position of the cursor

* a **definition list** button (shortcut <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>D</kbd>):

    <dl><dt>definition term</dt><dd>definition description</dd>

    Upon clicking the button, a popup will appear where you can enter your terms and descriptions.

* a **table** button (shortcut <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>3</kbd>):

    header | header
    --- | ---
    content | content
    
    Select the text you want to create a table from. This works very much the same as a Markdown list: 
    
        header1 | header2
        -|-
        elem1 | elem2
    
    This will create a list with two columns and two rows. The `-|-` part is optional, but can be used to align the column to the left (`:-`), right (`-:`) or to the center (`:-:`). You can skip this line completely, but do make sure you add a pipe character `|` between elements to designate a border.
    
    Alternatively, if you do not select any text, upon clicking the <kbd>Create a table</kbd> button you will be presented with a dialog window asking you to specify the number of rows and columns.
    
* a **keyboard key** button (shortcut <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>K</kbd>):
    
    This will create a keyboard key, for example <kbd>Esc</kbd>. By itself, the text that is wrapped in `<kbd>` will not look any different from the rest of the text. You have to style it first by going to the *Styling* section of *Cards* and add CSS to your liking. For example:


        kbd {
            box-shadow: inset 0px 1px 0px 0px #ffffff;
            background: -webkit-gradient(linear, left top, left bottom, color-stop(0.05, #f9f9f9), color-stop(1, #e9e9e9) );
            background-color: #f9f9f9;
            border-radius: 5px;
            border: 1px solid #dcdcdc;
            display: inline-block;
            font-size: 0.8em;
            height: 30px;
            line-height: 30px;
            padding: 0px 10px;
            text-align: center;
            text-shadow: 1px 1px 0px #ffffff;
        }

* a **hyperlink** button (shortcut <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>H</kbd>):

    Upon pressing the button, you will be presented with a dialog window where you can enter both a link and text.
    
* a **text highlight** button (shortcut <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>N</kbd> to select color, <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>B</kbd> to apply it):

    Highlight your text with any color you would like. On Linux, you are able to select all the text at once and apply highlighting. Due to an obscure bug in Anki, on Windows and Mac OS X you cannot select more than one line of text at a time.

The buttons can be enabled or disabled individually in *Tools > Supplementary buttons add-on (options)*, so feel free to disable the buttons you don't use.

To add this add-on to Anki, copy the file `extra_buttons.py` to your Anki add-on folder. On Linux,this is   `$HOME/Anki/addon` by default.
