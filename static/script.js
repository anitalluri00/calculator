// static/script.js

// Auto detect dark/light
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.setAttribute('data-theme', 'dark');
}

// Manual toggle
document.getElementById('theme-button').addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    document.documentElement.setAttribute('data-theme', currentTheme === 'dark' ? 'light' : 'dark');
});

// Scientific Calculator
function calculate() {
    const expression = document.getElementById('calc-input').value;
    const mode = document.getElementById('mode-select').value;
    fetch('/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expression: expression, mode: mode })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('calc-result').innerText = `Result: ${data.result}`;
    });
}

// Populate Units
const units = {
    length: ['meter', 'kilometer', 'centimeter', 'millimeter', 'mile', 'yard', 'foot', 'inch'],
    weight: ['kilogram', 'gram', 'milligram', 'pound', 'ounce'],
    area: ['sq_meter', 'sq_kilometer', 'sq_centimeter', 'sq_millimeter', 'sq_mile', 'sq_yard', 'sq_foot', 'sq_inch'],
    volume: ['cubic_meter', 'liter', 'milliliter', 'cubic_inch', 'cubic_foot', 'gallon']
};

function populateUnits() {
    const category = document.getElementById('unit-category').value;
    const fromUnit = document.getElementById('from-unit');
    const toUnit = document.getElementById('to-unit');
    fromUnit.innerHTML = '';
    toUnit.innerHTML = '';
    units[category].forEach(unit => {
        fromUnit.innerHTML += `<option value="${unit}">${unit}</option>`;
        toUnit.innerHTML += `<option value="${unit}">${unit}</option>`;
    });
}
populateUnits();

// Unit Conversion
function convertUnits() {
    const value = document.getElementById('unit-value').value;
    const fromUnit = document.getElementById('from-unit').value;
    const toUnit = document.getElementById('to-unit').value;
    const category = document.getElementById('unit-category').value;
    fetch('/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ value, from_unit: fromUnit, to_unit: toUnit, category })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('unit-result').innerText = `Result: ${data.result}`;
    });
}

// Currency Conversion
function convertCurrency() {
    const amount = document.getElementById('curr-amount').value;
    const fromCurr = document.getElementById('from-curr').value;
    const toCurr = document.getElementById('to-curr').value;
    fetch('/currency', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount, from_currency: fromCurr, to_currency: toCurr })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('curr-result').innerText = `Result: ${data.result}`;
    });
}
