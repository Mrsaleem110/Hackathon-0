'use client'

import './Footer.css'

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h3 className="footer-title">AI Employee Vault</h3>
          <p className="footer-description">
            Intelligent Multi-Channel Communication & Automation Platform
          </p>
        </div>

        <div className="footer-section">
          <h4 className="footer-heading">Quick Links</h4>
          <ul className="footer-links">
            <li><a href="#features">Features</a></li>
            <li><a href="#platforms">Platforms</a></li>
            <li><a href="#metrics">Metrics</a></li>
            <li><a href="#actions">Get Started</a></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4 className="footer-heading">Resources</h4>
          <ul className="footer-links">
            <li><a href="#">Documentation</a></li>
            <li><a href="#">API Reference</a></li>
            <li><a href="#">Support</a></li>
            <li><a href="#">Status</a></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4 className="footer-heading">Legal</h4>
          <ul className="footer-links">
            <li><a href="#">Privacy Policy</a></li>
            <li><a href="#">Terms of Service</a></li>
            <li><a href="#">Security</a></li>
            <li><a href="#">Contact</a></li>
          </ul>
        </div>
      </div>

      <div className="footer-bottom">
        <p className="footer-text">
          © 2026 AI Employee Vault. All rights reserved.
        </p>
        <p className="footer-text">
          Built with ⚡ for intelligent automation
        </p>
      </div>
    </footer>
  )
}
