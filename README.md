# Power Format Pack

## Formatting buttons

This add-on adds the following supplementary formatting buttons to Anki:

* a **code** button that will wrap selected text in a `<code>` (default:
    <kbd>Ctrl</kbd> + <kbd>,</kbd>). You can specify the CSS class you want to
    use in combination with `<code>`. For example, we have a CSS class named `c`
    defined in the *Styling* section of *Cards*:


        .c {
            font-family: droid sans mono;
            background-color: #f2f2f2;
            padding-left: 5px;
            padding-right: 5px;
        }

    In the options *Tools &gt; Power Format Pack add-on (options) &gt; CSS
    class for &lt;code&gt; and &lt;pre&gt; code blocks* we can specify the class
    name, so that our `<code>` elements will be automatically transformed to
    `<code class="c">`.

* an **unordered list** button (default <kbd>Ctrl</kbd> + <kbd>[</kbd>):

    * One
    * Two
    * Three

* an **ordered list** button (default <kbd>Ctrl</kbd> + <kbd>]</kbd>):

    1. One
    2. Two
    3. Three

* an **indent** button (default <kbd>Ctrl</kbd> + <kbd>Shift</kbd> +
    <kbd>]</kbd>) to indent text or lists:

    1. One
        * Two
            1. Three

* an **outdent** button (default <kbd>Ctrl</kbd> + <kbd>Shift</kbd> +
    <kbd>[</kbd>) to outdent text or lists

* a **strikethrough** button (default <kbd>Alt</kbd> + <kbd>Shift</kbd> +
    <kbd>5</kbd>):

    <del>strikethrough text example</del>

* a **code block** button (default <kbd>Ctrl</kbd> + <kbd>.</kbd>) that
    creates a `<pre>` block element around the selected element. This works the
    same way the code button works. You can specify the CSS class you want to use
    in combination with `&lt;pre&gt;` by going to *Tools &gt; Power Format Pack
    add-on (options) &gt; CSS class for &lt;code&gt; and &lt;pre&gt; code blocks*

* a **horizontal rule** button (default <kbd>Ctrl</kbd> + <kbd>H</kbd>) that
    inserts a horizontal rule after the current position of the cursor

* a **definition list** button (default <kbd>Ctrl</kbd> + <kbd>Shift</kbd> +
    <kbd>D</kbd>):

    <dl><dt>definition term</dt><dd>definition description</dd>

    Upon clicking the button, a popup will appear where you can enter your terms
    and descriptions.

* a **table** button (default <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>3</kbd>):

    <table>
        <thead>
            <tr>
                <th>header</th>
                <th>header</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>content</td>
                <td>content</td>
            </tr>
        </tbody>
    </table>

    Select the text you want to create a table from. This works very much the
    same as a Markdown list:

        header1 | header2
        -|-
        elem1 | elem2

    This will create a list with two columns and two rows. The `-|-` part is
    optional, but can be used to align the column to the left (`:-`), right
    (`-:`) or to the center (`:-:`). You can skip this line completely, but do
    make sure you add a pipe character `|` between elements to designate
    a border.

    Alternatively, if you do not select any text, upon clicking the
    <kbd>Create a table</kbd> button you will be presented with a dialog
    window asking you to specify the number of rows and columns.

    In the option menu, you can select whether you want your tables to be
    styled by the add-on (default) or if you prefer to use your own style sheet.

* a **keyboard key** button (default <kbd>Ctrl</kbd> + <kbd>Shift</kbd> +
    <kbd>K</kbd>):

    This will create a keyboard key, for example <kbd>Esc</kbd>. By itself,
    the text that is wrapped in `<kbd>` will not look any different from the
    rest of the text. You have to style it first by going to the *Styling*
    section of *Cards* and add CSS to your liking. For example:


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

* a **hyperlink** button (default <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>H</kbd>):

    Upon pressing the button, you will be presented with a dialog window where
    you can enter both a link and text. To unlink a hyperlink, use the unlink
    button.

* a **text highlight** button (default <kbd>Ctrl</kbd> + <kbd>Shift</kbd> +
    <kbd>N</kbd> to select color, <kbd>Ctrl</kbd> + <kbd>Shift</kbd> +
    <kbd>B</kbd> to apply it):

    Highlight your text with colors.

* a **blockquote** button (default <kbd>Ctrl</kbd> + <kbd>Shift</kbd> +
    <kbd>Y</kbd>):

    Cite your source distinctively from the rest of the text. You can add an
    author by putting brackets around the text:

        Do not pray for easy lives. Pray to be stronger men. [[John F. Kennedy]]

    > Do not pray for easy lives. Pray to be stronger men.<br />
    > _John F. Kennedy_

* **alignment** buttons:

    Align your text left, right, center or justified. Shortcuts are
    <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Alt</kbd> + <kbd>L</kbd>,
    <kbd>R</kbd>, <kbd>B</kbd> and <kbd>J</kbd>, respectively.

* a **heading** button (shortcut <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>1</kbd>):

    You can either create a heading by prepending text with hashes: `#` for
    a `<h1>` heading, `######` for a `<h6>` heading. If you do not prepend any
    hashes, or if you select no text at all, a dialog will appear where you
    can create your own heading.

<!-- end formatting buttons -->


## Markdown

You can use Markdown to style your notes. Markdown is a text-to-HTML
conversion tool that lets you quicky style your notes. If you don't know
Markdown yet, have a look at [this tutorial](http://markdowntutorial.com/).

##### Enable Markdown

Markdown is disabled by default, to keep this add-on as modularised as possible. To enable it, go to *Tools > Power Format Pack add-on (options) > Options... > Markdown* and tick the checkbox next to "Markdown". Restart Anki to complete the process.

##### Using Markdown

When you click the Markdown button, your Markdown syntax will be translated
into HTML and displayed. You are now in _Markdown mode_. Markdown mode is
indicated by the changed background color and the warning message under the
field you are editing. In Markdown mode, you cannot use any of the formatting
buttons you would normally have access to. This is done to prevent any
accidental editing of the displayed result. If you want to make changes to the
card, first toggle the Markdown button again and go back to normal mode.

However, if you absolutely need to edit the card in Markdown mode, you can
choose to keep the buttons enabled from the options menu, by ticking the
checkbox _Allow editing of rendered Markdown_.

When you do add text to your card or alter the HTML directly in Markdown mode,
a dialog box will appear asking whether you want to revert to your previous
Markdown syntax, or try to incorperate the changes in your card. Be advised,
however, that the result may lose some of your original Markdown syntax,
especially if the original syntax was complex (footnotes, tables, code
blocks).

To make sure you always return to your original syntax when exiting Markdown
mode, you can check the _Always automatically revert back to saved Markdown_
checkbox in the options. Doing this will never show you the warning dialog box
and will always discard any changes made in Markdown mode.

##### Don't use Markdown in combination with other formatting

I recommend you use either Markdown or the rich formatting buttons, but not
both at the same time. Markdown was designed to be a fast and simple way to
quickly write relatively simple formatted text. As such, it won't know what to
do with complex cards that use formatting unknown to the Markdown
specification. So when clicking the Markdown button, it _will_ erase
formatting that it does not know how to handle. You were warned.

### Extra Markdown syntax

This addons supports some Markdown syntax not found in
[John Gruber's original
Markdown](https://daringfireball.net/projects/markdown/):

#### Code blocks

Code blocks can be created by indenting four spaces with a white line before
and after the code block. The syntax can be specified either by:

    :::java
    public class Test { }

or by using:

    ```python
    def print_me(this):
        print "Printing: ", this
    ```

More (technical) details on code blocks (e.g. highlighting of lines) can be
found on the
[Python Markdown project](https://pythonhosted.org/Markdown/extensions/code_hilite.html).

#### Definition lists

A definition list can be created as follows:

    Apple
    :   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

    Orange
    :   The fruit of an evergreen tree of the genus Citrus.

Make sure there is a white line between the different definitions.

#### Footnotes


    Footnotes[^1] have a label[^@#$%] and the footnote's content.

    [^1]: This is a footnote content.
    [^@#$%]: A footnote on the label: "@#$%".

A footnote label must start with a caret `^` and may contain any inline text
(including spaces) between a set of square brackets `[]`. Only the first caret
has any special meaning.

A footnote content must start with the label followed by a colon and at least
one space. The label used to define the content must exactly match the label
used in the body (including capitalization and white space). The content would
then follow the label either on the same line or on the next line. The content
may contain multiple lines, paragraphs, code blocks, blockquotes and most any
other markdown syntax. The additional lines must be indented one level (four
spaces or one tab).

More (technical) details on footnotes (e.g. multiple blocks of content) can be
found on the
[Python Markdown project](https://pythonhosted.org/Markdown/extensions/footnotes.html).

#### Abbreviations

The Markdown syntax:

    The HTML specification
    is maintained by the W3C.

    *[HTML]: Hyper Text Markup Language
    *[W3C]:  World Wide Web Consortium

will be rendered as:

    <p>The <abbr title="Hyper Text Markup Language">HTML</abbr> specification
    is maintained by the <abbr title="World Wide Web Consortium">W3C</abbr>.</p>

#### Tables

Tables have the same syntax as described above for the table button. Tables
can be styled with CSS in your stylesheet.

#### Attributes

An example attribute list might look like this:

    {: #someid .someclass somekey='some value' }

A word which starts with a hash (`#`) will set the id of an element.

A word which starts with a dot (`.`) will be added to the list of classes
assigned to an element.

A key/value pair (`somekey='some value'`) will assign that pair to the element.

Be aware that while the dot syntax will add to a class, using key/value pairs
will always override the previously defined attribute. Consider the following:

    {: #id1 .class1 id=id2 class="class2 class3" .class4 }

The above example would result in the following attributes being defined:

    id="id2" class="class2 class3 class4"

Say you have a CSS class:

    .large { font-size: 32px; }

You can add this class to a paragraph like this:

    A person often meets his destiny on the road he took to avoid it.
    {: .large}

More (technical) details on attributes (e.g. block-level and inline
attributes) can be found on the [Python Markdown
project](https://pythonhosted.org/Markdown/extensions/attr_list.html).

## Custom user-defined keybindings

You can change the default keybindings to your liking by going to _Tools >
Power Format Pack add-on (options) > Keybindings..._ You will be presented
with a table view of all available functionality on the left and the associated
keyboard shortcuts on the right. To change a particular keybinding, double click
on the shortcut and press the desired keyboard combination.

Be aware that all keyboard combinations will be accepted, although some of them
won't actually work in practice. If you assign the keyboard shortcut 'A' to a
certain functionality, for example, the shortcut won't actually do anything. 

Also keep in mind that there is no check for duplicate keybindings. This means
that when a keybinding is already taken by either your OS, Anki, this add-on, or
some other running program, the result is undefined.

You can sort either on functionality ('Action') or keybindings by clicking on
the appropriate header columns.

If you want to revert to the default keybindings provided by Power Format Pack,
click the 'Restore Defaults' button. You can undo any changes you made and keep
the dialog window open by pressing the 'Reset' button. 'Cancel' will do the same
but will also close the window. Lastly, when you click 'Save', the dialog window
will close and your changes will be applied.

## Disabling unused buttons
The buttons can be enabled or disabled individually in *Tools > Power Format
Pack add-on (options)*, so feel free to disable the buttons you don't use.

## Installation
The preferred way to install is using the
[Anki add-on site](https://ankiweb.net/shared/info/162313389) way by copying the
add-on code (162313389) into Anki (*Tools > Add-ons > Browse & Install...*).
