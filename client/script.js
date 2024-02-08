async function ping() {
    fetch('http://localhost:8000/ping')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(json => {
        data = json;
        let result_container = document.getElementsByClassName("result");
        if (result_container.length > 0) {
            result_container[0].innerText = data["ping"];
        } else {
            console.error("Failed to retreive result container");
        }
    })
    .catch(error => {
        console.error('There was an error with the fetch operation:', error);
    });
}


async function fetchUsers() {fetch('http://localhost:8000/users')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        let result_container = document.getElementsByClassName("result");
        if (result_container.length > 0) {
            result_container[0].innerText = '';
            data.forEach(user => {
                result_container[0].innerText += `${user["login"]}, ${user["password"]}\n`;
            });
        } else {
            console.error("Failed to retreive result container");
        }
    })
    .catch(error => {
        console.error('There was an error with the fetch operation:', error);
    });
}