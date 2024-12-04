let mathfont_list = {
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

    let mathfont_select = document.querySelector("select.mathfont");
    if (mathfont_select) {
        function updateMathFont()
        {
            let mathfont = mathfont_select.value;
            if (mathfont == "Default")
                mathfont_link.removeAttribute("href");
            else
                mathfont_link.setAttribute("href",
                                           `/MathFonts/${mathfont}/mathfonts.css`);
        }
        for (let value in mathfont_list) {
            let option = document.createElement("option");
            option.setAttribute("value", value);
            option.innerText = mathfont_list[value];
            mathfont_select.appendChild(option);
        }
        updateMathFont();
        mathfont_select.addEventListener("change", updateMathFont);
    }

    let mathmlonly_checkbox =
        document.querySelector("input[type='checkbox'].mathmlonly")
    if (mathmlonly_checkbox) {
        function updateCheckBox()
        {
            if (mathmlonly_checkbox.checked)
                document.body.removeAttribute("class");
            else
                document.body.setAttribute("class", "htmlmathparagraph");
        }
        updateCheckBox();
        mathmlonly_checkbox.addEventListener("change", updateCheckBox);
    }
});
