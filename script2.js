document.addEventListener('DOMContentLoaded', function() {
    // Элементы DOM
    const datePicker = document.getElementById('datePicker');
    const todayBtn = document.getElementById('todayBtn');
    const amountInput = document.getElementById('amount');
    const fromCurrency = document.getElementById('fromCurrency');
    const toCurrency = document.getElementById('toCurrency');
    const resultInput = document.getElementById('result');
    const convertBtn = document.getElementById('convertBtn');
    const swapBtn = document.getElementById('swapCurrencies');
    const ratesBody = document.getElementById('ratesBody');

    // Установка сегодняшней даты по умолчанию
    const today = new Date();
    const formattedToday = formatDate(today);
    datePicker.value = formattedToday;
    datePicker.max = formattedToday;

    // Хранение курсов валют
    let currentRates = {
        date: '',
        RUB: 1,
        USD: 0,
        EUR: 0,
        GBP: 0,
        CNY: 0,
        JPY: 0
    };

    // Загрузка курсов валют при старте
    loadExchangeRates();

    // События
    datePicker.addEventListener('change', function() {
        const selectedDate = this.value;
        loadExchangeRates(selectedDate);
    });

    todayBtn.addEventListener('click', function() {
        datePicker.value = formattedToday;
        loadExchangeRates();
    });

    convertBtn.addEventListener('click', convert);

    swapBtn.addEventListener('click', function() {
        const temp = fromCurrency.value;
        fromCurrency.value = toCurrency.value;
        toCurrency.value = temp;
        convert();
    });

    amountInput.addEventListener('input', convert);
    fromCurrency.addEventListener('change', convert);
    toCurrency.addEventListener('change', convert);

    // Функция загрузки курсов валют
    async function loadExchangeRates(date) {
        try {
            let url = 'https://www.cbr-xml-daily.ru/daily_json.js';

            if (date) {
                const formattedDate = date.split('-').reverse().join('/');
                url = `https://www.cbr-xml-daily.ru/archive/${date.split('-').join('/')}/daily_json.js`;
            }

            const response = await fetch(url);

            if (!response.ok) {
                throw new Error('Не удалось загрузить курсы валют');
            }

            const data = await response.json();

            // Обновляем дату
            currentRates.date = data.Date ? data.Date.split('T')[0] : '';

            // Обновляем курсы валют
            if (data.Valute) {
                currentRates.USD = data.Valute.USD.Value / data.Valute.USD.Nominal;
                currentRates.EUR = data.Valute.EUR.Value / data.Valute.EUR.Nominal;
                currentRates.GBP = data.Valute.GBP.Value / data.Valute.GBP.Nominal;
                currentRates.CNY = data.Valute.CNY.Value / data.Valute.CNY.Nominal;
                currentRates.JPY = data.Valute.JPY.Value / data.Valute.JPY.Nominal;
            }

            updateRatesTable();
            convert();

        } catch (error) {
            console.error('Ошибка загрузки курсов:', error);
            alert('Не удалось загрузить курсы валют. Попробуйте позже.');
        }
    }

    // Функция конвертации валют
    function convert() {
        if (!currentRates.date) return;

        const amount = parseFloat(amountInput.value) || 0;
        const from = fromCurrency.value;
        const to = toCurrency.value;

        if (from === to) {
            resultInput.value = amount.toFixed(2);
            return;
        }

        try {
            const fromRate = currentRates[from];
            const toRate = currentRates[to];

            if (!fromRate || !toRate) {
                throw new Error('Не удалось получить курс для выбранных валют');
            }

            let result;
            if (from === 'RUB') {
                result = amount / toRate;
            } else if (to === 'RUB') {
                result = amount * fromRate;
            } else {
                const rubAmount = amount * fromRate;
                result = rubAmount / toRate;
            }

            resultInput.value = result.toFixed(2);

        } catch (error) {
            console.error('Ошибка конвертации:', error);
            resultInput.value = 'Ошибка';
        }
    }

    // Функция обновления таблицы курсов
    function updateRatesTable() {
        if (!ratesBody) return;

        ratesBody.innerHTML = '';

        const currencies = [
            { code: 'USD', name: 'Доллар США' },
            { code: 'EUR', name: 'Евро' },
            { code: 'GBP', name: 'Фунт стерлингов' },
            { code: 'CNY', name: 'Китайский юань' },
            { code: 'JPY', name: 'Японская йена' }
        ];

        currencies.forEach(currency => {
            const rate = currentRates[currency.code];
            if (!rate) return;

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${currency.name} (${currency.code})</td>
                <td>${rate.toFixed(4)} RUB</td>
                <td>${(1 / rate).toFixed(4)} ${currency.code}</td>
            `;
            ratesBody.appendChild(row);
        });
    }

    // Вспомогательная функция для форматирования даты
    function formatDate(date) {
        const d = new Date(date);
        let month = '' + (d.getMonth() + 1);
        let day = '' + d.getDate();
        const year = d.getFullYear();

        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;

        return [year, month, day].join('-');
    }
});