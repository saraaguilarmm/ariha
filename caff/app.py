from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sarai3005', 
    'database': 'ariha_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

@app.route('/')
def index():
    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Ariha - Café de Especialidad</title>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
        <style>
            :root { --bg: #fcfbf9; --accent: #2c4a3e; --card: #ffffff; --border: #eae6df; --accent-hover: #1e332a; }
            body { background: var(--bg); font-family: 'Plus Jakarta Sans', sans-serif; color: #1c1c1c; margin: 0; padding: 0; }
            
            /* Navbar superior */
            nav { background: #fff; border-bottom: 1px solid var(--border); padding: 15px 40px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }
            .nav-brand { font-weight: 700; font-size: 1.2rem; color: var(--accent); }
            .nav-links { display: flex; gap: 20px; align-items: center; }
            .nav-links a { text-decoration: none; color: #555; font-weight: 600; font-size: 0.9rem; cursor: pointer; }
            .nav-links a:hover { color: var(--accent); }
            .cart-btn { background: var(--accent); color: #fff; padding: 8px 16px; border-radius: 20px; border: none; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 8px; }

            header { text-align: center; padding: 40px 20px 20px 20px; }
            header h1 { color: var(--accent); font-size: 2.8rem; margin-bottom: 5px; }
            
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px; }
            
            .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); display: flex; flex-direction: column; justify-content: space-between; transition: transform 0.2s; }
            .card:hover { transform: translateY(-4px); box-shadow: 0 8px 25px rgba(0,0,0,0.06); }
            .card-img { width: 100%; height: 150px; object-fit: cover; border-radius: 8px; background: #eee; margin-bottom: 12px; cursor: pointer; }
            .category { font-size: 0.7rem; text-transform: uppercase; color: var(--accent); font-weight: 700; letter-spacing: 1px; margin-bottom: 4px; }
            .title { font-size: 1.05rem; font-weight: 700; margin-bottom: 4px; cursor: pointer; }
            .prep { font-size: 0.8rem; color: #666; margin-bottom: 10px; }
            
            .card-footer { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border); padding-top: 12px; margin-top: 10px; }
            .price { font-size: 1.15rem; font-weight: 700; color: var(--accent); }
            .btn-add { background: var(--accent); color: #fff; border: none; padding: 8px 14px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 0.85rem; transition: background 0.2s; position: relative; z-index: 10; }
            .btn-add:hover { background: var(--accent-hover); }

            /* Sección de Contacto */
            .contact-section { background: #fff; border-top: 1px solid var(--border); margin-top: 60px; padding: 50px 20px; }
            .contact-container { max-width: 800px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }
            .contact-info h3 { color: var(--accent); margin-top: 0; }
            .contact-info p { font-size: 0.95rem; color: #444; line-height: 1.6; margin: 10px 0; }
            .contact-form input, .contact-form textarea { width: 100%; padding: 10px; margin-bottom: 12px; border: 1px solid var(--border); border-radius: 8px; box-sizing: border-box; font-family: inherit; }
            .contact-form button { background: var(--accent); color: #fff; border: none; padding: 10px 20px; border-radius: 8px; font-weight: 600; cursor: pointer; width: 100%; }

            /* Modales (Carrito y Pago) */
            .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); justify-content: center; align-items: center; z-index: 1000; }
            .modal-content { background: #fff; padding: 30px; border-radius: 16px; width: 100%; max-width: 450px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); max-height: 90vh; overflow-y: auto; }
            .modal-content h2 { margin-top: 0; color: var(--accent); font-size: 1.4rem; margin-bottom: 15px; }
            .cart-item { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding: 10px 0; font-size: 0.9rem; }
            .cart-total { font-size: 1.2rem; font-weight: 700; text-align: right; margin: 20px 0; color: var(--accent); }
            
            .form-group { margin-bottom: 15px; }
            .form-group label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 5px; color: #444; }
            .form-group input { width: 100%; padding: 10px; border: 1px solid var(--border); border-radius: 8px; font-size: 0.95rem; box-sizing: border-box; }
            
            .btn { padding: 10px 18px; border-radius: 8px; font-weight: 600; cursor: pointer; border: none; font-size: 0.9rem; width: 100%; margin-top: 5px; }
            .btn-primary { background: var(--accent); color: #fff; }
            .btn-secondary { background: #eee; color: #333; margin-top: 10px; }
        </style>
    </head>
    <body>

        <! Navbar >
        <nav>
            <div class="nav-brand">𝐀𝐫𝐢𝐡𝐚 𝐂𝐨𝐟𝐟𝐞𝐞</div>
            <div class="nav-links">
                <a href="#catalog">Menú</a>
                <a href="#contact">Contacto</a>
                <button class="cart-btn" onclick="openCartModal()">
                     Carrito (<span id="cartCount">0</span>)
                </button>
            </div>
        </nav>

        <header id="catalog">
            <p style="letter-spacing: 2px; font-size: 0.8rem; font-weight: 700; color: #2c4a3e;">CAFÉ DE ESPECIALIDAD</p>
            <h1>Ariha</h1>
            <p style="color: #666; font-weight: 600;">Especialidad en la casa</p>
        </header>

        <div class="container">
            <div class="grid" id="container">Cargando catálogo desde MySQL...</div>
        </div>

        <! Sección Contacto >
        <section class="contact-section" id="contact">
            <div class="contact-container">
                <div class="contact-info">
                    <h3>Contáctanos</h3>
                    <p>¿Tienes dudas con tu pedido o quieres visitarnos? Estamos para servirte el mejor café de especialidad.</p>
                    <p> <strong>Teléfono:</strong> <a href="tel:4623064259" style="color: var(--accent); text-decoration: none;">462 306 4259</a></p>
                    <p> <strong>Correo:</strong> <a href="mailto:ariha.coffe@gmail.com" style="color: var(--accent); text-decoration: none;">ariha.coffe@gmail.com</a></p>
                </div>
                <div class="contact-form">
                    <h3>Envíanos un mensaje</h3>
                    <input type="text" id="msgName" placeholder="Tu nombre">
                    <input type="email" id="msgEmail" placeholder="Tu correo electrónico">
                    <textarea id="msgText" rows="3" placeholder="Escribe tu mensaje..."></textarea>
                    <button onclick="sendContactMessage()">Enviar Mensaje</button>
                </div>
            </div>
        </section>

        <! MODAL DEL CARRITO >
        <div class="modal" id="cartModal">
            <div class="modal-content">
                <h2>Tu Carrito de Compras</h2>
                <div id="cartItemsList">Tu carrito está vacío.</div>
                <div class="cart-total" id="cartTotalSum">Total: $0.00 MXN</div>
                <button class="btn btn-primary" onclick="openCheckoutModal()" id="checkoutBtn" style="display:none;">Pagar con Tarjeta</button>
                <button class="btn btn-secondary" onclick="closeCartModal()">Cerrar</button>
            </div>
        </div>

        <! MODAL DE PAGO CON TARJETA >
        <div class="modal" id="checkoutModal">
            <div class="modal-content">
                <h2>Pago Seguro con Tarjeta</h2>
                <div class="form-group">
                    <label>Nombre del titular</label>
                    <input type="text" id="cardName" placeholder="Como aparece en la tarjeta">
                </div>
                <div class="form-group">
                    <label>Número de Tarjeta</label>
                    <input type="text" id="cardNumber" placeholder="4532 •••• •••• 8920" maxlength="16">
                </div>
                <div style="display: flex; gap: 10px;">
                    <div class="form-group" style="flex: 1;">
                        <label>Expiración</label>
                        <input type="text" id="cardExp" placeholder="MM/AA" maxlength="5">
                    </div>
                    <div class="form-group" style="flex: 1;">
                        <label>CVV</label>
                        <input type="password" id="cardCvv" placeholder="123" maxlength="4">
                    </div>
                </div>
                <button class="btn btn-primary" onclick="processPayment()">Confirmar y Pagar</button>
                <button class="btn btn-secondary" onclick="closeCheckoutModal()">Cancelar</button>
            </div>
        </div>

        <script>
            let productsData = [];
            let cart = [];

            async function loadProducts() {
                try {
                    const response = await fetch('/api/products');
                    productsData = await response.json();
                    renderGrid();
                } catch (e) {
                    document.getElementById('container').innerText = 'Error al conectar con la base de datos.';
                }
            }

            function renderGrid() {
                const container = document.getElementById('container');
                container.innerHTML = '';

                productsData.forEach((p, index) => {
                    const imgSrc = p.image || 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=500&q=80';
                    const price = (65 + (p.Calories || 0) * 0.1).toFixed(2);
                    
                    const card = document.createElement('div');
                    card.className = 'card';
                    card.innerHTML = `
                        <div>
                            <img class="card-img" src="${imgSrc}" alt="${p.Beverage}">
                            <div class="category">${p.Beverage_category || 'Especialidad'}</div>
                            <div class="title">${p.Beverage || 'Café Ariha'}</div>
                            <div class="prep">${p.Beverage_prep || 'Estándar'}</div>
                        </div>
                        <div>
                            <div style="font-size: 0.8rem; color: #777; margin-bottom: 6px;">${p.Calories || 0} kcal</div>
                            <div class="card-footer">
                                <span class="price">$${price}</span>
                                <button class="btn-add" onclick="addToCart(event, ${index})">Agregar</button>
                            </div>
                        </div>
                    `;
                    container.appendChild(card);
                });
            }

            function addToCart(event, index) {
                event.stopPropagation(); // Evita conflictos con contenedores o imágenes
                const product = productsData[index];
                const price = 65 + (product.Calories || 0) * 0.1;
                cart.push({ name: product.Beverage, price: price });
                updateCartCount();
                alert(`¡"${product.Beverage}" agregado al carrito con éxito!`);
            }

            function updateCartCount() {
                document.getElementById('cartCount').innerText = cart.length;
            }

            function openCartModal() {
                const listContainer = document.getElementById('cartItemsList');
                const checkoutBtn = document.getElementById('checkoutBtn');
                
                if (cart.length === 0) {
                    listContainer.innerHTML = 'Tu carrito está vacío.';
                    document.getElementById('cartTotalSum').innerText = 'Total: $0.00 MXN';
                    checkoutBtn.style.display = 'none';
                } else {
                    let html = '';
                    let total = 0;
                    cart.forEach((item, idx) => {
                        total += item.price;
                        html += `<div class="cart-item"><span>${item.name}</span> <b>$${item.price.toFixed(2)}</b></div>`;
                    });
                    listContainer.innerHTML = html;
                    document.getElementById('cartTotalSum').innerText = `Total: $${total.toFixed(2)} MXN`;
                    checkoutBtn.style.display = 'block';
                }
                document.getElementById('cartModal').style.display = 'flex';
            }

            function closeCartModal() {
                document.getElementById('cartModal').style.display = 'none';
            }

            function openCheckoutModal() {
                closeCartModal();
                document.getElementById('checkoutModal').style.display = 'flex';
            }

            function closeCheckoutModal() {
                document.getElementById('checkoutModal').style.display = 'none';
            }

            function processPayment() {
                const name = document.getElementById('cardName').value;
                const number = document.getElementById('cardNumber').value;
                if(!name || number.length < 15) {
                    alert('Por favor ingresa datos de tarjeta válidos.');
                    return;
                }
                alert('¡Pago procesado con éxito! Gracias por tu compra en Ariha.');
                cart = [];
                updateCartCount();
                closeCheckoutModal();
            }

            function sendContactMessage() {
                const name = document.getElementById('msgName').value;
                const email = document.getElementById('msgEmail').value;
                const text = document.getElementById('msgText').value;
                if(!name || !email || !text) {
                    alert('Por favor llena todos los campos de contacto.');
                    return;
                }
                alert(`¡Gracias ${name}! Tu mensaje ha sido enviado a ariha.coffe@gmail.com correctamente.`);
                document.getElementById('msgName').value = '';
                document.getElementById('msgEmail').value = '';
                document.getElementById('msgText').value = '';
            }

            loadProducts();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True, port=5000)