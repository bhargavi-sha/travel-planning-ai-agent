import React, { useEffect, useMemo, useState } from 'react'
import { createRoot } from 'react-dom/client'
import './styles.css'
import './checkout.css'
import './admin.css'
import './admin-details.css'
import './product-form.css'
import './admin-tabs.css'
import './navigation-pages.css'

const fallback = [
  { id: 1, title: 'Echo Dot (5th Gen)', price: 49.99, rating: 4.7, reviews: 98214, category: 'Electronics', image: 'https://images.unsplash.com/photo-1543512214-318c7553f230?auto=format&fit=crop&w=500&q=80', prime: true },
  { id: 2, title: 'Noise Cancelling Headphones', price: 129.99, rating: 4.5, reviews: 4120, category: 'Electronics', image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=500&q=80', prime: true },
  { id: 3, title: 'Everyday Running Shoes', price: 64.50, rating: 4.4, reviews: 1893, category: 'Fashion', image: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=500&q=80', prime: false },
  { id: 4, title: 'Minimal Desk Lamp', price: 35.99, rating: 4.6, reviews: 726, category: 'Home', image: 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=500&q=80', prime: true },
  { id: 5, title: 'Stainless Steel Water Bottle', price: 22, rating: 4.8, reviews: 5632, category: 'Home', image: 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=500&q=80', prime: true },
  { id: 6, title: 'Smart Fitness Watch', price: 179, rating: 4.3, reviews: 2240, category: 'Electronics', image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=500&q=80', prime: true }
]
const categories = ['All', 'Electronics', 'Fashion', 'Home']

function NavigationPage({ title, data, onBack, onAdd }) {
  const isProductList = Array.isArray(data) && data.every(item => item.title && item.price !== undefined)
  return <section className="navigation-page"><button className="back" onClick={onBack}>Back to shop</button><h1>{title}</h1>{isProductList ? <div className="navigation-products">{data.map(product => <article key={product.id}><img src={product.image} alt={product.title}/><h3>{product.title}</h3><p className="price">${product.price.toFixed(2)}</p>{product.discount_percent && <p className="deal">{product.discount_percent}% off · Was ${product.original_price.toFixed(2)}</p>}<button className="add" onClick={() => onAdd(product)}>Add to cart</button></article>)}</div> : <div className="navigation-info">{Object.entries(data || {}).map(([key, value]) => <div key={key}><h2>{key.replaceAll('_', ' ')}</h2>{Array.isArray(value) ? <ul>{value.map(item => <li key={typeof item === 'string' ? item : JSON.stringify(item)}>{typeof item === 'string' ? item : JSON.stringify(item)}</li>)}</ul> : typeof value === 'object' ? <p>{Object.entries(value).map(([name, item]) => `${name}: ${item}`).join(' · ')}</p> : <p>{value}</p>}</div>)}</div>}</section>
}
function App() {
  const [products, setProducts] = useState(fallback), [query, setQuery] = useState(''), [category, setCategory] = useState('All'), [cart, setCart] = useState([]), [favorites, setFavorites] = useState([]), [notice, setNotice] = useState('')
  useEffect(() => { fetch('http://localhost:8000/api/products').then(r => r.ok ? r.json() : fallback).then(setProducts).catch(() => setProducts(fallback)) }, [])
  const visible = useMemo(() => products.filter(p => (category === 'All' || p.category === category) && p.title.toLowerCase().includes(query.toLowerCase())), [products, query, category])
  const add = p => { setCart(c => [...c, p]); setNotice(`${p.title} added to cart`); setTimeout(() => setNotice(''), 2200) }
  const toggleFavorite = p => {
    const isFavorite = favorites.includes(p.id)
    setFavorites(items => isFavorite ? items.filter(id => id !== p.id) : [...items, p.id])
    setNotice(isFavorite ? `${p.title} removed from favorites` : `${p.title} saved to favorites`)
    setTimeout(() => setNotice(''), 2200)
  }
  return <><header><div className="top"><a className="brand">shop<span>sphere</span></a><div className="location">⌖ <small>Deliver to<br/><b>Germany</b></small></div><div className="search"><select><option>All</option></select><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search ShopSphere"/><button>⌕</button></div><div className="account"><small>Hello, sign in</small><b>Account & Lists ▾</b></div><div className="orders"><small>Returns</small><b>& Orders</b></div><button className="cart">🛒 <b>Cart</b><em>{cart.length}</em></button></div><nav><b>☰ All</b><a>Today's Deals</a><a>Customer Service</a><a>Registry</a><a>Gift Cards</a><a>Sell</a><strong>Shop deals in Fashion</strong></nav></header>
  <main><section className="hero"><div><p>New season, fresh finds</p><h1>Make every day<br/>a little brighter.</h1><button onClick={() => document.querySelector('#products').scrollIntoView({behavior:'smooth'})}>Shop now</button></div></section><section className="category-grid">{[['Electronics','Explore electronics','⌁'],['Fashion','Refresh your style','◈'],['Home','Make home yours','⌂'],['Deals',"Today's best deals",'%']].map(([name,sub,icon]) => <button key={name} onClick={() => setCategory(name === 'Deals' ? 'All' : name)}><span>{icon}</span><b>{name}</b><small>{sub} →</small></button>)}</section><section className="content" id="products"><aside><h3>Department</h3>{categories.map(c => <button className={category === c ? 'active' : ''} onClick={() => setCategory(c)} key={c}>{c}</button>)}<hr/><h3>Delivery</h3><label><input type="checkbox"/> Prime eligible</label><hr/><h3>Price</h3><label><input type="checkbox"/> Under $50</label><label><input type="checkbox"/> $50 to $150</label></aside><div className="listing"><div className="list-head"><div><h2>Featured picks for you</h2><p>Discover products selected just for you</p></div><span>{visible.length} results</span></div><div className="products">{visible.map(p => <article key={p.id} onClick={() => add(p)}><div className="picture"><img src={p.image} alt={p.title}/><button className={`heart ${favorites.includes(p.id) ? 'liked' : ''}`} onClick={event => { event.stopPropagation(); toggleFavorite(p) }}>{favorites.includes(p.id) ? '♥' : '♡'}</button></div><h3>{p.title}</h3><div className="stars">★★★★★ <small>{p.rating} ({p.reviews.toLocaleString()})</small></div><p className="price"><sup>$</sup>{Math.floor(p.price)}<sup>{(p.price % 1).toFixed(2).slice(2)}</sup></p>{p.prime && <p className="prime">prime <small>FREE delivery</small></p>}<button className="add" onClick={event => { event.stopPropagation(); add(p) }}>Add to cart</button></article>)}</div></div></section></main>{notice && <div className="toast">✓ {notice}</div>}</>
}
function AppStore() {
  const [products, setProducts] = useState(fallback)
  const [query, setQuery] = useState('')
  const [category, setCategory] = useState('All')
  const [cart, setCart] = useState([])
  const [orders, setOrders] = useState([])
  const [favorites, setFavorites] = useState([])
  const [view, setView] = useState('shop')
  const [paymentOpen, setPaymentOpen] = useState(false)
  const [notice, setNotice] = useState('')
  const [productForm, setProductForm] = useState({ title: '', price: '', category: 'Electronics', image: '', prime: false })
  const [adminTab, setAdminTab] = useState('dashboard')
  const [dashboard, setDashboard] = useState({ product_count: 0, order_count: 0, preparation_count: 0, shipped_count: 0, delivered_count: 0 })
  const [navigationPage, setNavigationPage] = useState({ title: '', data: null })

  useEffect(() => { fetch('http://localhost:8000/api/products').then(r => r.ok ? r.json() : fallback).then(setProducts).catch(() => setProducts(fallback)) }, [])
  const visible = useMemo(() => products.filter(p => (category === 'All' || p.category === category) && p.title.toLowerCase().includes(query.toLowerCase())), [products, query, category])
  const total = cart.reduce((sum, item) => sum + item.price, 0)
  const add = product => { setCart(items => [...items, product]); setNotice(`${product.title} added to cart`); setTimeout(() => setNotice(''), 1800) }
  const remove = index => setCart(items => items.filter((_, itemIndex) => itemIndex !== index))
  const toggleFavorite = id => setFavorites(items => items.includes(id) ? items.filter(item => item !== id) : [...items, id])
  const addProduct = async event => {
    event.preventDefault()
    const response = await fetch('http://localhost:8000/api/admin/products', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...productForm, price: Number(productForm.price) }) })
    if (!response.ok) { setNotice('Product could not be created. Check the form and FastAPI server.'); return }
    const product = await response.json()
    setProducts(items => [...items, product])
    setProductForm({ title: '', price: '', category: 'Electronics', image: '', prime: false })
    setNotice(`${product.title} is now listed in the store.`)
    setTimeout(() => setNotice(''), 2500)
  }
  const loadOrders = () => fetch('http://localhost:8000/api/admin/orders').then(r => r.ok ? r.json() : []).then(setOrders).catch(() => setNotice('Could not load admin orders. Start the FastAPI server.'))
  const loadDashboard = () => fetch('http://localhost:8000/api/admin/dashboard').then(r => r.ok ? r.json() : Promise.reject()).then(setDashboard).catch(() => setNotice('Could not load dashboard. Start the FastAPI server.'))
  const openNavigation = async (path, title) => {
    const response = await fetch(`http://localhost:8000/api/navigation/${path}`)
    if (!response.ok) { setNotice('This page could not be loaded. Start the FastAPI server.'); return }
    setNavigationPage({ title, data: await response.json() })
    setView('navigation')
  }
  const updateStatus = (orderId, status) => {
    fetch(`http://localhost:8000/api/admin/orders/${orderId}/status`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ status }) })
      .then(r => r.ok ? r.json() : Promise.reject())
      .then(updated => { setOrders(items => items.map(item => item.id === updated.id ? updated : item)); setNotice(`${updated.id} is now ${updated.status}`); setTimeout(() => setNotice(''), 2000) })
      .catch(() => setNotice('Could not update the order. Start the FastAPI server.'))
  }
  const pay = async event => {
    event.preventDefault()
    if (!cart.length) return
    const response = await fetch('http://localhost:8000/api/orders', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ items: cart, total }) })
    if (!response.ok) { setNotice('Order could not be created. Start the FastAPI server.'); return }
    const order = await response.json()
    setOrders(existing => [order, ...existing])
    setCart([])
    setPaymentOpen(false)
    setView('orders')
    setNotice('Dummy payment accepted. Your order is confirmed.')
    setTimeout(() => setNotice(''), 3000)
  }

  return <>
    <header><div className="top"><a className="brand" onClick={() => setView('shop')}>shop<span>sphere</span></a><div className="location"><small>Deliver to<br/><b>Germany</b></small></div><div className="search"><select><option>All</option></select><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search ShopSphere"/><button>Search</button></div><button className="header-link" onClick={() => setView('orders')}><small>Returns</small><b>& Orders</b></button><button className="cart" onClick={() => setView('cart')}>Cart <em>{cart.length}</em></button></div><nav><button className="nav-link" onClick={() => openNavigation('all', 'All products')}>All</button><button className="nav-link" onClick={() => openNavigation('todays-deals', "Today's Deals")}>Today's Deals</button><button className="nav-link" onClick={() => openNavigation('customer-service', 'Customer Service')}>Customer Service</button><button className="nav-link" onClick={() => openNavigation('registry', 'Registry')}>Registry</button><button className="nav-link" onClick={() => openNavigation('gift-cards', 'Gift Cards')}>Gift Cards</button><button className="nav-link" onClick={() => openNavigation('sell', 'Sell on ShopSphere')}>Sell</button><button className="admin-link" onClick={() => { setView('admin'); setAdminTab('dashboard'); loadOrders(); loadDashboard() }}>Admin panel</button><button className="fashion-link" onClick={() => openNavigation('fashion-deals', 'Fashion deals')}>Shop deals in Fashion</button></nav></header>
    {view === 'navigation' && <NavigationPage title={navigationPage.title} data={navigationPage.data} onBack={() => setView('shop')} onAdd={add}/>} 
    {view === 'shop' && <main><section className="hero"><div><p>New season, fresh finds</p><h1>Make every day<br/>a little brighter.</h1><button onClick={() => document.querySelector('#products').scrollIntoView({ behavior: 'smooth' })}>Shop now</button></div></section><section className="category-grid">{categories.slice(1).map(name => <button key={name} onClick={() => setCategory(name)}><span>{name[0]}</span><b>{name}</b><small>Explore {name.toLowerCase()} -&gt;</small></button>)}<button onClick={() => setCategory('All')}><span>%</span><b>Deals</b><small>Today's best deals -&gt;</small></button></section><section className="content" id="products"><aside><h3>Department</h3>{categories.map(name => <button className={category === name ? 'active' : ''} onClick={() => setCategory(name)} key={name}>{name}</button>)}</aside><div className="listing"><div className="list-head"><div><h2>Featured picks for you</h2><p>Click a card or Add to cart.</p></div><span>{visible.length} results</span></div><div className="products">{visible.map(product => <article key={product.id} className="clickable-card" onClick={() => add(product)}><div className="picture"><img src={product.image} alt={product.title}/><button className={`heart ${favorites.includes(product.id) ? 'liked' : ''}`} onClick={event => { event.stopPropagation(); toggleFavorite(product.id) }}>{favorites.includes(product.id) ? '♥' : '♡'}</button></div><h3>{product.title}</h3><div className="stars">★★★★★ <small>{product.rating} ({product.reviews.toLocaleString()})</small></div><p className="price">${product.price.toFixed(2)}</p>{product.prime && <p className="prime">prime <small>FREE delivery</small></p>}<button className="add" onClick={event => { event.stopPropagation(); add(product) }}>Add to cart</button></article>)}</div></div></section></main>}
    {view === 'cart' && <section className="order-page"><button className="back" onClick={() => setView('shop')}>← Continue shopping</button><h1>Your cart</h1>{cart.length === 0 ? <div className="empty"><p>Your cart is empty.</p><button className="add" onClick={() => setView('shop')}>Shop products</button></div> : <div className="checkout-layout"><div className="cart-items">{cart.map((item, index) => <div className="cart-item" key={`${item.id}-${index}`}><img src={item.image} alt=""/><div><b>{item.title}</b><p>${item.price.toFixed(2)}</p><small>{item.prime ? 'Prime eligible' : 'Standard delivery'}</small></div><button className="remove" onClick={() => remove(index)}>Remove</button></div>)}</div><aside className="summary"><h2>Order summary</h2><p>Items ({cart.length}) <b>${total.toFixed(2)}</b></p><p>Delivery <b>FREE</b></p><hr/><h3>Total <b>${total.toFixed(2)}</b></h3><button className="add checkout" onClick={() => setPaymentOpen(true)}>Proceed to dummy payment</button></aside></div>}</section>}
    {view === 'orders' && <section className="order-page"><button className="back" onClick={() => setView('shop')}>← Continue shopping</button><h1>Your orders</h1>{orders.length === 0 ? <div className="empty"><p>No orders yet. Products added to the cart will appear here after dummy payment.</p><button className="add" onClick={() => setView('cart')}>View cart ({cart.length})</button></div> : orders.map(order => <div className="placed-order" key={order.id}><div><b>Order {order.id}</b><p>{order.date} · {order.items.length} item(s)</p></div><strong>{order.status}</strong><span>Total: ${order.total.toFixed(2)}</span><div className="ordered-items">{order.items.map((item, index) => <p key={`${item.id}-${index}`}>{item.title} — ${item.price.toFixed(2)}</p>)}</div></div>)}</section>}
    {paymentOpen && <div className="modal-backdrop"><form className="payment-modal" onSubmit={pay}><button type="button" className="close" onClick={() => setPaymentOpen(false)}>×</button><p className="demo-label">DEMO ONLY — no real payment is processed</p><h2>Dummy payment</h2><label>Name on card<input required placeholder="Jane Doe"/></label><label>Card number<input required inputMode="numeric" placeholder="4242 4242 4242 4242"/></label><div className="payment-row"><label>Expiry<input required placeholder="12/30"/></label><label>CVV<input required placeholder="123"/></label></div><p className="pay-total">Total to pay: <b>${total.toFixed(2)}</b></p><button className="add checkout" type="submit">Pay ${total.toFixed(2)} (demo)</button></form></div>}
    {view === 'admin' && <section className="order-page"><button className="back" onClick={() => setView('shop')}>Back to shop</button><div className="admin-heading"><div><p className="demo-label">ADMIN DEMO</p><h1>Admin panel</h1><p>Manage your store from one clear workspace.</p></div><button className="add" onClick={() => { loadOrders(); loadDashboard() }}>Refresh</button></div><div className="admin-tabs"><button className={adminTab === 'dashboard' ? 'selected' : ''} onClick={() => { setAdminTab('dashboard'); loadDashboard() }}>Dashboard</button><button className={adminTab === 'orders' ? 'selected' : ''} onClick={() => { setAdminTab('orders'); loadOrders() }}>Orders</button><button className={adminTab === 'products' ? 'selected' : ''} onClick={() => setAdminTab('products')}>Add product</button></div>{adminTab === 'dashboard' && <div className="dashboard-cards"><div><small>Products</small><b>{dashboard.product_count}</b></div><div><small>Total orders</small><b>{dashboard.order_count}</b></div><div><small>In preparation</small><b>{dashboard.preparation_count}</b></div><div><small>Shipped / on the way</small><b>{dashboard.shipped_count}</b></div><div><small>Delivered</small><b>{dashboard.delivered_count}</b></div></div>}{adminTab === 'products' && <form className="product-form" onSubmit={addProduct}><h2>Add a new product</h2><input required placeholder="Product name" value={productForm.title} onChange={event => setProductForm({ ...productForm, title: event.target.value })}/><input required min="0.01" step="0.01" type="number" placeholder="Price" value={productForm.price} onChange={event => setProductForm({ ...productForm, price: event.target.value })}/><select value={productForm.category} onChange={event => setProductForm({ ...productForm, category: event.target.value })}>{categories.slice(1).map(name => <option key={name}>{name}</option>)}</select><input required type="url" placeholder="Product image URL (https://...)" value={productForm.image} onChange={event => setProductForm({ ...productForm, image: event.target.value })}/><label className="prime-option"><input type="checkbox" checked={productForm.prime} onChange={event => setProductForm({ ...productForm, prime: event.target.checked })}/> Prime eligible</label><button className="add" type="submit">Add product</button></form>}{adminTab === 'orders' && (orders.length === 0 ? <div className="empty"><p>No orders available. Complete a dummy payment first.</p></div> : <div className="admin-orders">{orders.map(order => { const quantities = order.items.reduce((result, item) => ({ ...result, [item.id]: (result[item.id] || 0) + 1 }), {}); const uniqueItems = order.items.filter((item, index) => order.items.findIndex(candidate => candidate.id === item.id) === index); return <div className="admin-order" key={order.id}><div className="admin-order-info"><b>{order.id}</b><p>{order.date} · {order.items.length} item(s) · Order total: ${order.total.toFixed(2)}</p><div className="admin-item-list">{uniqueItems.map(item => <div className="admin-item" key={item.id}><img src={item.image} alt=""/><div><b>{item.title}</b><small>Unit price: ${item.price.toFixed(2)}</small><small>Quantity: {quantities[item.id]}</small></div><strong>${(item.price * quantities[item.id]).toFixed(2)}</strong></div>)}<div className="admin-subtotal"><span>Items subtotal</span><b>${order.items.reduce((sum, item) => sum + item.price, 0).toFixed(2)}</b></div></div></div><div className="status-control"><label>Status<select value={order.status} onChange={event => updateStatus(order.id, event.target.value)}><option>Preparation</option><option>Shipped</option><option>Out for delivery</option><option>Delivered</option></select></label><strong className={`status ${order.status.toLowerCase().replaceAll(' ', '-')}`}>{order.status}</strong></div></div>})}</div>)}</section>}
    {notice && <div className="toast">{notice}</div>}
  </>
}

createRoot(document.getElementById('root')).render(<AppStore />)
