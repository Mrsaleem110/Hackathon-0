'use client'

import './Platforms.css'

export default function Platforms() {
  const platforms = [
    { icon: '📧', name: 'Gmail', status: 'Active' },
    { icon: '💼', name: 'LinkedIn', status: 'Active' },
    { icon: '📱', name: 'WhatsApp', status: 'Active' },
    { icon: '📸', name: 'Instagram', status: 'Ready' },
    { icon: '👍', name: 'Facebook', status: 'Ready' },
    { icon: '𝕏', name: 'Twitter/X', status: 'Ready' },
  ]

  return (
    <section id="platforms" className="platforms-section fade-in">
      <div className="platforms-container">
        <h2 className="section-title">Connected Platforms</h2>
        <div className="platforms-grid">
          {platforms.map((platform, index) => (
            <div key={index} className="platform-card">
              <div className="platform-icon">{platform.icon}</div>
              <div className="platform-name">{platform.name}</div>
              <div className={`platform-status ${platform.status.toLowerCase()}`}>
                ✓ {platform.status}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
