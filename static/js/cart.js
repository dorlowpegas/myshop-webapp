// Функция добавления в корзину
function addToCart(id, name, price) {
  let cart = JSON.parse(localStorage.getItem('cart') || '{}');

  if (cart[id]) {
    cart[id].quantity += 1;
  } else {
    cart[id] = { name, price, quantity: 1 };
  }

  localStorage.setItem('cart', JSON.stringify(cart));
  updateCart();
  alert(`Добавлено: ${name}`);
}

// Обновление значка корзины
function updateCart() {
  const cart = JSON.parse(localStorage.getItem('cart') || '{}');
  const count = Object.values(cart).reduce((sum, item) => sum + item.quantity, 0);
  document.getElementById('cart-count').textContent = count;

  renderCart();
}

// Открыть/закрыть корзину
function openCart() {
  document.getElementById('cart-modal').style.display = 'block';
  renderCart();
}

function closeCart() {
  document.getElementById('cart-modal').style.display = 'none';
}

// Рендер содержимого корзины
function renderCart() {
  const cart = JSON.parse(localStorage.getItem('cart') || '{}');
  const items = document.getElementById('cart-items');
  const total = document.getElementById('cart-total');

  let html = '';
  let sum = 0;

  for (const id in cart) {
    const item = cart[id];
    const itemTotal = item.price * item.quantity;
    sum += itemTotal;

    html += `
      <div class="cart-item">
        <div>
          <strong>${item.name}</strong> x${item.quantity}<br>
          ${item.price} ₽ за шт
        </div>
        <div>
          <button onclick="removeFromCart(${id})">Удалить</button>
        </div>
      </div>
    `;
  }

  items.innerHTML = html || '<p>Корзина пуста</p>';
  total.textContent = sum.toFixed(2);
}

// Удалить товар из корзины
function removeFromCart(id) {
  let cart = JSON.parse(localStorage.getItem('cart') || '{}');
  delete cart[id];
  localStorage.setItem('cart', JSON.stringify(cart));
  updateCart();
}

// Оформить заказ
document.getElementById('order-form')?.addEventListener('submit', function(e) {
  e.preventDefault();

  const cart = JSON.parse(localStorage.getItem('cart') || '{}');
  if (Object.keys(cart).length === 0) {
    alert('Корзина пуста!');
    return;
  }

  const name = document.getElementById('name').value;
  const phone = document.getElementById('phone').value;
  const address = document.getElementById('address').value;

  if (!name || !phone || !address) {
    alert('Заполните все поля!');
    return;
  }

  // Здесь можно отправить заказ на сервер (пока просто алерт)
  alert(`Заказ оформлен!\n\nИмя: ${name}\nТелефон: ${phone}\nАдрес: ${address}`);

  // Очистить корзину
  localStorage.removeItem('cart');
  updateCart();
  closeCart();
});