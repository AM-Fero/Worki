async function getData() {
    try {
        // Replace with your actual endpoint URL
        const response = await fetch('http://localhost:5002//api/worki-auth/get-unis', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const data = await response.json();

        if (response.ok) {
            console.log(data);
            const parent = document.getElementById('table');
            const table = document.createElement('table');
            table.setAttribute('border', '1'); // Optional: adds border
            for (let i = 0; i < data['Email'].length; i++) {
                const tr = document.createElement('tr');
                const td = document.createElement('td')
                const td2 = document.createElement('td')
                const td3 = document.createElement('td')
                const td4 = document.createElement('td');
                const td5 = document.createElement('td');

                const deletebutton = document.createElement('button');
                deletebutton.textContent = 'Удалить';
                deletebutton.className = "main-btn";
                td5.appendChild(deletebutton);

                td.textContent = data['Email'][i];
                td2.textContent = data['Name'][i];
                td3.textContent = data['FullName'][i];
                if (data['Status'][i] == false) {
                    const button = document.createElement('button');
                    button.textContent = 'Одобрить';
                    button.className = "btn-2";
                    td4.appendChild(button)
                }
                else {
                    td4.textContent = "+"
                }

                tr.appendChild(td2);
                tr.appendChild(td);
                //tr.appendChild(td3);
                tr.appendChild(td4);
                tr.appendChild(td5);
                table.appendChild(tr);
            }
            parent.appendChild(table);

        } else {

        }

    } catch (error) {
        // Network or other errors
        console.error('Fetch error:', error);
    }
}
getData();