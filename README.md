## New buttons

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

    Upon pressing the button, you will be presented with a dialog window where you can enter both a link and text. To unlink a hyperlink, use the unlink button.
    
* a **text highlight** button (shortcut <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>N</kbd> to select color, <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>B</kbd> to apply it):

    Highlight your text with any color you would like.
    
* a **blockquote** button (shortcut <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Y</kbd>):

    Cite your source distinctively from the rest of the text. You can add an author by putting brackets around the text:
    
        Do not pray for easy lives. Pray to be stronger men. [[John F. Kennedy]]
    
    > Do not pray for easy lives. Pray to be stronger men.  
    > _John F. Kennedy_

* **alignment** buttons:

    Align your text left, right, center or justified. Shortcuts are <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Alt</kbd> + <kbd>L</kbd>, <kbd>R</kbd>, <kbd>B</kbd> and <kbd>J</kbd>, respectively.
    
* a **heading** button (shortcut <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>1</kbd>):

    You can either create a heading by prepending text with hashes: `#` for a `<h1>` heading, `######` for a `<h6>` heading. If you do not prepend any hashes, or if you select no text at all, a dialog will appear where you can create your own heading.

## Custom user-defined keybindings

You can change the default keybindings by editing the `keybinding.json` file in your `Anki/addons/extra_buttons` folder.  Please keep in mind that there is no check for duplicate keybindings. This means that when a keybinding is already taken by either your OS, Anki, this addon, or some other running program, the result is undefined.

This file needs to contain valid JSON. Basically this means that the key-value pairs should be enclosed in double quotes:

    "key": "value"

The opening and closing braces in the file `{` and `}` are mandatory. Each key-value pair should contain a colon `:` and should end with a comma, except for the last pair. See the file for valid examples.

Invalid JSON cannot be parsed and will result in the use of the default keybindings. If you find that your new keybindings don't work (i.e. they don't show up in Anki, despite you changing this file), please use a JSON validator to check for faulty JSON.

Modifier keys that can be used include: the function keys (`F1` through `F12`), `Ctrl`, `Alt`, `Shift`, ASCII alphanumeric characters, and ASCII punctuation characters. For Mac OS X, be advised that `Ctrl` maps to the <kbd>Cmd</kbd> key (or "Apple key"), NOT to <kbd>Ctrl</kbd>. If you want to use the <kbd>Ctrl</kbd> key on Mac OS X, use `Meta` instead. So, `Ctrl+Shift+[` on Linux or Windows maps to `Meta+Shift+[` on Mac OS X. The string `Ctrl+Shift+[` on Mac OS X will require you to type <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>[</kbd> in Anki. Please make sure you understand this before opening bug reports.

The use of an invalid key sequence will silently revert the sequence to the default setting. For example, invalid sequences are:

* only modifier keys: `Ctrl+Shift`
* empty sequence
* non-existing modifier keys: `Ctrl+Iota+j`

The order or case of the string sequence is unimportant. `Ctrl+Alt+p` is the same as `ALT+CTRL+P` or even `p+Ctrl+Alt`.

If you want to revert your changes to the default keybindings provided by Supplementary Buttons for Anki, please remove the keybindings JSON file in your addon folder.

## Disabling unused buttons

The buttons can be enabled or disabled individually in *Tools > Supplementary buttons add-on (options)*, so feel free to disable the buttons you don't use.

## Installation

The preferred way to install is using the [Anki add-on site](https://ankiweb.net/shared/info/162313389) way by copying the addon code (162313389) into Anki (*Tools > Add-ons > Browse & Install...*).
