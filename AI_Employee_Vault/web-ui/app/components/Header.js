'use client'

import { useState } from 'react'
import './Header.css'

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <div className="logo-icon">⚡</div>
          <span>AI Employee Vault</span>
        </div>

        <nav className={`nav ${menuOpen ? 'open' : ''}`}>
          <a href="#features">Features</a>
          <a href="#platforms">Platforms</a>
          <a href="#metrics">Metrics</a>
          <a href="#actions">Actions</a>
        </nav>

        <div className="status-badge">✓ PRODUCTION READY</div>

        <button
          className="menu-toggle"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          ☰
        </button>
      </div>
    </header>
  )
}
