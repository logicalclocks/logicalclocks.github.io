# Linked tabs and CSS text-transform

Material links content tabs (`content.tabs.link`) by comparing label text with `innerText`. `innerText` carries CSS text transforms on rendered elements but not on hidden ones, so a label uppercased by CSS reads "PYTHON" where it is visible and "Python" in every hidden set, and a switch made on the visible set never reaches the others (only labels that are already uppercase, like "CLI", keep working). The home stepper hit this: switching on step 3 left steps 1 and 2 on the old tab.

Never put `text-transform` on a linked tab label. Write the label text as it should display and style the rest (font, weight, size).
