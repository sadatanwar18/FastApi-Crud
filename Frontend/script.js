const API_URL = "http://127.0.0.1:8000"


// Fetch
async function fetchProducts() {
    const res = await fetch(`${API_URL}/products`);
    const products = await res.json();

    const tbody = document.querySelector("#productTable tbody");
    tbody.innerHTML = "";

    products.forEach(p => {
        const row = `
        <tr>
            <td>${p.name}</td>
            <td>${p.description}</td>
            <td>${p.price}</td>
            <td>${p.quantity}</td>
            <td>
                <button onclick="deleteProduct(${p.id})">Delete</button>
            </td>
        </tr>
        `;
        tbody.innerHTML += row
    });
}


// Add new product
document.getElementById("productForm").addEventListener("submit", async(e) =>{
    e.preventDefault();

    const newProduct = {
        name: document.getElementById("name").value,
        description: document.getElementById("description").value,
        price: parseFloat(document.getElementById("price").value),
        quantity: parseInt(document.getElementById("quantity").value)
    };

    await fetch(`${API_URL}/product`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(newProduct)
    });

    fetchProducts();
    e.target.reset();
});


// Delete
async function deleteProduct(id) {
    await fetch(`${API_URL}/product/${id}`, {
        method: "DELETE"
    });
    fetchProducts();
}

// Initial Load
fetchProducts()