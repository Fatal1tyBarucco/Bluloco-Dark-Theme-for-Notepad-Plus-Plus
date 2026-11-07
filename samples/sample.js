// Sample JS code to test Bluloco Dark
// Includes ES6+, template literals, and async/await

const apiCall = async (url) => {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (err) {
        console.error(`Error fetching ${url}: ${err}`);
    }
};

const user = {
    name: 'Gemma',
    greet() {
        console.log(`Hello, I am ${this.name}!`);
    }
};

user.greet();
