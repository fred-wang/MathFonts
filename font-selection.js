const mathfont_list = {
    "Default":  "Default fonts (local only)",
    "Asana": "Asana",
    "Cambria": "Cambria (local only)",
    "DejaVu": "DejaVu",
    "FiraMath": "FiraMath",
    "Garamond": "Garamond",
    "GFS_NeoHellenic": "GFS NeoHellenic",
    "LatinModern": "Latin Modern",
    "LeteSansMath": "Lete Sans Math",
    "Libertinus": "Libertinus",
    "LucidaBright": "Lucida Bright (local only)",
    "NewComputerModern": "New Computer Modern",
    "NewComputerModernSans": "New Computer Modern Sans",
    "Minion": "Minion (local only)",
    "STIX": "STIX",
    "TeXGyreBonum": "TeX Gyre Bonum",
    "TeXGyrePagella": "TeX Gyre Pagella",
    "TeXGyreSchola": "TeX Gyre Schola",
    "TeXGyreTermes": "TeX Gyre Termes",
    "XITS": "XITS",
};

document.addEventListener("DOMContentLoaded", () => {
    let mathfont_link = document.createElement("link");
    mathfont_link.setAttribute("rel", "stylesheet");
    mathfont_link.setAttribute("type", "text/css");
    document.head.appendChild(mathfont_link);

    const mathfont_select = document.querySelector("select.mathfont");
    const mathmlonly_checkbox =
        document.querySelector("input[type='checkbox'].mathmlonly")

    const urlParams = new URLSearchParams(window.location.search);
    const fontFamily = urlParams.get('fontFamily');
    const mathFontOnly = urlParams.get('mathFontOnly') === 'true';
    function updateQueryStrings() {
        const url = new URL(window.location.href);
        if (mathfont_select) {
            if (mathfont_select.value !== "Default") {
              url.searchParams.set('fontFamily',  mathfont_select.value);
            } else {
              url.searchParams.delete('fontFamily');
            }
        }
        if (mathmlonly_checkbox) {
            if (mathmlonly_checkbox.checked) {
                url.searchParams.set('mathFontOnly', mathmlonly_checkbox.checked);
            } else {
              url.searchParams.delete('mathFontOnly');
            }
        }
        window.history.pushState(null /* state */, '' /* unused */, url.toString());
    }

    if (mathfont_select) {
        function updateMathFont()
        {
            let mathfont = mathfont_select.value;
            if (mathfont == "Default")
                mathfont_link.removeAttribute("href");
            else
                mathfont_link.setAttribute("href",
                                           `/MathFonts/${mathfont}/mathfonts.css`);
            updateQueryStrings();
        }
        for (let value in mathfont_list) {
            let option = document.createElement("option");
            option.value = value;
            option.innerText = mathfont_list[value];
            if (value === fontFamily) {
              option.selected = true;
            }
            mathfont_select.appendChild(option);
        }
        updateMathFont();
        mathfont_select.addEventListener("change", updateMathFont);
    }

    if (mathmlonly_checkbox) {
        function updateCheckBox()
        {
            if (mathmlonly_checkbox.checked)
                document.body.removeAttribute("class");
            else
                document.body.setAttribute("class", "htmlmathparagraph");
            updateQueryStrings();
        }
        mathmlonly_checkbox.checked = mathFontOnly;
        updateCheckBox();
        mathmlonly_checkbox.addEventListener("change", updateCheckBox);
    }
});
