This add-on adds the following supplementary formatting buttons to Anki:

* a **code** button that will wrap selected text in a `<code>` (shortcut: **Ctrl+,**). You can specify the CSS class you want to use in combination with `<code>`. For example, we have a CSS class named `c` defined in the *Styling* section of *Cards*:

        .c {
            font-family: droid sans mono;
            background-color: #f2f2f2;
            padding-left: 5px;
            padding-right: 5px;
        }

    In the options *Tools &gt; Supplementary buttons add-on (options) &gt; Alter &lt;code&gt; CSS...* we can specify the class name, so that our `<code>` elements will be automatically transformed to `<code class="c">`.

* an **unordered list** button (shortcut **Ctrl+[**):

    * One
    * Two
    * Three

* an **ordered list** button (shortcut **Ctrl+]**):

    1. One
    2. Two
    3. Three

* an **indent** button (shortcut **Ctrl+Shift+I**) to indent text or lists:

    1. One
        * Two
            1. Three

* an **outdent** button (shortcut **Ctrl+Shift+O**) to outdent text or lists

* a **strikethrough** button (shortcut **Alt+Shift+5**):

    ~~strikethrough text example~~

* a **code block** button (shortcut **Ctrl+.**) that creates a `<pre>` block element around the selected element

* a **horizontal rule** button (shortcut **Ctrl+H**) that inserts a horizontal rule after the current position of the cursor

The buttons can be enabled or disabled individually in *Tools > Supplementary buttons add-on (options)*, so feel free to disable the buttons you don't use.

To add this add-on to Anki, copy the file `extra_buttons.py` to your Anki add-on folder, by default on Linux `$HOME/Anki/addon`.
