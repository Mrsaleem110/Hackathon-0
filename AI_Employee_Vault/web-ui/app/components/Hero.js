'use client'

import './Hero.css'

export default function Hero() {
  return (
    <section className="hero fade-in">
      <div className="hero-content">
        <h1 className="hero-title">AI Employee Vault</h1>
        <p className="hero-subtitle">
          Intelligent Multi-Channel Communication & Automation Platform
        </p>
        <p className="hero-description">
          Automate your workflow across 6+ platforms with intelligent orchestration,
          real-time monitoring, and human-in-the-loop approval systems.
        </p>
        <div className="hero-buttons">
          <button className="btn btn-primary">Get Started</button>
          <button className="btn btn-secondary">Learn More</button>
        </div>
      </div>
      <div className="hero-visual">
        <div className="floating-card card-1">
          <div className="card-icon">📧</div>
          <div className="card-text">Email Detection</div>
        </div>
        <div className="floating-card card-2">
          <div className="card-icon">💼</div>
          <div className="card-text">LinkedIn</div>
        </div>
        <div className="floating-card card-3">
          <div className="card-icon">📱</div>
          <div className="card-text">WhatsApp</div>
        </div>
      </div>
    </section>
  )
}
